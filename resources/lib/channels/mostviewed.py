#-*- coding: utf-8 -*-
import xml.etree.ElementTree as ET  
from resources.lib import utils    
from resources.lib import globalvar
import os, os.path  
import re      


title=['Most Viewed']
img=['mostviewed']
readyForUse=True

def list_shows(channel,folder):
  shows=[]
  
  if folder=='none':
    shows.append( [channel,'now', 'Being Watched','','shows'] ) 
    shows.append( [channel,'7', '7 Days','','shows'] )
    shows.append( [channel,'30', '30 Days','','shows'] )
  return shows

def list_videos(channel,category):
  videos=[] 
  
  filePath=utils.downloadCatalog('https://docs.google.com/spreadsheets/d/1KKPs4EPV65c1qjS74hK8VEJ32EAtX-rWGp2glydwLJI/pubhtml','MOSTVIEWED.HTML',False)
  html=open(filePath).read()
  match = re.compile(r'<td class="s17" dir="ltr">(.*?)</td><td class="s18" dir="ltr">(.*?)</td>',re.DOTALL).findall(html)
  if match:
    for title,url in match:
      print title,url               
      infoLabels={ "Title": title}
      videos.append( [channel, url, title, os.path.join( globalvar.MEDIA, "cplus.png"),infoLabels,'play'] ) 
    
  return videos  