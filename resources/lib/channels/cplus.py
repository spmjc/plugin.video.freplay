#-*- coding: utf-8 -*-
import urllib,urllib2
import xml.dom.minidom
from resources.lib import utils
import json

title=['Canal +']
img=['cplus']
readyForUse=True

def get_token():  
  filePath=utils.downloadCatalog('http://service.mycanal.fr/authenticate.json/Android_Tab/1.1?highResolution=1','TokenCPlus.json',False,{}) 
  filPrgm=open(filePath).read()
  jsoncat     = json.loads(filPrgm)
  return jsoncat['token']

def list_shows(channel,folder):
    shows=[]
                    
    if folder=='none':    
        filePath=utils.downloadCatalog('http://service.mycanal.fr/page/'+get_token()+'/1595.json','CPLUS.json',False,{})
        filPrgm=open(filePath).read()                       
        jsoncat     = json.loads(filPrgm)
        strates  = jsoncat['strates']
        for strate in strates :
            if strate['type']=='links':
              for content in strate['contents']:  
                shows.append( [channel,content['onClick']['URLPage'].encode('utf-8'), content['onClick']['displayName'].encode('utf-8'),content['URLImage'].encode('utf-8'),'folder'] )
    else:  
        fileName=folder[folder.find('.json')-4:folder.find('.json')+5]
        filePath=utils.downloadCatalog(folder,fileName,False,{})
        filPrgm=open(filePath).read()
        jsoncat     = json.loads(filPrgm)
        strates  = jsoncat['strates']
        for strate in strates :
            if strate['type']=='contentGrid':
              for content in strate['contents']:   
                  shows.append( [channel,content['onClick']['URLPage'].replace(get_token(),'$$TOKEN$$').encode('utf-8'), content['title'].encode('utf-8'),content['URLImage'],'shows'] )
    
    return shows

def getVideoURL(channel,video_URL):
    video_URL=video_URL.replace('$$TOKEN$$',get_token())
    filPrgm=urllib2.urlopen(video_URL).read()
    jsoncat     = json.loads(filPrgm)
    return jsoncat['detail']['informations']['VoD']['videoURL'].encode('utf-8')
    #return 'http:\/\/us-cplus-aka.canal-plus.com\/i\/1509\/14\/nip_NIP_64296_,200k,400k,800k,1500k,.mp4.csmil\/master.m3u8'
    
def search(channel,keyWord):
    return list_shows(channel,keyWord)

def list_videos(channel,show_URL):
    videos=[] 
    
    show_URL=show_URL.replace('$$TOKEN$$',get_token())
    
    url=''
    title=''
    icon=''
    filPrgm=urllib2.urlopen(show_URL).read()
    jsoncat     = json.loads(filPrgm)
    contents={}
    if 'contents' in jsoncat:	
        contents  = jsoncat['contents']
    else:
        strates  = jsoncat['strates']
        for strate in strates:
            if 'title' in strate:
	        if 'contents' in strate:
                    contents  = strate['contents']
                    break
    for content in contents:
	    
        url=content['onClick']['URLPage'].encode('utf-8').replace(get_token(),'$$TOKEN$$')
        if 'title' in content:
            title=content['title'].encode('utf-8')
        if 'subtitle' in content:
            title+=' - ' + content['subtitle'].encode('utf-8')
        icon=content['URLImage'].encode('utf-8')
        infoLabels={ "Title": title} 
        videos.append( [channel, url, title, icon,infoLabels,'play'] )
             
    return videos

