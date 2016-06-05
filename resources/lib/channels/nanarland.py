#-*- coding: utf-8 -*-
import urllib2
import re
import CommonFunctions
import base64
common = CommonFunctions 
from resources.lib import utils


title=['Nanarland']
img=['nanarland']

readyForUse=True

url_root = 'http://www.nanarland.com/'

def list_shows(channel,folder):

    shows=[]
    
    filePath=utils.downloadCatalog(url_root+'video.php',channel + '.html',False,{})    
    html=open(filePath).read()

    if folder=='none':      
        match = re.compile(r'<div class="list-cat-item">(.*?)<a href="(.*?)">(.*?)<img src="(.*?)" alt=(.*?)<span class="list-cat-item-title">(.*?)</span>',re.DOTALL).findall(html)
        if match:
            for empty, link, empty2, img, empty3, title  in match:
              link = url_root+link
              img = url_root+img
              shows.append( [channel,link+'|'+title, title , img,'shows'] )
                     
    return shows



def list_videos(channel,show): 
    
    videos=[]
    link = show.split('|')[0]
    title = show.split('|')[1]                                                                               
    filePath=utils.downloadCatalog(link ,channel +'_'+ title +'.html',False,{})  
    html=open(filePath).read()
  
    match = re.compile(r'<div class="video-list-item video-cat-list-item">(.*?)<a href="(.*?)">(.*?)alt="(.*?)" src="(.*?)">(.*?)<span class="video-list-item-info-duree">(.*?):(.*?)</span>',re.DOTALL).findall(html)

    if match:
      for empty1, link, empty2, title, img, empty3, minutes, seconds in match:
        link = url_root+link
        img = url_root+img
        duration = int(minutes)*60+int(seconds)
        infoLabels={ "Title": title , "Duration": duration,}
        videos.append( [channel, link, title, img,infoLabels,'play'] ) 

    return videos



def getVideoURL(channel,urlPage):
  html=urllib2.urlopen(urlPage).read()
  url = ''
  match = re.compile(r'<source src="(.*?)"></source>',re.DOTALL).findall(html)
  if match:
    url=url_root+match[0]
 
  return url