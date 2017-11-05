#-*- coding: utf-8 -*-
import resources.lib.utils as utils 
import simplejson as json    
import re, urllib
from resources.lib import globalvar 

title       = ['L\'Equipe.fr']
img         = ['lequipefr']
readyForUse = True

def list_shows(channel,param):  
  shows      = []           
  jsonFile   = utils.get_webcontent('https://www.lequipe.fr/equipehd/applis/filtres/videosfiltres.json')
  jsonParser = json.loads(jsonFile)
  for item in jsonParser['filtres_vod']:
    if 'missions' in item['titre']:
      for filter in item['filters']:
        shows.append( [channel,filter['filters'], filter['titre'].encode('utf-8'),'','shows'] )
  return shows
  
def list_videos(channel,show_url):
  videos     = []  
  jsonFile   = utils.get_webcontent(show_url)
  jsonParser = json.loads(jsonFile)
  for video in jsonParser['videos'] :
    video_id   = video['lien_dm'].split('://')[1]   
    title      = video['titre'].encode('utf-8')      
    icon       = video['src_tablette_retina'] + '.jpg'
    infoLabels = {"Title": title} 
    videos.append([channel,video_id,title,icon,infoLabels,'play'])     
  return videos

def getVideoURL(channel,video_id):
    web_url  = 'http://www.dailymotion.com/embed/video/%s' % video_id
    return utils.getDMURL(web_url)
 