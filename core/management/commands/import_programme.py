import glob, os

from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from core.models import Chapter, Article


class Command(BaseCommand):
    def handle(self, *args, **options):
        Article.objects.all().delete()
        Chapter.objects.all().delete()

        for file in glob.glob("programme/chapitre*/index.md"):
            title = open(file,encoding='utf-8').read().split('\n')[0][1:].strip()
            print("numero du fichier",file.split('chapitre-')[1].split('\\')[0])
            Chapter(
                number=file.split('chapitre-')[1].split('\\')[0],
                slug=slugify(title),
                title=title,
                content='\n'.join(open(file,encoding='utf-8').read().split('\n')[1:]),
            ).save()


        for file in glob.glob("programme/chapitre*/*.md"):
            if 'index.md' in file:
                continue
            chapter_number = file.split('chapitre-')[1].split('\\')[0]
            print(chapter_number)
            chapter = Chapter.objects.get(number=chapter_number)
            title = open(file,encoding='utf-8').read().split('\n')[0][1:].strip()
            Article(
                number=int(file.split('\\')[-1].replace('.md', '')),
                slug=slugify(title),
                title=title,
                content='\n'.join(open(file,encoding='utf-8').read().split('\n')[1:]),
                chapter=chapter,
            ).save()