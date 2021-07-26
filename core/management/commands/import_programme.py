import glob, os

from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags
from core.models import Chapter, Article


class Command(BaseCommand):
    def handle(self, *args, **options):
        Article.objects.all().delete()
        Chapter.objects.all().delete()
        id = 0
        for file in glob.glob("programme/chapitre*/*.md"):
            if "!index.md" in file:
                title = open(file,encoding='utf-8').read().split('\n')[0][1:].strip()
                number=file.split('chapitre-')[1].split('\\')[0]
                if slugify(title) == "preface-nous-sommes-pour"  or slugify(title) == "annexes" :
                    Chapter(
                         number= number,
                        slug=slugify(title),
                        entity="chapitre",
                        title=title,
                        id=id,
                        content=strip_tags('\n'.join(open(file,encoding='utf-8').read().split('\n')[1:])),
                    ).save()                    
                else:
                    Chapter(
                            number= number,
                            slug=slugify(title),
                            entity="chapitre",
                            title=title,
                            id= id,
                            content=strip_tags('\n'.join(open(file,encoding='utf-8').read().split('\n')[1:])),
                            main_title = title.split(',', 1)[0],
                            sub_title = title.split(',', 1)[1]

                        ).save()
                print("-------blabla---------")
                print(id," - ", slugify(title), '[ ', number , ' ]')
                print("---------------------")
                id += 1
              
                continue

            chapter_number = file.split('chapitre-')[1].split('\\')[0]
            chapter = Chapter.objects.get(number=chapter_number)
            title = open(file,encoding='utf-8').read().split('\n')[0][1:].strip()
            number= int(file.split('\\')[-1].replace('.md', ''))
            print(id," - ", slugify(title) , '[ ', number , ' ]' )
            Article(
                number=number,
                slug=slugify(title),
                entity="section",
                title=title,
                id=id,
                content=strip_tags('\n'.join(open(file,encoding='utf-8').read().split('\n')[1:])),
                chapter=chapter,
            ).save()
            id +=1
           