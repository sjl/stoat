# {{{
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.db.models.loading import get_model
from django.db.models.signals import post_save
from treebeard.mp_tree import MP_Node

import stemplates
# }}}

ALLOWED_CHARS = 'abcdefghijklmnopqrstuvwxyz1234567890_'
def clean_field_title(title):
    """Return a "clean" version of the title, suitable for template/variable use.

    Ex:
        "Hello" -> "hello"
        "Hello World!" -> "hello_world"
    """
    return ''.join((c if c in ALLOWED_CHARS else '_') for c in title.lower())


CONTENT_TYPES = (
    ('char', 'char'),
    ('text', 'text'),
    ('ckeditor', 'ckeditor'),
    ('img', 'img'),
    ('fk', 'fk'),
    ('int', 'int'),)
TEMPLATES = sorted([(name, name) for name in settings.STOAT_TEMPLATES.keys()])


class Page(MP_Node):
    title = models.CharField(max_length=100, verbose_name='page title')
    slug = models.SlugField(max_length=100, blank=True)
    template = models.CharField(max_length=100, choices=TEMPLATES,
                                default=settings.STOAT_DEFAULT_TEMPLATE)
    url = models.CharField(max_length=255, blank=True, unique=True)
    show_in_nav = models.BooleanField(default=False)

    class Meta:
        pass


    def __unicode__(self):
        return u'%s' % self.title

    def full_url(self):
        """Return the full URL of this page, taking ancestors into account."""

        url = '/' + '/'.join(p.slug for p in list(self.get_ancestors()) + [self] if p.slug)

        # Make sure the URL ends with a slash, as god intended.
        # This little endswith dance is done to handle the root url ('/') correctly.
        if not url.endswith('/'):
            url = url + '/'

        return url

    def save(self, *args, **kwargs):
        """Save the page.

        Does a few interesting things:

        * Regenerates the stored URL.
        * Saves children so their URLs will be regenerated as well.
        * Clears the cache of this page's children.
        """
        skip_cache_clear = kwargs.pop('skip_cache_clear', False)

        # Regenerate the URL.
        self.url = self.full_url()

        if not skip_cache_clear and self.id:
            # Clear this page's ancestor cache.
            key = 'stoat:pages:%d:children' % (self.id)
            cache.delete(key)

        # Save the page.
        resp = super(Page, self).save(*args, **kwargs)

        # Resave children to update slugs.
        for p in self.get_descendants():
            p.save(skip_cache_clear=True)

        if not skip_cache_clear:
            # Clear the cache for the NEW set of ancestors.
            self._clear_ancestor_caches()

        return resp


    def fields(self):
        """Return a dict of this page's content (MEMOIZED)."""
        if not hasattr(self, '_fields'):
            self._fields = dict((clean_field_title(pc.title), pc.get_content())
                                for pc in self.pagecontent_set.all())

        return self._fields

    def f(self):
        """A simple alias for fields()."""
        return self.fields()


    def get_absolute_url(self):
        return self.url


    def breadcrumbs(self):
        """Return a list of this pages' ancestors and itself."""
        return list(self.get_ancestors()) + [self]


    def nav_siblings(self):
        """Return a list of sibling Page objects (including this page)."""
        return list(self.get_siblings().filter(show_in_nav=True))

    def nav_children(self):
        """Return a list of child Page objects."""
        return list(self.get_children().filter(show_in_nav=True))

    def nav_siblings_and_children(self):
        """Return a nested list of sibling/children Page objects (including this page)."""
        siblings = self.nav_siblings()
        results = []
        for sibling in siblings:
            results.append([sibling, sibling.get_children().filter(show_in_nav=True)])

        return results


    def _clear_ancestor_caches(self):
        """Clear the child ID caches for all of this page's ancestors."""
        for page in Page.objects.get(id=self.id).get_ancestors():
            key = 'stoat:pages:%d:children' % (page.id)
            cache.delete(key)


class PageContent(models.Model):
    page = models.ForeignKey(Page)
    title = models.CharField(max_length=40)
    cleaned_title = models.CharField(max_length=40, editable=False)
    typ = models.CharField(max_length=12, choices=CONTENT_TYPES, verbose_name='type')
    content = models.TextField(blank=True)

    class Meta:
        unique_together = (('title', 'page'),)


    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.typ)

    def save(self, *args, **kwargs):
        self.cleaned_title = clean_field_title(self.title)
        return super(PageContent, self).save(*args, **kwargs)


    def get_content(self):
        """Return the actual content.

        If this is a ForeignKey, the model instance it points at will be returned.
        Otherwise, the content itself is returned as a string.
        """
        if self.typ == 'fk':
            if not self.content:
                return None

            options = stemplates.get_field(self.page.template, self.title)[2]

            app_label = options.get('app', 'stoat')
            model_name = options.get('model', 'Page')
            model = get_model(app_label, model_name)

            try:
                return model.objects.get(id=self.content)
            except model.DoesNotExist:
                return None
        else:
            return self.content


def clean_content(sender, instance, **kwargs):
    """Clean the PageContent objects for a given Page.

    New, needed PageContent objects will be created.
    Existing, needed PageContent objects will not be touched.
    Unneeded PageContent objects will be deleted.

    """
    if kwargs.get('raw'):
        # We're in loaddata (or something similar).
        return

    page = instance
    fields = dict(stemplates.get_fields_bare(page.template))
    current_contents = list(page.pagecontent_set.all())

    for content in current_contents:
        if content.title not in fields or fields[content.title] != content.typ:
            content.delete()

    existing_contents = dict([(pc.title, pc.typ)
                              for pc in page.pagecontent_set.all()])

    for title, typ in fields.items():
        if title not in existing_contents or existing_contents[title] != typ:
            PageContent(page=page, title=title, typ=typ, content='').save()

post_save.connect(clean_content, sender=Page, dispatch_uid='stoat-clean_content')

