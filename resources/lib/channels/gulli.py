#-*- coding: utf-8 -*-
import urllib2
import CommonFunctions
common = CommonFunctions 
from resources.lib import utils 
import re

title=['Gulli']
img=['gulli']
readyForUse=True

urlBase='http://replay.gulli.fr/replay/'
urlVideo='http://replay.gulli.fr/replay/embed/%s?v=2.7'

def list_shows(channel,folder):
  shows=[]
  
  if folder=='none': 
    shows.append( [channel,'dessins-animes','Dessins Animes','','folder'] )
    shows.append( [channel,'emissions','Emissions','','folder'] )
    shows.append( [channel,'series','Series et films','','folder'] )
  else:           
    d=dict()
    filePath=utils.downloadCatalog(urlBase + folder,'gulli' + folder +'.html',False,{})    
    html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a')
    
    replays = common.parseDOM(html,"div",attrs={"class":"img"})
    for replay in replays :
      title = (common.parseDOM(replay,"span",attrs={"class":"tooltip_ctnt"}) [0]).encode("utf-8") 
      if title not in d:     
        img = re.findall('src="(.*?)"',replay) [0]
        shows.append( [channel,folder + '$$' + title,title,img.encode("utf-8"),'shows'] )
        d[title]=title
    
  return shows

def getVideoURL(channel,id):
    html=utils.get_webcontent(urlVideo % id) 
    url= re.findall("file: '(.*?)',",html) [0]
    return url
        
def list_videos(channel,param):
  folder=param.split('$$')[0]  
  category=param.split('$$')[1]
  
  videos=[] 
  filePath=utils.downloadCatalog(urlBase + folder,'gulli' + folder +'.html',False,{})    
  html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace("\n", " ") 
  html=' '.join([segment for segment in html.split()])
  
  uls = common.parseDOM(html,"ul",attrs={"class":"liste_resultats"})
  for ul in uls:
    replays = common.parseDOM(ul,"li")
    for replay in replays :
      title = (common.parseDOM(replay,"span",attrs={"class":"tooltip_ctnt"}) [0]).encode("utf-8") 
      if title == category:
        match = re.compile(r'<p> <strong>(.*?)</strong> <span>(.*?)<br/>(.*?)</span> </p>',re.DOTALL).findall(replay)            
        if match:
          for t,st,e in match:
            title=t + '-' + st + '-' + e.replace('&nbsp;',' ')
        img = re.findall('src="(.*?)"',replay) [0]  
        url= re.findall('href="(.*?)"',replay) [0]
        iStart=url.find('VOD')
        vodId= url[iStart:]       
        infoLabels={ "Title": title}
        videos.append( [channel, vodId.encode("utf-8") , title.encode("utf-8") , img,infoLabels,'play'] )
  return videos