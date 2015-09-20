#-*- coding: utf-8 -*-
import urllib2
import CommonFunctions
common = CommonFunctions 
from resources.lib import utils 
import re

title=['TFou']
img=['tfou']
readyForUse=True

urlBase='http://www.tfou.fr'

def list_shows(channel,folder):
  shows=[]
  
  if folder=='none': 
    print urlBase + '/videos/'
    filePath=utils.downloadCatalog(urlBase + '/videos/','tfou.html',False)    
    html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a')
    
    replays = common.parseDOM(html,"li",attrs={"class":"teaser158120 t3"})
    for replay in replays :
      match = re.compile(r'alt="(.*?)" style="background-image: url(.*?);" class="teaserImg"> </a> <a href="(.*?)"',re.DOTALL).findall(replay)
            
      if match:
        for title,img,url in match:
          shows.append( [channel,url.encode("utf-8"), title.replace('&#039;',"'").encode("utf-8") , img.replace('(','').replace(')','').encode("utf-8"),'shows'] )
      
    
  return shows
  
def list_videos(channel,folder):  
  videos=[] 
  
  filePath=utils.downloadCatalog(urlBase + folder,'tfou' + folder +'.html',False)    
  html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a') 
  
  divs = common.parseDOM(html,"div",attrs={"class":"description"})
  for div in divs: 
    print div.encode("utf-8")
    titre='bb'
    url=''
    img=''
                    
    match = re.compile(r'<a href="(.*?)">(.*?)</a>"',re.DOTALL).findall(div)
          
    if match:
      for title,link in match:
        titre=title
        url=link
    
    print titre
    print img
    
    infoLabels={ "Title": titre}
    videos.append( [channel, url.encode("utf-8") , titre.replace('&#039;',"'").encode("utf-8") , img,infoLabels,'play'] )
    
  return videos