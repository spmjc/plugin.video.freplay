#-*- coding: utf-8 -*-
import urllib2
import re
import CommonFunctions
import base64
common = CommonFunctions 
from resources.lib import utils

title=['NRJ12','Chérie 25']
img=['nrj12','cherie25']

readyForUse=True

def list_shows(channel,folder):

    shows=[]
    
    filePath=utils.downloadCatalog('http://www.nrj-play.fr/%s/replay' % channel,channel + '.html',False,{})    
    html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a')

    if folder=='none':      
        match = re.compile(r'<li class="subNav-menu-item">(.*?)<a href="(.*?)" class=(.*?)>(.*?)</a>',re.DOTALL).findall(html)
            
        if match:
            for empty,link,empty2,title in match:
                if 'active' not in empty2:
                  shows.append( [channel,link, title , '','folder'] )
    else:                                                                                     
      print 'http://www.nrj-play.fr%s' % (folder)
      filePath=utils.downloadCatalog('http://www.nrj-play.fr%s' % (folder),channel + folder +'.html',False,{})  
      html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace("\n", "")
      
      match = re.compile(r'<div class="linkProgram-infos">(.*?)<a href="(.*?)" class="linkProgram-thumbnail embed-responsive embed-responsive-16by9">(.*?)<img src="(.*?)" class="program-img embed-responsive-item" alt="(.*?)"',re.DOTALL).findall(html)
      if match:
        for empty,link,empty2,img,title in match:
          shows.append( [channel,link, title.encode("utf-8") , img,'shows'] )                           
                     
    return shows


def getVideoURL(channel,urlPage):
  html=urllib2.urlopen(urlPage).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', 'a')
  
  match = re.compile(r'<link itemprop="contentUrl" href="(.*?)" />',re.DOTALL).findall(html)
  if not match:
    print 'hi'
    match = re.compile(r'<meta itemprop="contentUrl" content="(.*?)" alt="',re.DOTALL).findall(html)
  
  url=match[0]
  
  
  return url

def list_videos(channel,show): 
    
    videos=[]  
    full_url='http://www.nrj-play.fr' + show
    print full_url                                            

    opener = urllib2.build_opener()
    f = opener.open(full_url)
    full_url= f.url
    
    html=urllib2.urlopen(full_url).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', '')    
    
    k = full_url.rfind("/")
    base_url= full_url[:k+1]   
    print base_url                
    
    match = re.compile(r'<img class="itemprop" itemprop="thumbnailUrl" src="(.*?)" alt="(.*?)" />',re.DOTALL).findall(html)
    for img,title in match:          
      infoLabels={ "Title": title}
      videos.append( [channel, full_url, title, img,infoLabels,'play'] )
    
    match = re.compile(r'<div class="col-md-4">(.*?)<a href="(.*?)">(.*?)src="(.*?)" />(.*?)<h3><img src="(.*?)/>(.*?)</h3>',re.DOTALL).findall(html)
    for empty,link,empty2,img,empty3,empty4,title in match:          
      infoLabels={ "Title": title}
      videos.append( [channel, base_url + link, title, img,infoLabels,'play'] )
    
    match = re.compile(r'<div class="thumbnail-infos">(.*?)<a href="(.*?)" class="thumbnail-visual embed-responsive embed-responsive-16by9">(.*?)src="(.*?)" class="thumbnail-img embed-responsive-item" alt="(.*?)"/>',re.DOTALL).findall(html)
    for empty,link,empty2,img,title in match:          
      infoLabels={ "Title": title}
      videos.append( [channel, 'http://www.nrj-play.fr' + link, title, img,infoLabels,'play'] )  
    
      
    return videos