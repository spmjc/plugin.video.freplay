#-*- coding: utf-8 -*-
import urllib2
import json      
from resources.lib import globalvar
from resources.lib import utils   

title       = ['Wat.tv']
img         = ['wattv']
readyForUse = True

def list_shows(channel,folder):
  shows=[]       
  if folder=='none':   
    filePath = utils.downloadCatalog('http://www.wat.tv/v4/appmobile/index','wattv.json',False)
    jsonFile     = open(filePath).read()
    jsoncat     = json.loads(jsonFile)
    for theme in jsoncat['themes'] :
      shows.append( [channel,theme['link'], theme['name'].encode('utf-8'),'','folder'] ) 
    shows.append( [channel,'http://www.wat.tv/v4/appmobile/channel/mostFollowed', globalvar.LANGUAGE(33040).encode('utf-8'),'','folder'] )
    shows.append( [channel,'http://www.wat.tv/v4/appmobile/channel/recommendation', globalvar.LANGUAGE(33041).encode('utf-8'),'','folder'] ) 
    shows.append( [channel,'http://www.wat.tv/v4/appmobile/channel/popular', globalvar.LANGUAGE(33042).encode('utf-8'),'','folder'] )
    shows.append( [channel,'http://www.wat.tv/v4/appmobile/tops/wat', 'Tops Wat.tv','','shows'] )
    shows.append( [channel,'http://www.wat.tv/v4/appmobile/tops/facebook', 'Tops Facebook','','shows'] )
    shows.append( [channel,'http://www.wat.tv/v4/appmobile/tops/twitter', 'Tops Twitter','','shows'] )
  
  else:
    fileVideos=urllib2.urlopen(folder).read()
    jsonData     = json.loads(fileVideos)
    if 'contents' in jsonData:
      jsonChans=jsonData ['contents']
    else:
      jsonChans=jsonData ['channels']
      
    for chan in jsonChans : 
      if 'channelIcon' in chan:
        img=chan['channelIcon']
      else:             
        img=chan['vignette']
        
      shows.append( [channel,chan['link'].replace('\\',''), chan['title'].encode('utf-8'),img,'shows'] ) 
    
  return shows  
  
def list_videos(channel,show_url):
    videos=[]    
    fileVideos=urllib2.urlopen(show_url).read()
    jsonvid     = json.loads(fileVideos)['results']['contents']
    for video in jsonvid : 
        video_url=''
        id=str(video['id'])
        name=video['title'].encode('utf-8')
        image_url=video['pictures']['normal']
        duration=int(video['duration']) / 60
        views=''
        desc=video['description']
        rating=''
        infoLabels={ "Title": name,"Plot":desc,"Duration": duration}
        videos.append( [channel, id, name, image_url,infoLabels,'play'] )
    return videos   

def getVideoURL(channel,idVideo):
    VideoURL = 'http://wat.tv/get/ipad/'+idVideo+'.m3u8'
    if globalvar.ADDON.getSetting('tf1ForceHD')=='true' and isHD(VideoURL) :
        VideoURL += '?bwmin=2000000'
    return VideoURL   
    
def isHD(VideoURL) :
    m3u8 = utils.get_webcontent(VideoURL)
    if '1280x720' in m3u8 : return True
    else                  : return False