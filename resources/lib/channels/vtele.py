#-*- coding: utf-8 -*-
import json       
import urllib,urllib2
import resources.lib.utils as utils 
from resources.lib import globalvar          

title       = ['VTele']
img         = ['vtele']
readyForUse = True

urlCatalog = 'http://apps.vtele.ca/api/shows'
videoList       = 'http://apps.vtele.ca/api/shows/%s/videos'
videoDetails         = 'http://api.brightcove.com/services/library?command=find_video_by_id&video_fields=renditions&media_delivery=http&token=2sgr1KCsKKJXcqUFQdti_mXZAhdNB-wCFwCbGW6lz5atwI1QTrElxQ..&video_id=%s'
urlVideo         = 'http://uds.ak.o.brightcove.com/%s'
data = urllib.urlencode({'timestamp' : '1' })
headers = { 'Authorization' : 'Basic bWlyZWdvOlJpT25WLzI0XzhXQy1qUy1AJTklUThSSWIhZCNyd1NF' }

def list_shows(channel,uid):  
  shows      = []  
          
  req = urllib2.Request(urlCatalog, data, headers)
  filPrgm = urllib2.urlopen(req).read()
  jsonParser = json.loads(filPrgm)   
  emissions  = jsonParser['data']
  for emission in emissions :           
    shows.append( [channel,emission['uid'], emission['nom'].encode('utf-8'),'','shows'] )  
  return shows
  
def list_videos(channel,uid):
  videos     = []    
  req = urllib2.Request(videoList % uid, data, headers)
  filPrgm = urllib2.urlopen(req).read()
  print filPrgm
  jsonParser = json.loads(filPrgm)   
  items  = jsonParser['data']
  for item in items : 
    titre=item['titre'].encode('utf-8')   
    description=item['description'].encode('utf-8') 
    dateandtime=item['dateandtime'][:10]   
    idBC=item['idBC']    
    image=item['image'].encode('utf-8')       
    infoLabels = { "Title": titre,"Plot":description,"Aired":dateandtime,"Year":dateandtime[:4]}
    videos.append( [channel, idBC, titre, image,infoLabels,'play'] )    
  return videos    
  
def getVideoURL(channel,idBC):          
  req = urllib2.Request(videoDetails % idBC, data, headers)
  filPrgm = urllib2.urlopen(req).read()
  print filPrgm
  jsonParser = json.loads(filPrgm)   
  renditions= jsonParser['renditions']
  i= len(renditions)-1
  url=renditions[i]['url']
  return url 