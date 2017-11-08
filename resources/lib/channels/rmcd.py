#-*- coding: utf-8 -*-
import urllib2
import re
import CommonFunctions
common = CommonFunctions 
from resources.lib import utils     
from resources.lib import globalvar 
import json       

title=['RMC Decouverte']
img=['rmcd']
readyForUse=True

url_video_json='https://edge.api.brightcove.com/playback/v1/accounts/%s/videos/%s'

def list_shows(channel,page):  
  shows      = []  
  shows.append([channel,'empty', 'Toutes les videos','','shows'])
  return shows
  
def list_videos(channel,page):
  videos=[]
  filePath=utils.downloadCatalog('http://rmcdecouverte.bfmtv.com/mediaplayer-replay/' ,'rmcd.html',False,{})
  html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
  
  
  match = re.compile(r'<figure class="figure modulx1-5-inside-bloc">(.*?)<a href="(.*?)" title="(.*?)">(.*?)data-original="(.*?)"  alt=',re.DOTALL).findall(html)
  for a,url,title,b,img in match:
    title=utils.formatName(title)
    infoLabels = {"Title": title.encode('utf-8')}
    videos.append( [channel, url.replace('\t','').encode('utf-8') , title.encode('utf-8') , img.encode('utf-8'),infoLabels,'play'] )
    
  return videos
  
def getVideoURL(channel,url):
  url='http://rmcdecouverte.bfmtv.com' + url 
  #http://rmcdecouverte.bfmtv.com/mediaplayer-replay/?id=18118&title=DEVOIR%20D%27ENQUETE%20:LES%20TUEURS%20DU%20BRABANT
  #/mediaplayer-replay/?id=18118&title= 																			DEVOIR D'ENQUETE : 																		LES%20TUEURS%20DU%20BRABANT
  #url='http://rmcdecouverte.bfmtv.com/mediaplayer-replay/?id=16112&title=CONSTRUIRE%20L%27IMPOSSIBLE%20:LE%20CANAL%20DE%20PANAMA'
  return utils.getExtURL(url)