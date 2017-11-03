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
    infoLabels = {"Title": title.encode('utf-8')}
    videos.append( [channel, url.encode('utf-8') , title.encode('utf-8') , img.encode('utf-8'),infoLabels,'play'] )
    
  return videos
  
def getVideoURL(channel,url):
  url='http://rmcdecouverte.bfmtv.com/mediaplayer-replay/?id=16112&title=CONSTRUIRE%20L%27IMPOSSIBLE%20:LE%20CANAL%20DE%20PANAMA'
  filePath = utils.downloadCatalog(url, 'rmcd.html', True, {})
  html = open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace("\n", "")
  da=re.findall('data-account="(.*?)"', html)[0]
  vid=re.findall('data-video-id="(.*?)"', html)[0]
  
  filePath = utils.downloadCatalog(url_video_json % (da,vid), 'rmcd%s.json' % vid, True, {}, {'Accept':'application/json;pk=BCpkADawqM145C2ijKGLTnwjc7d61ZlONDwMyE_8xJ-8UVM6hjWtMzw5gMSTc3xniaSHQAJ7Mj23t6tajoj7IQdwFuqpwLac1Gm0L6F11zSTeSWfsOW2KF83_vo'})
  filPrgm = open(filePath).read()
  print filPrgm
  jsonParser = json.loads(filPrgm)
  
  for i in range(len(jsonParser['sources'])) :
    src=jsonParser['sources'][i]
    if ('type') in src:
      if(src['type']=='application/x-mpegURL'):
        return src['src']