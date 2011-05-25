import datetime
from haystack.indexes import *
from haystack import site
from models import Page


class PageIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    title = CharField(model_attr='title')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Page.objects.all()


site.register(Page, PageIndex)

