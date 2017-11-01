#-*- coding: utf-8 -*-
import json       
import urllib,urllib2
import resources.lib.utils as utils 
from resources.lib import globalvar  
import re  
import base64    

title       = ['Nat Geo']
img         = ['natgeo']
readyForUse = True

url_Videos='http://www.nationalgeographic.fr/json/video_search/?page=%s&type=undefined'
url_base='http://www.nationalgeographic.fr'
json_video='{"template":"ngpgs/default","country":"FR","site_section_id":"www.nationalgeographic.fr","id":"%s","instance_id":111111}'
url_video='http://players.fichub.com/api/v1/get-player?data=%s&callback=sdkcb_1'

def list_shows(channel,page):  
  shows      = []  
  shows.append([channel,'0', 'Toutes les videos','','shows'])
  return shows
  
def list_videos(channel,page):
  videos=[]     
  
  if page!='0':
    videos.append( [channel,str(int(page)-1), '<<Page Precedente' ,'',{} ,'shows'] )
  
  filePath = utils.downloadCatalog(url_Videos % page, 'natgeo%s.JSON' % page, False, {})
  filPrgm = open(filePath).read()
  jsonParser = json.loads(filPrgm)
  for vid in jsonParser:
    id=vid['field_mpx_guid'].encode('utf-8')
    title=vid['title'].encode('utf-8')
    img=url_base + vid['field_promo_image']
    infoLabels = {"Title": title}
    videos.append( [channel, id , title , img,infoLabels,'play'] )
  videos.append( [channel,str(int(page)+1), 'Page Suivante>>' ,'',{} ,'shows'] )
      
  return videos
                              
def getVideoURL(channel,vidId):

  encoded = base64.b64encode(json_video % vidId)
  encoded=encoded.replace('=','%3D')
  
  filePath=utils.downloadCatalog(url_video % (encoded),'natgeo%s.json' % (vidId),False,{}) 
  txt=open(filePath).read()
  
  url=re.findall('releaseUrl =(.*?);', txt)[0]
  url='http:' + url.replace('\u0022','').replace('\u0026','&').replace('\/','/').replace(' ','').encode('utf-8')
  
  filePath=utils.downloadCatalog(url,'natgeo%s.txt' % (vidId),False,{}) 
  txt=open(filePath).read()
  
  url=re.findall('<video src="(.*?)"', txt)[0]
  
  return url