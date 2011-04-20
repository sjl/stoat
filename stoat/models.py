from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from treebeard.mp_tree import MP_Node

import stemplates


CONTENT_TYPES = (
    ('char', 'char'),
    ('text', 'text'),
    ('html', 'html'),
    ('img', 'img'),
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
        url = '/' + '/'.join(p.slug for p in list(self.get_ancestors()) + [self])

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
            self._fields = dict((pc.title.lower(), pc.content)
                                for pc in self.pagecontent_set.all())

        return self._fields


    def get_absolute_url(self):
        return self.url


class PageContent(models.Model):
    page = models.ForeignKey(Page)
    title = models.CharField(max_length=40)
    typ = models.CharField(max_length=4, choices=CONTENT_TYPES, verbose_name='type')
    content = models.TextField(blank=True)

    class Meta:
        unique_together = (('title', 'page'),)


    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.typ)

def clean_content(sender, instance, **kwargs):
    page = instance
    fields = dict(stemplates.get_fields(page.template))
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

