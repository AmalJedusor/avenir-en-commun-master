import glob, os

from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags
from core.models import Chapter, Article, UrlData, Part, Measure

def build_nav_tree():
    nav = [dict(id=p.id, entity="part") for p in Part.objects.all()]

    nav += [ dict(id=c.id, entity="chapter") for c in Chapter.objects.all()]
    nav += [ dict(id=a.id, entity="section") for a in Article.objects.all()]
    nav.sort(key=lambda x:int(x['id']))

    def get_next(nav,i):
        i += 1
        while i<len(nav) and nav[i]['entity']=='chapter':
            i += 1
        return dict(next_id=i,next_entity=nav[i]['entity']) if i<len(nav) else dict(next_id = None,next_entity = None)

    def get_prev(nav,i):
        i -= 1
        while i>=0 and nav[i]['entity']!='section':
            i -= 1
        return dict(prev_id=i,prev_entity=nav[i]['entity']) if i>=0 else dict(prev_id = None,prev_entity = None)

    for i,n in enumerate(nav):
        n.update(get_next(nav,i))
        n.update(get_prev(nav,i))

    #logging.warning(nav)
    import json
    import os
    with open(os.path.join('core','data','navtree.json'),'w') as f:
        f.write(json.dumps(nav))


class Command(BaseCommand):
    def handle(self, *args, **options):
        Measure.objects.all().delete()
        UrlData.objects.all().delete()
        Article.objects.all().delete()
        Chapter.objects.all().delete()
        Part.objects.all().delete()

        def make_searchable(s):
            return s.replace('’',"'")

        id = 0
        last_elt = None
        for file in sorted(glob.glob("programme-v2/partie-*/*")):
            if "!index.md" in file:
                part_title = open(file,encoding='utf-8').read().split('\n')[0].strip()
                print(part_title)
                part_number=int(file.split('partie-')[1].split(os.path.sep)[0])
                content =strip_tags('\n'.join(open(file,encoding='utf-8').read().split('\n')[1:]))


                if last_elt:
                    last_elt.nav_suiv_id = id
                    last_elt.nav_suiv_type = "partie"
                    last_elt.save()

                nav_last_elt = Part(
                        number= part_number,
                        slug=slugify(part_title),
                        entity="partie",
                        title=make_searchable(part_title),
                        id=id,
                        main_title=part_title,
                        content= make_searchable(strip_tags('\n'.join(open(file,encoding='utf-8').read().split('\n')[1:]))),
                        nav_prec_id = nav_last_elt.id if nav_last_elt else None,
                        nav_prec_type = nav_last_elt.entity if nav_last_elt else None,
                )

                last_elt = nav_last_elt
                last_elt.save()

                UrlData(url="/partie/"+str(part_number)+"/"+slugify(part_title),
                slug="/p"+str(part_number) +"/"
                ).save()
                id += 1
                continue
            for subfile in sorted(glob.glob(file+os.path.sep+"*" )):
                title = open(subfile,encoding='utf-8').read().split('\n')[0].strip()
                number=int(subfile.split('chapitre-')[1].split(os.path.sep)[0])
                print(title)
                if "!index.md" in subfile:
                    part = Part.objects.get(number=part_number)

                    last_elt = Chapter(
                            number= number,
                            slug=slugify(title),
                            entity="chapitre",
                            title=make_searchable(title),
                            part_number=part_number,
                            id= id,
                            content=make_searchable(strip_tags('\n'.join(open(subfile,encoding='utf-8').read().split('\n')[1:]))),
                            text ='\n'.join(open(subfile,encoding='utf-8').read().split('\n')[1:]),
                            main_title = title.split(',', 1)[0],
                            sub_title = part_title,
                            part = part,
                            nav_prec_id = nav_last_elt.id if nav_last_elt else None,
                            nav_prec_type = nav_last_elt.entity if nav_last_elt else None,
                        )

                    last_elt.save()

                    UrlData(url="/chapitre/"+str(number)+"/"+slugify(title),
                    slug="/c"+str(number) +"/"
                    ).save()
                    id += 1
                    continue
                chapter_number = int(subfile.split('chapitre-')[1].split(os.path.sep)[0])

                chapter = Chapter.objects.get(number=chapter_number)
                title = open(subfile,encoding='utf-8').read().split('\n')[0].strip()
                number= int(subfile.split(os.path.sep)[-1].replace('.md', ''))

                if last_elt:
                    last_elt.nav_suiv_id = id
                    last_elt.nav_suiv_type = "section"
                    last_elt.save()

                nav_last_elt = Article(
                    number=number,
                    slug=slugify(title),
                    entity="section",
                    title=make_searchable(title),
                    part_number=part_number,
                    id=id,
                    content = make_searchable(strip_tags('\n'.join(open(subfile,encoding='utf-8').read().split('\n')[1:]))),
                    text='\n'.join(open(subfile,encoding='utf-8').read().split('\n')[1:]),
                    chapter=chapter,
                    nav_prec_id = nav_last_elt.id if nav_last_elt else None,
                    nav_prec_type = nav_last_elt.entity if nav_last_elt else None,
                )

                last_elt = nav_last_elt
                nav_last_elt.save()

                UrlData(url="/section/"+str(number)+"/"+slugify(title),
                        slug="/s"+str(number)+"/"
                        ).save()
                id +=1

        build_nav_tree()
