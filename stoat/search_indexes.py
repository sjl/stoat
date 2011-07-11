import datetime
from haystack.indexes import *
from haystack import site

from django.conf import settings

from models import Page

INDEX_CLASS = getattr(settings, 'STOAT_HAYSTACK_INDEX_CLASS', SearchIndex)

class PageIndex(INDEX_CLASS):
    text = CharField(document=True, use_template=True)
    title = CharField(model_attr='title')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Page.objects.all()


site.register(Page, PageIndex)

