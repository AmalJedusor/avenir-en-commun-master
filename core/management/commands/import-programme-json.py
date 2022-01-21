
import glob, os
import json
from turtle import update
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags
from core.models import Chapter, Article, UrlData, Part
import markdown_to_json.scripts.md_to_json as md_to_json

from core.management.md_to_json import jsonify_markdown

class Command(BaseCommand):
    def handle(self, *args, **options):
        id = 0
        for file in sorted(glob.glob("programme-json/partie-*/*")):         
            if "!index.md" in file:   
                # explication de la partie

             
                 
                output_part = json.loads(jsonify_markdown(file,None).encode('utf8'))

               
                if "Forewords" in output_part:  
                    forewords = output_part["Forewords"]          
                    part_number=int(file.split('partie-')[1].split(os.path.sep)[0])

                    part = Part.objects.get(number = str(part_number))
                    part.forewords = forewords
                    part.save()
                
                 
                print('---------------------------------------------------------')  
                """part_title = open(file,encoding='utf-8').read().split('\n')[0].strip()
                print(part_title)
                
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
"""             
                id += 1              
                continue
            for subfile in sorted(glob.glob(file+"\\*" )): 
                """           
                title = open(subfile,encoding='utf-8').read().split('\n')[0].strip()
                number=int(subfile.split('chapitre-')[1].split(os.path.sep)[0])
               """
             
               
                if "!index.md" in subfile:
                    c = os.popen('.\markdown_to_json\scripts\md_to_json.py ' + subfile).read()
                    
                    output_chap = json.loads(str(c))
                    print(output_chap["Titre"])
                    print('---------------------------------------------------------')
                # explication du chapitre
                    """     
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
                    id += 1 """
                    continue
                # section
                s = os.popen('.\markdown_to_json\scripts\md_to_json.py ' + subfile).read()
                s = s.replace('None','null')
       
                output = json.loads(str(s))
                chapter_number = int(subfile.split('chapitre-')[1].split(os.path.sep)[0])
                number= int(subfile.split(os.path.sep)[-1].replace('.md', ''))
               
                title = output["Titre"]
                entity="section"                
               
                asavoir = ""
                if "A_Savoir" in output:
                    asavoir = output["A_Savoir"]          
                   
                    article = Article.objects.get(number = str(number))
                 
                    article.asavoir = asavoir
                    article.save() 
                if "Mesures" in output: 
                   
                    measures = output["Mesures"]          
                  
                    article = Article.objects.get(number = str(number))
                    
                    article.measures = str(measures )
                    article.save()
                if "Forewords" in output:  
                    forewords = output["Forewords"]          
            
                    article = Article.objects.get(number = str(number))
                  
                    article.forewords = forewords
                    article.save()
                if "Cle" in output:  
                    key = output["Cle"]          
            
                    article = Article.objects.get(number = str(number))
                  
                    article.key = key
                    article.save()    
              
             