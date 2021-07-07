from random import choice

from django.shortcuts import render, redirect
import markdown

from .models import Chapter, Article


def home(request):
    return render(request, "home.html")


def toc(request):
    return render(request, "toc.html",{
        'chapters': Chapter.objects.all()
    })


def chapter(request, n, slug):
    chapter = Chapter.objects.get(number=n)
    return render(request, "chapter.html", {
        'chapter': chapter,
        'content': markdown.Markdown().convert(chapter.content),
    })


def section(request, n, slug):
    article = Article.objects.get(number=n)
    return render(request, "section.html", {
        'article': article,
        'content': markdown.Markdown().convert(article.content),
    })


def random(request):
    article = choice(list(Article.objects.all()))
    return redirect(f'/section/{article.number}/{article.slug}')


def search(request):
    q = request.GET.get("termes")
    articles = Article.objects.filter(content__icontains=q)
    return render(request, "search.html", {
        'articles': articles
    })


