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
        for empty1,link,empty2,img,title in match:
          title = common.replaceHTMLCodes(title)
          title = title.capitalize()
          shows.append( [channel,link, title.encode("utf-8") , img,'shows'] )                           
                     
    return shows



def list_videos(channel,show): 
    
    videos=[]

    full_url='http://www.nrj-play.fr' + show

    opener = urllib2.build_opener()
    f = opener.open(full_url)
    full_url= f.url
    
    html=urllib2.urlopen(full_url).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', '')    
    
    k = full_url.rfind("/")
    base_url= full_url[:k+1]   
    print base_url

    d=dict()

 

    match = re.compile(r'<img class="itemprop" itemprop="thumbnailUrl" src="(.*?)" alt="(.*?)"/>',re.DOTALL).findall(html)
    for img,title, empty, desc in match:
      title = common.replaceHTMLCodes(title)
      title = title.capitalize()        
      if title not in d:
        infoLabels={ "Title": title}
        videos.append( [channel, full_url, title, img,infoLabels,'play'] )
        d[title] = title 
    
    # Pour les anges de NRJ12 ...
    match = re.compile(r'<div class="col-md-4">(.*?)<a href="(.*?)">(.*?)src="(.*?)" />(.*?)Le (.*?) -(.*?)<h3><img src="(.*?)/>(.*?)</h3>',re.DOTALL).findall(html)
    for empty,link,empty2,img,empty3, date, empty4, empty5,title in match:          
      title = common.replaceHTMLCodes(title)
      title = title.capitalize()
      if title not in d:
        infoLabels={ "Title": title, "Aired":date}
        videos.append( [channel, base_url + link, title, img,infoLabels,'play'] )
        d[title] = title 
    
    # S'il y a plusieurs vid?os pour ce programme
    match = re.compile(r'<div class="thumbnail-infos">(.*?)<a href="(.*?)" class="thumbnail-visual embed-responsive embed-responsive-16by9">(.*?)src="(.*?)" class="thumbnail-img embed-responsive-item" alt="(.*?)"/>(.*?)class="thumbnail-time">Le (.*?)/(.*?)/(.*?)</time>',re.DOTALL).findall(html)
    for empty,link,empty2,img,title, empty3, day, mounth, years in match:          
      title = common.replaceHTMLCodes(title)
      title = title.capitalize()
      if title not in d:
        date = day+'/'+mounth+'/'+years 
        infoLabels={ "Title": title, "Aired":date}
        videos.append( [channel, 'http://www.nrj-play.fr' + link, title, img,infoLabels,'play'] )
        d[title] = title 


    # S'il n'y a qu'une seule vid?o pour ce programme
    match = re.compile(r'<meta itemprop="thumbnailUrl" content="(.*?)" alt="(.*?)"/>(.*?)<p>(.*?)</p>',re.DOTALL).findall(html)
    for img, title, empty, desc in match:
      title = common.replaceHTMLCodes(title)
      title = title.capitalize()
      if title not in d:
        desc = common.replaceHTMLCodes(desc.decode('utf-8'))
        infoLabels={ "Title": title, "Plot":desc}
        videos.append( [channel, full_url, title, img,infoLabels,'play'] ) 
        d[title] = title   
      
    return videos



def getVideoURL(channel,urlPage):
  html=urllib2.urlopen(urlPage).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', 'a')
  
  match = re.compile(r'<link itemprop="contentUrl" href="(.*?)" />',re.DOTALL).findall(html)
  if not match:
    match = re.compile(r'<meta itemprop="contentUrl" content="(.*?)" alt="',re.DOTALL).findall(html)
  url=match[0]
 
  return url