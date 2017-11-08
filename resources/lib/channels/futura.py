#-*- coding: utf-8 -*-
import urllib2
import re
import CommonFunctions
common = CommonFunctions 
from resources.lib import utils     
from resources.lib import globalvar

title=['FUTURA Sciences']
img=['futura']
readyForUse=True

url_base='http://www.futura-sciences.com'

def list_shows(channel,folder):
  shows=[]              
    
  filePath=utils.downloadCatalog('http://www.futura-sciences.com/videos/' ,'futuraMain.html',False,{})
  html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
  
  match = re.compile(r'<a class="nav-sections-item-link" href="(.*?)"><h2 class="nav-sections-item-title text-shadow">(.*?)</h2><p class="nav-sections-item-count show-on-hover text-shadow">(.*?)</p></a></article>',re.DOTALL).findall(html)
  for url,title, nb in match:
    shows.append( [channel,url, title + ' (' + nb +')' , '','shows'] )
  
  return shows
      
def list_videos(channel,cat):
  videos=[]
  
  filePath=utils.downloadCatalog(url_base + cat ,'futura%s.html' % cat.replace('/video/','').replace('/',''),False,{})
  html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
  
  prev=re.findall('<link rel="prev" href="(.*?)" />', html)
  if len(prev)==1:
    title='<<Page Precedente'
    videos.append( [channel,prev[0].replace(url_base,''), title , '',{"Title": title},'shows'] )  
    
  match = re.compile(r'</header><a href="(.*?)" class="link-wrapper"><article><h3 class="gamma image-mosaic-title text-shadow">(.*?)</h3></article>',re.DOTALL).findall(html)
  for url,title in match:
    title=utils.formatName(title)
    videos.append( [channel,url, title , '',{"Title": title},'play'] )    
  
  next=re.findall('<link rel="next" href="(.*?)" />', html)
  if len(next)==1:    
    title='Page Suivante>>'
    videos.append( [channel,next[0].replace(url_base,''), title , '',{"Title": title},'shows'] )
     
  return videos 
  
def getVideoURL(channel,idVideo):  
  filePath=utils.downloadCatalog(url_base + idVideo ,'futuravideo.html',True,{})
  html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
  url=da=re.findall('src="http://www.dailymotion.com(.*?)"', html)[0]
  return utils.getDMURL('http://www.dailymotion.com' + url)
  