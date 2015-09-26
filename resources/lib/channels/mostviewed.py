#-*- coding: utf-8 -*-
import xml.etree.ElementTree as ET  
from resources.lib import utils    
from resources.lib import globalvar
import os, os.path  
import re      


title=[globalvar.LANGUAGE(33030).encode('utf-8')]
img=['mostviewed']
readyForUse=True

def list_shows(channel,folder):
  shows=[]
  
  if folder=='none':                                         
    shows.append( [channel,'1vw_WcP8zyswY1b5l4dck_rE9huXrMNxMnLjbgyzks-g', globalvar.LANGUAGE(33031).encode('utf-8'),'','shows'] )
    shows.append( [channel,'1KKPs4EPV65c1qjS74hK8VEJ32EAtX-rWGp2glydwLJI', globalvar.LANGUAGE(33032).encode('utf-8'),'','shows'] )
    shows.append( [channel,'1Xx4AAA4lHOogJYCT1ylnNj3fNi62XGwZxQPOwc_hwSQ', globalvar.LANGUAGE(33033).encode('utf-8'),'','shows'] )
  return shows

def list_videos(channel,param):
  videos=[] 
  
  filePath=utils.downloadCatalog('https://docs.google.com/spreadsheets/d/%s/pubhtml' % (param),'%s.HTML' % (param),False,{})  
  html=open(filePath).read()
  match = re.compile(r'<td class="s19" dir="ltr">(.*?)</td><td class="s19" dir="ltr">(.*?)</td><td class="s17" dir="ltr">(.*?)</td>',re.DOTALL).findall(html)
  if match:
    for title,path,cnt in match:
      pIndex=path.find('&amp;p=')  
      chan= path[3:pIndex]  
      url=path[pIndex+7:]
      infoLabels={ "Title": title,"Plot":cnt + ' ' + globalvar.LANGUAGE(33039).encode('utf-8')}
      videos.append( [chan, url,title, os.path.join( globalvar.MEDIA, chan +".png"),infoLabels,'play'] ) 
    
  return videos  
