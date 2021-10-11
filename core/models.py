from django.db import models


class Chapter(models.Model):
    number = models.CharField(max_length=500, primary_key=True)
    slug = models.CharField(max_length=500)
    entity=models.CharField(max_length=500, default='')
    title = models.CharField(max_length=500)
    id =  models.IntegerField(default=1)
    content = models.TextField()
    main_title = models.CharField(max_length=500,default='')
    sub_title = models.CharField(max_length=500,default='')
    text =  models.TextField(default='')

    class Meta:
        ordering = ('number',)


class Article(models.Model):
    number = models.IntegerField(primary_key=True)
    slug = models.CharField(max_length=500)
    entity=models.CharField(max_length=50, default='')
    title = models.CharField(max_length=500)
    id =  models.IntegerField(default=1)
    content = models.TextField()
    chapter = models.ForeignKey(Chapter, on_delete=models.DO_NOTHING)
    text =  models.TextField(default='')

    class Meta:
        ordering = ('number',)


class UrlData(models.Model):
    url = models.CharField(max_length=200)
    slug = models.CharField(max_length=15)

    class Meta:
        ordering = ('slug',)
