import datetime
from haystack import indexes
from .models import Chapter, Article
from .search_backends import CustomEdgeNgramField

class ChapterIndex(indexes.SearchIndex, indexes.Indexable):
   
    text = indexes.EdgeNgramField(document=True, use_template=True) 
    content = indexes.CharField(model_attr='content')
    number = indexes.CharField(model_attr='number')
    slug = indexes.CharField(model_attr='slug')
    title = indexes.CharField(model_attr='title')
    main_title = indexes.CharField(model_attr='main_title')
    sub_title = indexes.CharField(model_attr='sub_title')
    entity = indexes.CharField(model_attr='entity')
    id = indexes.IntegerField(model_attr='id')
  # We add this for autocomplete.
    content_auto = CustomEdgeNgramField(model_attr='content',index_analyzer="snowball")
    title_auto = CustomEdgeNgramField(model_attr='title',index_analyzer="snowball")

    def get_model(self):
        return Chapter
    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    content = indexes.CharField(model_attr='content')
    number = indexes.CharField(model_attr='number')
    slug = indexes.CharField(model_attr='slug')
    title = indexes.CharField(model_attr='title')
    entity = indexes.CharField(model_attr='entity')
    id = indexes.IntegerField(model_attr='id')
      # We add this for autocomplete.
    content_auto = CustomEdgeNgramField(model_attr='content',index_analyzer="french_elision")
    title_auto = CustomEdgeNgramField(model_attr='title',index_analyzer="french_elision")





    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

