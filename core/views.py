
from random import choice
from django.shortcuts import render, redirect
import markdown
from .models import Chapter, Article, Part, UrlData
from haystack.query import SQ

from elasticsearch import Elasticsearch
from django.utils.html import strip_tags
import pandas as pd
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Q
import ast
import json
def home(request):
    return render(request, "home.html")


def toc(request):
 
    return render(request, "toc.html",{
        'chapters': Chapter.objects.all(),
        'parts': Part.objects.all()
       
    })
def mentions(request):
 
    return render(request, "mentions-legales.html")
def part(request, n, slug=''):
    part = Part.objects.get(number=n)
    prev = None
    next = None
    print( part.main_title)
    try:
        prev  = Article.objects.get(id = int(part.id)-1)
        prev.desc = "Section précédente"
        prev.url = "/section/"
    except Article.DoesNotExist:
        prev = None
    if prev is None:
        try:
            print(part.id)
            prev = Chapter.objects.get(id=int(part.id) -1)

            prev.desc = "Chapitre précédent"
            prev.url = "/chapitre/"
        except Chapter.DoesNotExist:
            prev = None


    try:
        next  = Article.objects.get(id = int(part.id)+1)
        next.desc = "Section suivante"
        next.url = "/section/"
    except Article.DoesNotExist:
        next = None
    if next is None:
        try:
            next = Chapter.objects.get(id = int(part.id)+1)
            next.desc = "Chapitre suivant"
            next.url = "/chapitre/"
        except Chapter.DoesNotExist:
            next = None


    return render(request, "part.html", {
        'subject': part,
        'content': markdown.Markdown().convert(part.content),
        'next': next,
        'prev': prev,
        'book_navigation':None,
        'title' : part.title,
    })

def chapter(request, n, slug=''):
    chapter = Chapter.objects.get(number=n)
    prev = None
    next = None
    print( chapter.main_title)
    try:
        prev  = Article.objects.get(id = int(chapter.id)-1)
        prev.desc = "Section précédente"
        prev.url = "/section/"
    except Article.DoesNotExist:
        prev = None
    if prev is None:
        try:
            prev = Chapter.objects.get(number=int(n) -1)
            print( chapter.number)
            prev.desc = "Chapitre précédent"
            prev.url = "/chapitre/"
        except Chapter.DoesNotExist:
            prev = None


    try:
        next  = Article.objects.get(id = int(chapter.id)+1)
        next.desc = "Section suivante"
        next.url = "/section/"
    except Article.DoesNotExist:
        next = None
    if next is None:
        try:
            next = Chapter.objects.get(number = int(chapter.number)+1)
            next.desc = "Chapitre suivant"
            next.url = "/chapitre/"
        except Chapter.DoesNotExist:
            next = None


    return render(request, "chapter.html", {
        'subject': chapter,
        'content': markdown.Markdown().convert(chapter.text),
        'next': next,
        'prev': prev,
        'book_navigation':None,
        'title' : chapter.sub_title,
    })

def section(request, n, slug):

    article = Article.objects.get(number=n)
    res = article.measures

    article.measures =  ast.literal_eval(res)
  
    prev = None
    next = None

    #previous 
    try:
        prev = Article.objects.get(id = int(article.id)-1)
        prev.desc = "Section précédente"
        prev.url = "/section/"
    except Article.DoesNotExist:
        prev = None
    
    #next
    try:
         next = Article.objects.get(id = int(article.id)+1)
         next.desc = "Section suivante"
         next.url = "/section/"
    except Article.DoesNotExist:
        next = None
    if next is None:
        try:
            next = Chapter.objects.get(number = int(article.chapter.number)+1)
            next.desc = "Chapitre suivant"
            next.url = "/chapitre/"
        except Chapter.DoesNotExist:
            next = None   

    return render(request, "section.html", {
        'subject': article,
        'content': markdown.Markdown().convert(article.text),
        'next': next,
        'prev': prev,
        'book_navigation':None,
        'title' : article.title,
    })


def random(request):
    article = choice(list(Article.objects.all()))

    return redirect(f'/section/{article.number}/{article.slug}')
  

def fin(request):
    baseurl = request.build_absolute_uri()
    return render(request, "fin.html", { 'baseurl': baseurl })



def recherche(request):
    """My custom search view."""

   
    # further filter queryset based on some set of criteria     
    req = request.GET.get('q','')
    print(req)
  #  res  = queryset.filter(content_auto=req)
    #highlight = MyHighlighter(req, html_tag='mark', css_class='found', max_length=35)     
    #for r in res:
        #   highlight.highlight(r.content)
        
        #  highlight.highlight(r.content)
    elastic_client = Elasticsearch()
    # create a Python dictionary for the search query:
    search_param = {
        "query": {
            "simple_query_string": {
                "query": req,
                "fields": ["title_auto","content_auto"], 
                "default_operator": "or",       
            }
            },
                "highlight" : {
                "require_field_match": True,
                "pre_tags" : ["<mark>"],
                    "post_tags" : ["</mark>"],
                "fields": {
                     "title_auto": {
                "fragment_size": 300,           
                     }, 
                 "content_auto": {
                "fragment_size": 300,
              

            }
                }
    }
    }
    # get a response from the cluster
    response = elastic_client.search(index="haystack", body=search_param)
    connections.create_connection(hosts=['localhost'], timeout=20)
    s = Search(index='haystack')
    q = Q("multi_match", query=req, fields=['title_auto','content_auto'])
    s = s.query(q).extra(from_=0, size=100)
    s = s.highlight('title_auto', 'content_auto',pre_tags=["<mark>"],post_tags=["</mark>"],require_field_match=True, number_of_fragments=1, fragment_size=300)
    s = s.execute()
    for h in s.hits:  
        print(h.content)
    return render(request, "recherche.html", {
        'query': s,
        'request' :req
    })

def redirect_short(request,n):
     content = UrlData.objects.get(slug=request.path)
     print(content)
     return redirect( content.url,n = n)
