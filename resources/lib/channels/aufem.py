#-*- coding: utf-8 -*-
import re
from resources.lib import utils     

title=['Au Feminin']
img=['aufem']
readyForUse=True

def list_shows(channel,folder):
  shows=[]
                                                        
  shows.append( [channel,'http://www.aufeminin.com/mode/video-mode-ssc118.html', 'Mode' , '','shows'] )
  shows.append( [channel,'http://www.aufeminin.com/beaute/video-maquillage-beaute-ssc119.html', 'Beaute' , '','shows'] )  
  shows.append( [channel,'http://www.aufeminin.com/maman/video-maman-bebe-ssc122.html', 'Maman' , '','shows'] )
  shows.append( [channel,'http://www.aufeminin.com/psycho/video-psycho-ssc125.html', 'Psycho' , '','shows'] )
  shows.append( [channel,'http://www.aufeminin.com/couple/video-couple-ssc126.html', 'Sexo' , '','shows'] )
  shows.append( [channel,'http://www.aufeminin.com/cuisine/video-recette-cuisine-ssc117.html', 'Cuisine' , '','shows'] )
  shows.append( [channel,'http://www.aufeminin.com/societe/video-societe-ssc130.html', 'Societe' , '','shows'] )
  shows.append( [channel,'http://www.aufeminin.com/forme/video-fitness-ssc120.html', 'Forme' , '','shows'] )
  shows.append( [channel,'http://www.aufeminin.com/culture/video-culture-ssc121.html', 'Culture' , '','shows'] )
  shows.append( [channel,'http://www.aufeminin.com/mariage/video-mariage-ssc129.html', 'Mariage' , '','shows'] )     
  shows.append( [channel,'http://www.aufeminin.com/deco/video-deco-ssc127.html', 'Deco' , '','shows'] )
  
  return shows
 
def list_videos(channel,url): 
    
  videos=[]
  filePath=utils.downloadCatalog(url ,'aufem' + url[-8:],False,{})
  html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
  #print html
  match = re.compile(r'shareImg: "(.*?)",  (.*?),  shareTitle: "(.*?)",  shareUrl: "(.*?)",',re.DOTALL).findall(html)
  
  for img,empty,title,url in match:
    infoLabels={ "Title": title}
    videos.append( [channel, url.replace('\\','') , title , img,infoLabels,'play'] )
    
  return videos
  
def getVideoURL(channel,url):
  filePath=utils.downloadCatalog(url ,'aufem' + url[-12:],False,{})
  html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
  print html
  urls = re.compile(r'<source src="(.*?)"', re.DOTALL).findall(html)
  for url in urls:
    if 'HD.mp4' in url:
      url_video=url
      
  return url_video
  
  