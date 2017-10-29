# -*- coding: utf-8 -*-

import urllib2
import CommonFunctions as common
from resources.lib import utils
from resources.lib import globalvar  
import CommonFunctions as common 
import re


title=['Jeux Video.com']
img=['jvc']
readyForUse=True

def list_shows(channel,folder):
  shows =[]                                                       
  shows.append( [channel,'pc', 'PC'.encode('utf-8') , '','shows'] )          
  shows.append( [channel,'ps4', 'PS4'.encode('utf-8') , '','shows'] )          
  shows.append( [channel,'xo', 'XBox One'.encode('utf-8') , '','shows'] )          
  shows.append( [channel,'switch', 'Switch'.encode('utf-8') , '','shows'] )          
  shows.append( [channel,'ps3', 'PS3'.encode('utf-8') , '','shows'] )          
  shows.append( [channel,'360', 'XBox 360'.encode('utf-8') , '','shows'] )          
  shows.append( [channel,'wiiu', 'Wii U'.encode('utf-8') , '','shows'] )          
  shows.append( [channel,'wii', 'Wii'.encode('utf-8') , '','shows'] )          
  shows.append( [channel,'3ds', '3DS'.encode('utf-8') , '','shows'] )          
  shows.append( [channel,'vita', 'PS Vita'.encode('utf-8') , '','shows'] )          
  shows.append( [channel,'ds', 'DS'.encode('utf-8') , '','shows'] )          
  shows.append( [channel,'psp', 'PSP'.encode('utf-8') , '','shows'] )          
  shows.append( [channel,'iphone', 'Iphone'.encode('utf-8') , '','shows'] )          
  shows.append( [channel,'android', 'Android'.encode('utf-8') , '','shows'] )
    
  return shows
  
def list_videos(channel,folder):  
  videos=[]
  filePath=utils.downloadCatalog('http://www.jeuxvideo.com/rss/rss-videos-%s.xml' % folder ,'jvc%s.xml' % folder,False,{})  
  xml = open(filePath).read()
  items = common.parseDOM(xml, "item") 
  for item in items:          
    title=common.parseDOM(item, "title")[0].encode('utf-8')
    img=common.parseDOM(item, "url")[0].encode('utf-8')
    desc=common.parseDOM(item, "description")[0].encode('utf-8')
    link=common.parseDOM(item, "link")[0].encode('utf-8')
    infoLabels = {
                "Title": title,
                "Plot": desc,}
    videos.append([channel,link,title,img,infoLabels,'play'])
  
  return videos  
  

def getVideoURL(channel, url):
  html = urllib2.urlopen(url).read()  
  video=re.findall('<meta itemprop="contentUrl" content="(.*?)" />', html)[0]
  return video