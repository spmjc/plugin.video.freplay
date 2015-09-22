#-*- coding: utf-8 -*-
import json       
import urllib,urllib2
import resources.lib.utils as utils 
from resources.lib import globalvar          

title       = ['La 1ere','France 2', 'France 3', 'France 4', 'France 5', 'France O']
img         = ['la_1ere' ,'france2','france3','france4','france5','franceo']
readyForUse = True

channelCatalog = 'http://pluzz.webservices.francetelevisions.fr/pluzz/liste/type/replay/nb/1000/chaine/%s'
showInfo       = 'http://webservices.francetelevisions.fr/tools/getInfosOeuvre/v2/?idDiffusion=%s&catalogue=Pluzz'
imgURL         = 'http://refonte.webservices.francetelevisions.fr%s'

def list_shows(channel,folder):
  shows      = []
  uniqueItem = dict()  
  filePath   = utils.downloadCatalog(channelCatalog % (channel),'%s.json' % (channel),False) 
  filPrgm    = open(filePath).read()
  jsonParser = json.loads(filPrgm)   
  emissions  = jsonParser['reponse']['emissions']  
  if folder=='none':           
    for emission in emissions :           
      rubrique = emission['rubrique'].title().encode('utf-8')
      if rubrique not in uniqueItem:
        uniqueItem[rubrique] = rubrique
        shows.append( [channel,rubrique, rubrique,'','folder'] )
  else:
    for emission in emissions :           
      rubrique = emission['rubrique'].title().encode('utf-8')
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
  
def list_videos(channel,folder):
  videos     = []    
  uniqueItem = dict()  
  filePath   = utils.downloadCatalog(channelCatalog % (channel),'%s.json' % (channel),False) 
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
      filPrgm        = urllib2.urlopen(showInfo % (emission['id_diffusion'])).read()
      jsonParserShow = json.loads(filPrgm)
      if jsonParserShow['synopsis']:        
        plot           = jsonParserShow['synopsis'].encode('utf-8')
      date           = jsonParserShow['diffusion']['date_debut']
      if jsonParserShow['real_duration']!=None : 
          duration   = jsonParserShow['real_duration']/60
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
  filPrgm        = urllib2.urlopen(showInfo % (id)).read()
  jsonParser = json.loads(filPrgm)   
  for video in jsonParser['videos']:
    if video['format']==globalvar.ADDON.getSetting('%sQuality' % (channel)):
      url = video['url']
  return url