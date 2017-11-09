#-*- coding: utf-8 -*-              
import json       
import urllib2
import re
import CommonFunctions
common = CommonFunctions 
from resources.lib import utils     
from resources.lib import globalvar

title=['Les Docus']
img=['lesdocus']
readyForUse=True

categ='{"categories":[{"id":"","name":"Derniers Ajouts","sub":[]},{"id":"arts","name":"Arts","sub":[{"id":"architecture","name":"Architecture"},{"id":"cinema","name":"Cinema"},{"id":"dessin","name":"Dessin"},{"id":"litterature","name":"Litterature"},{"id":"musique","name":"Musique"},{"id":"peinture","name":"Peinture"},{"id":"sculpture","name":"Sculpture"}]},{"id":"histoire","name":"Histoire","sub":[{"id":"prehistoire","name":"Prehistoire"},{"id":"antiquite","name":"Antiquite"},{"id":"moyen-age","name":"Moyen Age"},{"id":"temps-modernes","name":"Temps Modernes"},{"id":"temps-revolutionnaires","name":"Temps revolutionnaires"},{"id":"19eme-siecle","name":"19eme siecle"},{"id":"20eme-siecle","name":"20eme siecle"},{"id":"epoque-contemporaine","name":"Epoque contemporaine"}]},{"id":"societe","name":"Societe","sub":[{"id":"argent","name":"Argent"},{"id":"monde","name":"Monde"},{"id":"politique","name":"Politique"},{"id":"sexualite","name":"Sexualite"},{"id":"social","name":"Social"}]},{"id":"sciences","name":"Sciences","sub":[{"id":"astronomie","name":"Astronomie"},{"id":"ecologie","name":"Ecologie"},{"id":"economie","name":"Economie"},{"id":"genetique","name":"Genetique"},{"id":"geographie","name":"Geographie"},{"id":"geologie","name":"Geologie"},{"id":"mathematique","name":"Mathematique"},{"id":"medecine","name":"Medecine"},{"id":"physique","name":"Physique"},{"id":"psychologie","name":"Psychologie"}]},{"id":"technologie","name":"Technologie","sub":[{"id":"aviation","name":"Aviation"},{"id":"informatique","name":"Informatique"},{"id":"marine","name":"Marine"},{"id":"telephonie","name":"Telephonie"}]},{"id":"paranormal","name":"Paranormal","sub":[{"id":"fantomes-et-esprits","name":"Fantomes et Esprits"},{"id":"ovnis-et-extraterrestres","name":"Ovni et Extraterrestres"},{"id":"cryptozoologie","name":"Cryptozoologie"},{"id":"mysteres-et-legendes","name":"Mysteres et Legendes"},{"id":"divers","name":"Divers"}]},{"id":"autres","name":"Autres","sub":[{"id":"animaux","name":"Animaux"},{"id":"gastronomie","name":"Gastronomie"},{"id":"jeux-video","name":"Jeux video"},{"id":"loisirs","name":"Loisirs"},{"id":"metiers","name":"Metiers"},{"id":"militaire","name":"Militaire"},{"id":"nature","name":"Nature"},{"id":"policier","name":"Policier"},{"id":"religion","name":"Religion"},{"id":"sante","name":"Sante"},{"id":"sport","name":"Sport"},{"id":"voyage","name":"Voyage"}]}]}'

def list_shows(channel,folder):
  shows=[]
  
  jsonParser = json.loads(categ)
    
  if folder=='none' :
    for c in jsonParser['categories']:
      if c['id']=='':
        shows.append( [channel,c['id'] + '|1', c['name'] ,'' ,'shows'] )
      else:
        shows.append( [channel,c['id'], c['name'],'' ,'folder'] )
    
  if folder !='none':  
    for c in jsonParser['categories']:
      if c['id']==folder:
        for s in c['sub']:
          shows.append( [channel,'/' + c['id'] + '/' + s['id'] + '|1', s['name'],'' ,'shows'] )
    
  return shows
  
def list_videos(channel,folder):     
  videos=[] 
    
  cat,page=folder.split('|')
  filePath=utils.downloadCatalog('http://www.les-docus.com%s/page/%s/' % (cat,page),'lesdocuslist.html',True,{})
  html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
  
  match = re.compile(r'<a class="(.*?) page-numbers"',re.DOTALL).findall(html)
  prev=False
  next=False
  for item in match:
    prev=('prev' in item or prev)
    next=('next' in item or next)
  
  if prev:
    videos.append( [channel,cat + '|' + str(int(page)-1), '<<Page Precedente' ,'',{}  ,'shows'] )
              
  match = re.compile(r'<div class="post-header"> <a href="(.*?)" title="(.*?)">',re.DOTALL).findall(html)
  for url,title in match: 
    title=utils.formatName(title)  
    infoLabels={ "Title": title}
    videos.append( [channel, url , title , '',infoLabels,'play'] )
  
  if next:
    videos.append( [channel,cat + '|' + str(int(page)+1), 'Page Suivante>>' ,'',{}  ,'shows'] ) 
  
  return videos
  
def getVideoURL(channel,url):
  html=utils.get_webcontent(url).replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')  
  urls=re.findall('<noscript><iframe(.*?)src="(.*?)"', html)
  if(len(urls)==0):
    url=re.findall('<meta itemprop="embedURL" content="(.*?)">', html)[0]
  else:
    if 'vimeo' in url:
      return utils.getVimeoURL(urls[0][1])
    else: 
      return utils.getDMURL(urls[0][1])
      
  return utils.getExtURL(url)