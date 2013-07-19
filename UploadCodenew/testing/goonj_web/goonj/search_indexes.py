import datetime
from haystack.indexes import *
from haystack import site
from goonj.models import Story


class StoryIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    title = CharField(model_attr='title', faceted=True)
    date = DateTimeField(model_attr='date')

    #def index_queryset(self):
        #"""Used when the entire index for model is updated."""
        #return Story.objects.filter(date__lte=datetime.datetime.now())


site.register(Story, StoryIndex)

