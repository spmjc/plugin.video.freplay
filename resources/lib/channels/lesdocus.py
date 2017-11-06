#-*- coding: utf-8 -*-
import urllib2
import re
import CommonFunctions
common = CommonFunctions 
from resources.lib import utils     
from resources.lib import globalvar

title=['Les Docus']
img=['lesdocus']
readyForUse=True

def list_shows(channel,folder):
  shows=[]
  d = dict()         
  filePath=utils.downloadCatalog('http://www.les-docus.com/','lesdocus.html',False,{})
  html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
  if folder=='none' :
    
    match = re.compile(r'<li id="(.*?)" class="(.*?)menu-item-has-children has-children(.*?)"><a href="(.*?)">(.*?)</a>',re.DOTALL).findall(html)
    for empty1,empty2,empty3,url,title in match:
      if title not in d:
        shows.append( [channel,url, title ,'' ,'folder'] )
        d[title] = title
  if folder !='none':
  
    match = re.compile(r'<li id="(.*?)" class="(.*?)"><a href="(.*?)">(.*?)</a></li>',re.DOTALL).findall(html)
    for empty1,empty2,url,title in match:
      if folder in url and folder != url and url not in d:
        shows.append( [channel,url, title ,'' ,'shows'] )
        d[url] = url
    
  return shows
  
def list_videos(channel,url):     
  videos=[] 
  
  filePath=utils.downloadCatalog(url,'lesdocuslist.html',True,{})
  html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
  print html
  print 'herrrrrre'
  match = re.compile(r'<div class="post-header"> <a href="(.*?)" title="(.*?)">',re.DOTALL).findall(html)
  print len(match)
  for url,title in match:   
    infoLabels={ "Title": title}
    videos.append( [channel, url , title , '',infoLabels,'play'] ) 
  
  return videos
  
def getVideoURL(channel,url):
  html=utils.get_webcontent(url).replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')  
  url=re.findall('<noscript><iframe(.*?)src="(.*?)"', html)[0][1]
  print url
  if 'vimeo' in url:
    return utils.getVimeoURL(url)
  else:
    return utils.getDMURL(url)