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
    html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace("\n", "")
    html=' '.join(html.split())
    
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
      html=' '.join(html.split())
      print html
      
      match = re.compile(r'<h2 class="linkProgram-title"> <a href="(.*?)">(.*?)</a> </h2>',re.DOTALL).findall(html)
      print 'rr'
      if match:
        for link,title in match:
          print 'ff'
          title = common.replaceHTMLCodes(title)
          title = title.title()
          shows.append( [channel,link, title.encode("utf-8") , '','shows'] )                           
                     
    return shows           

def list_videos(channel,link): 
    
    videos=[]
    
    filePath=utils.downloadCatalog('http://www.nrj-play.fr' + link,channel + link.replace('/','') +'.html',False,{})    
    html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace("\n", "")
    html=' '.join(html.split())    
    print html
    
    match = re.compile(r'<h3 class="thumbnailReplay-title" itemprop="name"> <a href="(.*?)">(.*?)</a> </h3>',re.DOTALL).findall(html)

    if match:
      for link,title in match:
        title = common.replaceHTMLCodes(title)
        title = title.title()                          
        infoLabels={ "Title": title}
        videos.append( [channel, link , title , '',infoLabels,'play'] )
    else:         
      match = re.compile(r'<meta itemprop="name" content="(.*?)" />',re.DOTALL).findall(html) 
      if match:
        for title in match:
          title = common.replaceHTMLCodes(title)
          title = title.title()                          
          infoLabels={ "Title": title}
          videos.append( [channel, link , title , '',infoLabels,'play'] )
          
    return videos



def getVideoURL(channel,link):

    filePath=utils.downloadCatalog('http://www.nrj-play.fr' + link,channel + link.replace('/','') +'.html',False,{})    
    html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace("\n", "")
    html=' '.join(html.split())    
    print html
      
    match = re.compile(r'<meta itemprop="contentUrl" content="(.*?)" alt="',re.DOTALL).findall(html)
    
    url=match[0]
   
    return url