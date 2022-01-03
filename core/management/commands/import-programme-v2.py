import glob, os

from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags
from core.models import Chapter, Article, UrlData, Part
class Command(BaseCommand):
    def handle(self, *args, **options):
        Article.objects.all().delete()
        Chapter.objects.all().delete()
        UrlData.objects.all().delete()
        id = 0
        for file in sorted(glob.glob("programme-v2/partie-*/*")):         
            if "!index.md" in file:               
                part_title = open(file,encoding='utf-8').read().split('\n')[0].strip()
                print(part_title)
                part_number=int(file.split('partie-')[1].split(os.path.sep)[0])
                content =strip_tags('\n'.join(open(file,encoding='utf-8').read().split('\n')[1:]))
                Part(
                        number= part_number,
                        slug=slugify(part_title),
                        entity="partie",
                        title=part_title,
                        id=id,
                        main_title=part_title,
                        content= strip_tags('\n'.join(open(file,encoding='utf-8').read().split('\n')[1:])),                                    
                ).save()
                UrlData(url="/partie/"+str(part_number)+"/"+slugify(part_title),
                slug="/p"+str(part_number) 
                ).save()

                       
                id += 1              
                continue
            for subfile in sorted(glob.glob(file+"\\*" )):              
                title = open(subfile,encoding='utf-8').read().split('\n')[0].strip()
                number=int(subfile.split('chapitre-')[1].split(os.path.sep)[0])
               
                if "!index.md" in subfile:                  
                    part = Part.objects.get(number=part_number)
                    Chapter(
                            number= number,
                            slug=slugify(title),
                            entity="chapitre",
                            title=title,
                            id= id,
                            content=strip_tags('\n'.join(open(subfile,encoding='utf-8').read().split('\n')[1:])),
                            text ='\n'.join(open(subfile,encoding='utf-8').read().split('\n')[1:]),                       
                            main_title = title.split(',', 1)[0],
                            sub_title = part_title,
                            part = part
                        ).save()                   
                    UrlData(url="chapitre/"+str(number)+"/"+slugify(title),
                    slug="/c"+str(number) 
                    ).save()
                    id += 1              
                    continue
                chapter_number = int(subfile.split('chapitre-')[1].split(os.path.sep)[0])
             
                chapter = Chapter.objects.get(number=chapter_number)
                title = open(subfile,encoding='utf-8').read().split('\n')[0].strip()
                number= int(subfile.split(os.path.sep)[-1].replace('.md', ''))
                Article(
                    number=number,
                    slug=slugify(title),
                    entity="section",
                    title=title,
                    id=id,
                    content=strip_tags('\n'.join(open(subfile,encoding='utf-8').read().split('\n')[1:])),
                    text='\n'.join(open(subfile,encoding='utf-8').read().split('\n')[1:]),
                    chapter=chapter,
                ).save()
               
                UrlData(url="/section/"+str(number)+"/"+slugify(title),
                        slug="/s"+str(number) 
                        ).save()
                id +=1            