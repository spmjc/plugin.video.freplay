#-*- coding: utf-8 -*-
from resources.lib import utils
import re 
import CommonFunctions
common = CommonFunctions   

title       = ['BeCurious TV']
img         = ['becurioustv']
readyForUse = True

def list_shows(channel,folder):
    shows = []
    filePath=utils.downloadCatalog('http://becurioustv.com/' ,'becurioustv.html',False,{})
    html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
    
    match = re.compile(r'<h2><a class="category-link" href="(.*?)"><img class="category-logo" src="(.*?)"> <span>(.*?)</span></a></h2>',re.DOTALL).findall(html)
    for url,img,title in match:
      shows.append( [channel,url, title.encode('utf-8') ,img ,'shows'] )
    return shows
    
def list_videos(channel,folder):  
    
  videos=[]
  filePath=utils.downloadCatalog('http://becurioustv.com' + folder ,'becurious' + folder.replace('/','') + '.html',False,{})
  html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\t', '').replace('\r', '').replace('&#x27;','\'')
  
  match = re.compile(r'<div class="video"> <a href="(.*?)">(.*?)<img(.*?)src="(.*?)"(.*?)<h2>(.*?)</h2>',re.DOTALL).findall(html)
  for url,empty,empty1,img,empty2,title in match:
    infoLabels={ "Title": title.encode('utf-8')}
    videos.append( [channel, url , title.encode('utf-8') , img,infoLabels,'play'] ) 
  
  return videos
  
def getVideoURL(channel,url):
  html=utils.get_webcontent('http://becurioustv.com' + url).replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')  
  url=re.findall('<iframe(.*?)src="(.*?)"(.*?)</iframe>', html)[0][1]
  return utils.getExtURL(url)
