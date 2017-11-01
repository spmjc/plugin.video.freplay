#-*- coding: utf-8 -*-
import json       
import urllib,urllib2
import resources.lib.utils as utils 
from resources.lib import globalvar  
import re        

title       = ['VTele']
img         = ['vtele']
readyForUse = True

url_themes='http://api.noovo.ca/api/v1/themes'
url_episodes='http://api.noovo.ca/api/v1/search/videos?limit=199&subThemes=%s'
url_video='https://noovo.ca/videos/%s'
url_video_json='https://edge.api.brightcove.com/playback/v1/accounts/%s/videos/%s' 

def list_shows(channel,folder):  
  shows      = []  
  
  if folder == 'none':
    filePath = utils.downloadCatalog(url_themes, 'VTELE.JSON', False, {})
    filPrgm = open(filePath).read()
    jsonParser = json.loads(filPrgm)
    for em in jsonParser['data']['results']:
      shows.append( [channel,em['slug'], em['title'].encode('utf-8'),em['header']['url-list'],'folder'] )
  else:
    filePath = utils.downloadCatalog(url_themes, 'VTELE.JSON', False, {})
    filPrgm = open(filePath).read()
    jsonParser = json.loads(filPrgm)
    for em in jsonParser['data']['results']:
      if em['slug']==folder:
        for sub in em['subthemes']:
          shows.append( [channel,sub['id'], sub['title'].encode('utf-8'),'','shows'] )
      
  return shows

def list_videos(channel,id):
  videos=[]
  
  filePath = utils.downloadCatalog(url_episodes % id, 'VTELE%s.XML' % id, False, {})
  filPrgm = open(filePath).read()
  jsonParser = json.loads(filPrgm)
  for ep in jsonParser['data']['results']:
    if 'id' in ep['episode']:
      slug=ep['slug']
      show=ep['episode']['season']['show']['title'] 
      season=ep['episode']['season']['title']
      title=ep['title']
      title=(show + ' - ' + season + ' - ' + title).encode('utf-8')
      description=ep['description'].encode('utf-8')
      duration=ep['duration']
      img=ep['image']['url-list']
      infoLabels = {
              "Title": title,
              "Plot": description,
              'Duration': duration}
      videos.append( [channel, slug , title , '',infoLabels,'play'] )
  return videos

def getVideoURL(channel,slug):
  filePath = utils.downloadCatalog(url_video % slug, 'vtelevideo.html', True, {})
  html = open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace("\n", "")
  da=re.findall('data-account="(.*?)"', html)[0]
  vid=re.findall('data-video-id="(.*?)"', html)[0]
  
  filePath = utils.downloadCatalog(url_video_json % (da,vid), 'VTELE%s.json' % vid, True, {}, {'Accept':'application/json;pk=BCpkADawqM145C2ijKGLTnwjc7d61ZlONDwMyE_8xJ-8UVM6hjWtMzw5gMSTc3xniaSHQAJ7Mj23t6tajoj7IQdwFuqpwLac1Gm0L6F11zSTeSWfsOW2KF83_vo'})
  filPrgm = open(filePath).read()
  print filPrgm 
  jsonParser = json.loads(filPrgm)
  print len(jsonParser['sources'])
  for i in range(len(jsonParser['sources'])) :
    src=jsonParser['sources'][i]
    if ('type') in src:
      if(src['type']=='application/x-mpegURL'):
        return src['src']