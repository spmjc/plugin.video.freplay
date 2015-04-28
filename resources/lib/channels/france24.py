#-*- coding: utf-8 -*-
from resources.lib import utils    
from resources.lib import globalvar
import json

title=['France 24']
img=['france24']
readyForUse=True

def list_shows(channel,param):  
  shows=[]
  
  filePath=utils.downloadCatalog('http://api.france24.com/fr/services/json-rpc/emission_list?databases=f24fr&key=XXX&start=0&limit=30&edition_limit=8','France24.json',False) 
  filPrgm=open(filePath).read()
  jsonParser = json.loads(filPrgm)
   
  for item in jsonParser['result']['f24fr']['list'] :
    shows.append( [channel,item['nid'], item['title'].encode('utf-8'),item['image'][0]['original'].encode('utf-8'),'shows'])
    
  return shows
  
def list_videos(channel,show):
  videos=[]
    
  filePath=utils.downloadCatalog('http://api.france24.com/fr/services/json-rpc/emission_list?databases=f24fr&key=XXX&start=0&limit=30&edition_limit=8','France24.json',False) 
  filPrgm=open(filePath).read()
  jsonParser = json.loads(filPrgm)
  
  for item in jsonParser['result']['f24fr']['list'] :
    if item['nid']==show:
      for video in item['editions']['list']:
        url=video['video'][0][globalvar.ADDON.getSetting('france24Quality')].encode('utf-8')
        title=video['title'].encode('utf-8')
        icon=video['image'][0]['original'].encode('utf-8')
        desc=video['intro']
        infoLabels={ "Title": title,"Plot":desc} 
        videos.append( [channel, url, title, icon,infoLabels,'play'] )
             
  return videos

def getVideoURL(channel,video_URL):
  return video_URL 