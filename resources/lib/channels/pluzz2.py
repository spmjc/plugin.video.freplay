#-*- coding: utf-8 -*-
import json       
import resources.lib.utils as utils 
from resources.lib import globalvar          

title       = ['La 1ère','France 2', 'France 3', 'France 4', 'France 5', 'France Ô']
img         = ['la_1ere' ,'france2','france3','france4','france5','franceo']
readyForUse = True

channelCatalog = 'http://pluzz.webservices.francetelevisions.fr/pluzz/liste/type/replay/nb/1000/chaine/%s'
showInfo       = 'http://webservices.francetelevisions.fr/tools/getInfosOeuvre/v2/?idDiffusion=%s&catalogue=Pluzz'
imgURL         = 'http://refonte.webservices.francetelevisions.fr%s'

def list_shows(channel,folder):
  shows      = []
  uniqueItem = dict() 
  if channel == 'la_1ere':
    url_json = channelCatalog % ('')
  else:
    url_json = channelCatalog % (channel)
  filePath   = utils.downloadCatalog(url_json,'%s.json' % (channel),False,{}) 
  filPrgm    = open(filePath).read()
  jsonParser = json.loads(filPrgm)   
  emissions  = jsonParser['reponse']['emissions']  
  if folder=='none':           
    for emission in emissions :           
      rubrique = emission['rubrique'].encode('utf-8')
      chaine_id = emission['chaine_id'].encode('utf-8')
      if channel == "la_1ere":
        if chaine_id == "la_1ere":
          if rubrique not in uniqueItem:
            uniqueItem[rubrique] = rubrique
            shows.append( [channel,rubrique, change_to_nicer_name(rubrique),'','folder'] )
          
      else:
        if rubrique not in uniqueItem:
          uniqueItem[rubrique] = rubrique
          shows.append( [channel,rubrique, change_to_nicer_name(rubrique),'','folder'] )
  else:
    for emission in emissions :           
      rubrique = emission['rubrique'].encode('utf-8')
      chaine_id = emission['chaine_id'].encode('utf-8')
      if channel == "la_1ere":
        if chaine_id == "la_1ere":
          if rubrique==folder:        
            titre = emission['titre_programme'].encode('utf-8')
            if titre!='':      
              id = emission['id_programme'].encode('utf-8')
              if id=='':
                id = emission['id_emission'].encode('utf-8')        
              if id not in uniqueItem:
                uniqueItem[id]=id
                shows.append( [channel,id,titre,imgURL % (emission['image_large']),'shows'] )   
         
      else:
        if rubrique==folder:        
          titre = emission['titre_programme'].encode('utf-8')
          if titre!='':      
            id = emission['id_programme'].encode('utf-8')
            if id=='':
              id = emission['id_emission'].encode('utf-8')        
            if id not in uniqueItem:
              uniqueItem[id]=id
              shows.append( [channel,id,titre,imgURL % (emission['image_large']),'shows'] )     
  return shows


def change_to_nicer_name(original_name):
  Dic = {"france2"              :"France 2",
         "france3"              :"France 3",
         "france4"              :"France 4",
         "france5"              :"France 5",
         "franceo"              :"France Ô",
         "guadeloupe"           :"Guadeloupe 1ère",
         "guyane"               :"Guyane 1ère",
         "martinique"           :"Martinique 1ère",
         "mayotte"              :"Mayotte 1ère",
         "nouvellecaledonie"    :"Nouvelle Calédonie 1ère",
         "polynesie"            :"Polynésie 1ère",
         "reunion"              :"Réunion 1ère",
         "saintpierreetmiquelon":"St-Pierre et Miquelon 1ère",
         "wallisetfutuna"       :"Wallis et Futuna 1ère",
         "sport"                :"Sport",
         "info"                 :"Info",
         "documentaire"         :"Documentaire",
         "seriefiction"         :"Série & fiction",
         "magazine"             :"Magazine",
         "jeunesse"             :"Jeunesse",
         "divertissement"       :"Divertissement",
         "jeu"                  :"Jeu",
         "culture"              :"Culture"
         }
  for key,value in Dic.iteritems():
      if original_name==key : return value
  return original_name

def list_videos(channel,folder):
  videos     = []    
  uniqueItem = dict()  
  filePath   = utils.downloadCatalog(channelCatalog % (channel),'%s.json' % (channel),False,{}) 
  filPrgm    = open(filePath).read()
  jsonParser = json.loads(filPrgm)   
  emissions  = jsonParser['reponse']['emissions']  
  for emission in emissions :     
    titre='' 
    plot=''
    duration='0'     
    id = emission['id_programme'].encode('utf-8')
    if id=='':
      id = emission['id_emission'].encode('utf-8')
    if id==folder: 
      id_diffusion=emission['id_diffusion']  
      filPrgm=utils.get_webcontent(showInfo % (emission['id_diffusion'])) 
      if(filPrgm!=''):
        jsonParserShow = json.loads(filPrgm)
        if jsonParserShow['synopsis']:        
          plot           = jsonParserShow['synopsis'].encode('utf-8')
        date           = jsonParserShow['diffusion']['date_debut']
        if jsonParserShow['real_duration']!=None : 
            duration   = jsonParserShow['real_duration']/50
        if jsonParserShow['titre']:
          titre          = jsonParserShow['titre'].encode('utf-8')
        if jsonParserShow['sous_titre']:
          titre+=' - ' + jsonParserShow['sous_titre'].encode('utf-8')
        image      = imgURL % (jsonParserShow['image'])  
        infoLabels = { "Title": titre,"Plot":plot,"Aired":date,"Duration": duration, "Year":date[6:10]}
        if jsonParserShow['genre']!='':
            infoLabels['Genre']=jsonParserShow['genre'].encode('utf-8')
        videos.append( [channel, id_diffusion, titre, image,infoLabels,'play'] )    
  return videos
  
  
def getVideoURL(channel,id):          
  filPrgm    = utils.get_webcontent(showInfo % (id))
  jsonParser = json.loads(filPrgm)   
  for video in jsonParser['videos']:
    if video['format']==globalvar.ADDON.getSetting('%sQuality' % (channel)):
      url = video['url']
  return url