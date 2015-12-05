#-*- coding: utf-8 -*-
import urllib2
import json      
from resources.lib import globalvar
from resources.lib import utils   

title       = ['Wat.tv']
img         = ['wattv']
readyForUse = True

def getToken():
  login=globalvar.ADDON.getSetting('watLogin')
  pwd=globalvar.ADDON.getSetting('watPwd')
  filePath=utils.downloadCatalog('https://www.wat.tv/v4/appmobile/user/authentication','WatAuth.html',False,{'username':login,'password':pwd})    
  jsonFile=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a')
  print jsonFile

def list_shows(channel,folder):
  shows=[]      
  if folder=='none':
    shows.append( [channel,'https://www.wat.tv/v4/appmobile/user/subscriptions/channel', 'My Channels','','folder'] ) 
    shows.append( [channel,'http://www.wat.tv/v4/appmobile/theme/61', 'Replay TV','','folder'] ) 
    shows.append( [channel,'http://www.wat.tv/v4/appmobile/theme/1', 'Musique','','folder'] )   
    shows.append( [channel,'http://www.wat.tv/v4/appmobile/theme/101', 'Humour','','folder'] )  
    shows.append( [channel,'http://www.wat.tv/v4/appmobile/theme/39', 'Cinema','','folder'] )  
    shows.append( [channel,'http://www.wat.tv/v4/appmobile/theme/173', 'Actu','','folder'] )  
    shows.append( [channel,'http://www.wat.tv/v4/appmobile/theme/213', 'Sport','','folder'] )  
    shows.append( [channel,'http://www.wat.tv/v4/appmobile/theme/153', 'Manga','','folder'] )  
    shows.append( [channel,'http://www.wat.tv/v4/appmobile/theme/127', 'Jeux Video','','folder'] )  
    
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
    
    jsonResult=json.loads(fileVideos)['results']           
    if 'previousPage' in jsonResult:
      infoLabels={}
      videos.append( [channel, jsonResult['previousPage'], '<<<', '',infoLabels,'shows'] ) 
    jsonvid     = jsonResult['contents']
    for video in jsonvid : 
        video_url=''
        id=str(video['id'])
        name=video['title'].encode('utf-8')
        image_url=video['pictures']['normal']
        duration=int(video['duration']) / 60          
        desc=video['description']
        rating=''
        infoLabels={ "Title": name,"Plot":desc,"Duration": duration}
        videos.append( [channel, id, name, image_url,infoLabels,'play'] )
    if 'nextPage' in jsonResult:
      infoLabels={}
      videos.append( [channel, jsonResult['nextPage'], '>>>', '',infoLabels,'shows'] )  
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