from django.db import models



class Part(models.Model):
    number = models.CharField(max_length=500, primary_key=True)
    slug = models.CharField(max_length=500)
    entity=models.CharField(max_length=500, default='')
    title = models.CharField(max_length=500)
    id =  models.IntegerField(default=1)
    content = models.TextField()
    main_title = models.CharField(max_length=500,default='')
    text =  models.TextField(default='')
    #newsetup
    forewords = models.TextField(default='')
    class Meta:
        ordering = ('number',)

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
    part = models.ForeignKey(Part, on_delete=models.DO_NOTHING,default='')


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
    #new setup
    key = models.TextField(default='')
    measures = models.TextField(default='')
    asavoir = models.TextField(default='')
    forewords = models.TextField(default='')
    

    class Meta:
        ordering = ('number',)


class UrlData(models.Model):
    url = models.CharField(max_length=200)
    slug = models.CharField(max_length=15)

    class Meta:
        ordering = ('slug',)

class Measure(models.Model):
    number = models.IntegerField(primary_key=True)
    section = models.ForeignKey(Article, on_delete=models.DO_NOTHING)
    text=models.TextField( default='')
    key = models.BooleanField(default=False)


    class Meta:
        ordering = ('number',)