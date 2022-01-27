import glob, os

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ids', nargs='+', type=str)
        parser.add_argument(
            '--rebuild',
            action='store_true',
            help='Regénérer les visuels',
        )


    def handle(self, *args, **options):

        couleurs = [
            ('#ed8f0e','#ffd397'), #1
            ('#32bf7c','#a9e7c9'), #2
            ('#f06e6e','#ffc7c7'), #3
            ('#412883','#aa9ec9'), #4
            ('#679ae7','#c0d6f7ff'), #5
        ]

        import requests
        import csv
        import io
        response = requests.get('https://docs.google.com/spreadsheet/ccc?key=1NBkcDOXTXGwajAWpnueTUzihJ1z_j2ydD3dO6-iuA-k&output=csv')
        assert response.status_code == 200, 'Wrong status code'
        csvfile = io.StringIO(response.content.decode('utf8'))
        csvfile.readline()
        reader = csv.DictReader(csvfile)

        import hashlib
        import json

        mesures_dict = {}
        with open('generation_visuels/sections.json','r') as f:
            sections_dict = json.loads(f.read())

        mesures = []
        chapitres = []
        sections = []

        partie = ""
        npartie = 0
        chapitre = ""
        nchapitre = 0
        section = ""
        nsection = 0
        nmesure = 0
        for row in reader:
            if row['PARTIE']!= partie:
                partie = row['PARTIE']
                npartie += 1
                print(npartie,partie)
            if row['CHAPITRE'].strip() and row['CHAPITRE'].strip() != chapitre:
                chapitre = row['CHAPITRE'].strip()
                nchapitre += 1
                chapitres.append((npartie,partie,nchapitre,chapitre.split(':')[1].strip()))
            if row['SECTION N°'] and row['SECTION N°'] != str(nsection):
                section = row['SECTION'].strip()
                nsection += 1
                if str(nsection) != row['SECTION N°']:
                    print('PB',row)
                    exit()

                sec = [npartie,partie,nchapitre,chapitre.split(':')[1].strip(),nsection,section,0]
                hash = hashlib.md5(json.dumps(sec).encode('utf8')).hexdigest()
                sec.append(hash!=sections_dict.get('c{c}s{s}'.format(c=nchapitre,s=nsection),{'hash':''})['hash'])
                sec.append(hash)
                sections.append(sec)
            if row['MESURE']:
                nmesure += 1
                if str(nmesure) != row['MESURE N°']:
                    print('PB',nmesure,row)
                    
                mes = [npartie,partie,nchapitre,chapitre,nsection,section,row['MESURE N°'],row['MESURE'],row['MESURE CLEF']=='OUI',0]
                hash = hashlib.md5(json.dumps(mes).encode('utf8')).hexdigest()
                mes.append(hash!=mesures_dict.get('s{s}m{m}'.format(s=nsection,m=nmesure),{'hash':''})['hash'])
                mes.append(hash)
                mesures.append(mes)

        import re
        import os
        sections_dict = dict(('c{c}s{s}'.format(c=nchapitre,s=nsection),dict(shortlink='c{c}s{s}'.format(c=nchapitre,s=nsection),npartie=npartie,partie=partie,nchapitre=nchapitre,chapitre=chapitre,nsection=nsection,section=section,adjust=adjust,hash=hash)) for npartie,partie,nchapitre,chapitre,nsection,section,adjust,new,hash in sections)
        import json
        with open('generation_visuels/sections.json','w') as f:
            f.write(json.dumps(sections_dict))

        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

        soptions = webdriver.ChromeOptions()
        soptions.add_argument("--no-sandbox")
        soptions.add_argument("--disable-gpu")
        soptions.add_argument("--window-size=1400,1000")
        soptions.add_argument("--disable-dev-shm-usage")
        soptions.add_argument("--headless")
        soptions.add_argument('--allow-running-insecure-content')
        soptions.add_argument('--ignore-certificate-errors')


        driver = webdriver.Remote(
                            command_executor='http://selenium-hub:4444/wd/hub',   desired_capabilities={'browserName': 'chrome', 'javascriptEnabled': True}, options=soptions)



        import os
        import time
        import random
        import socket

        ip = socket.gethostbyname(socket.gethostname())


        for npartie,partie,nchapitre,chapitre,nsection,section,adjust,new,hash in sections:
            if not 'all' in options['ids'] and not 'sections' in optins['ids'] and options['ids'] and not "s{n}".format(n=nsection) in options['ids']:
                continue
            if new==False:
                continue
            name = "c{c}s{s}".format(c=nchapitre,s=nsection)
            basepath = os.path.join('core','static','visuels')
            imgpath = os.path.join(basepath,name+'.png')
            print(imgpath)
            driver.get('http://'+ip+':8000/visuel/'+name)
            time.sleep(1)
            driver.find_element(By.ID, 'mesure').screenshot(imgpath)

        driver.quit()
        exit()

        for v in ('','_alt'):
            for npartie,partie,nchapitre,chapitre,nsection,section,nmesure,mesure,cle,adjust in mesures:
                name = "s{s}m{m}".format(s=nsection,m=nmesure)
                mesure = re.sub(r'(\*)([^\*]+)\1',r'<span class="highlight">\2</span>',mesure)
                background = ("mc" if cle else "m") + 'P{n}{v}.png'.format(n=npartie,v=v)
                html_content = mesure_template.render(adjust=adjust,background=background,cle=cle,titre=section, titre_numero=nsection,couleurs=couleurs[npartie-1],mesure=mesure,shortlink=name)

                with open('visuels/html/'+name+v+'.html','w') as f:
                    f.write(html_content)
                driver.get('file:///home/olivier/devs/laecV2/gen/visuels/html/'+name+v+'.html')
                time.sleep(1)
                driver.find_element(By.ID, 'mesure').screenshot('visuels/png/Mesures/'+name+v+'.png')
























        driver.quit()
