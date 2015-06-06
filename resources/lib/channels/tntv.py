#-*- coding: utf-8 -*-
from resources.lib import utils   
from resources.lib import globalvar 
import json

title=['TNTV']
img=['tntv']
readyForUse=True

nbItems=25

def list_shows(channel,param):  
  shows=[]
           
  shows.append( [channel,'1', "Mag Actu".encode('utf-8'),'','shows'] ) 
  shows.append( [channel,'2', "Culture".encode('utf-8'),'','shows'] )
  shows.append( [channel,'3', "Sport".encode('utf-8'),'','shows'] )
  shows.append( [channel,'4', "Divertissement".encode('utf-8'),'','shows'] )
    
  return shows
  
def list_videos(channel,show):
  videos=[] 
  
  filePath=utils.downloadCatalog('http://tntv.goodbarber.com/apiv3/getItemsByCategorie/6833037/%s/1/%s/' % (show,nbItems),'tntv%s.json' % (show),False)
  
  jsonParser= json.loads(open(filePath).read())
  for item in jsonParser['items'] :
    videoId=str(item['id'])   
    title=item['title'].encode('utf-8')      
    icon=item['smallThumbnail'].encode('utf-8')
    desc=item['summary'].encode('utf-8')
    duration=item['length']/60
    infoLabels={ "Title": title,"Plot":desc,"Duration": duration} 
    videos.append( [channel, show+'-'+videoId, title, icon,infoLabels,'play'] )     
    
  return videos
  
def getVideoURL(channel,video_id):
  urlVideo=''
  t=video_id.split('-')
  print t[0]
  print t[1]
  filePath=utils.downloadCatalog('http://tntv.goodbarber.com/apiv3/getItemsByCategorie/6833037/%s/1/%s/' % (t[0],nbItems),'tntv%s.json' % (t[0]),False)
  
  jsonParser= json.loads(open(filePath).read())
  for item in jsonParser['items'] :
    if t[1]==str(item['id']):
      urlVideo=item['videoUrls'][globalvar.ADDON.getSetting('tntvQuality')]
         
  return urlVideo