#-*- coding: utf-8 -*-
import json       
import urllib,urllib2
import resources.lib.utils as utils 
from resources.lib import globalvar  
import re  
import base64    

title       = ['Bein Sport']
img         = ['bsport']
readyForUse = True

url_themes='http://api.beinsports.com/dropdowns?reference=replay_show&site=2'
url_videos='http://api.beinsports.com/contents?itemsPerPage=50&type=3&site=2&taxonomy%%5B%%5D=%s&order%%5BpublishedAt%%5D=DESC'

def list_shows(channel,page):  
  shows      = []  
  
  filePath = utils.downloadCatalog(url_themes, 'bsport.JSON', False, {})
  filPrgm = open(filePath).read()
  jsonParser = json.loads(filPrgm)
  
  for item in jsonParser['hydra:member'][0]['dropdownEntries'] :
    id=item['taxonomy']['@id']
    id=id.replace('/taxonomies/','')
    title=item['taxonomy']['name']
    shows.append([channel,id, title,'','shows'])
  return shows
  
def list_videos(channel,id):
  videos=[]
  
  filePath = utils.downloadCatalog(url_videos % id, 'bsport%s.JSON' % id, False, {})
  filPrgm = open(filePath).read()
  jsonParser = json.loads(filPrgm)
  for item in jsonParser['hydra:member']:
    url=item['media'][0]['media']['uri'].encode('utf-8')
    name=item['headline'].encode('utf-8')
    infoLabels = {"Title": name}
    videos.append( [channel, url , name , '',infoLabels,'play'] )
  
  return videos    

def getVideoURL(channel,url):
  return utils.getDMURL(url)