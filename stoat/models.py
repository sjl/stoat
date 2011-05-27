from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.db.models.loading import get_model
from treebeard.mp_tree import MP_Node

import stemplates

ALLOWED_CHARS = 'abcdefghijklmnopqrstuvwxyz1234567890_'
def clean_field_title(title):
    return ''.join((c if c in ALLOWED_CHARS else '_') for c in title.lower())


CONTENT_TYPES = (
    ('char', 'char'),
    ('text', 'text'),
    ('ckeditor', 'ckeditor'),
    ('img', 'img'),
    ('fk', 'fk'),
    ('int', 'int'),)
TEMPLATES = [(name, name) for name in settings.STOAT_TEMPLATES.keys()]


class Page(MP_Node):
    title = models.CharField(max_length=100, verbose_name='page title')
    slug = models.SlugField(max_length=100, blank=True)
    template = models.CharField(max_length=100, choices=TEMPLATES,
                                default=settings.STOAT_DEFAULT_TEMPLATE)
    url = models.CharField(max_length=255, blank=True, unique=True)

    class Meta:
        pass


    def __unicode__(self):
        return u'%s' % self.title

    def full_url(self):
        url = '/' + '/'.join(p.slug for p in list(self.get_ancestors()) + [self] if p.slug)

        # Make sure the URL ends with a slash, as god intended.
        # This little endswith dance is done to handle the root url ('/') correctly.
        if not url.endswith('/'):
            url = url + '/'

        return url

    def save(self, *args, **kwargs):
        self.url = self.full_url()
        resp = super(Page, self).save(*args, **kwargs)

        # Resave children to update slugs.
        for p in self.get_descendants():
            p.save()

        return resp


    def fields(self):
        if not hasattr(self, '_fields'):
            self._fields = dict((clean_field_title(pc.title), pc.get_content())
                                for pc in self.pagecontent_set.all())

        return self._fields

    def f(self):
        return self.fields()


    def get_absolute_url(self):
        return self.url


    def breadcrumbs(self):
        return list(self.get_ancestors()) + [self]


    def nav_siblings(self):
        return list(self.get_siblings())

    def nav_children(self):
        return list(self.get_children())

    def nav_siblings_and_children(self):
        siblings = self.nav_siblings()
        results = []
        for sibling in siblings:
            results.append([sibling, sibling.get_children()])

        return results

    def nav_roots(self):
        return list(self.get_root().get_siblings())

    def nav_roots_and_children(self):
        roots = self.nav_roots()
        results = []
        for root in roots:
            results.append([root, root.get_children()])

        return results




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

