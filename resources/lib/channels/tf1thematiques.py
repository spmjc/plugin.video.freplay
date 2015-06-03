#-*- coding: utf-8 -*-
import urllib2
import re
import CommonFunctions
common = CommonFunctions 
from resources.lib import utils     
from resources.lib import globalvar

title=['Histoire','Ushuaia TV', 'TV Breizh']
img=['histoire','ushuaiatv','tvbreizh']
readyForUse=True

def list_shows(channel,folder):
  shows=[]
  for i in range(0, int(globalvar.ADDON.getSetting('tf1ThemePages'))):
    filePath=utils.downloadCatalog('http://www.%s.fr/videos?page=%s' % (channel,i),'%s%s.html' % (channel,i),False)    
    html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a')
    
    items=re.findall(r'src="(.*?)"/> 	</a></div>       <div class="views-field views-field-title">        <span class="field-content"><a href="(.*?)">(.*?)</a></span>', html.replace('\n', ' ').replace('\r', ''))
    for item in items:
      shows.append( [channel,item[1], item[2] , 'http://www.%s.fr/%s' % (channel,item[0]),'shows'] )
      
  return shows


def getVideoURL(channel,idVideo):
    VideoURL = 'http://wat.tv/get/ipad/'+idVideo+'.m3u8'
    if globalvar.ADDON.getSetting('tf1ForceHD')=='true' and isHD(VideoURL) :
        VideoURL += '?bwmin=2000000'
    return VideoURL

def list_videos(channel,show): 
    
  videos=[]                  
  htmlFile=urllib2.urlopen('http://www.%s.fr%s' % (channel,show)).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
  
  desc = re.findall(r'<meta name="description" content="(.*?)" />', htmlFile)[0] 
  title = re.findall(r'<meta property="og:title" content="(.*?)" />', htmlFile)[0]
  id = re.findall(r'//www.wat.tv/embedframe/(.*?)" frameborder="0"', htmlFile)[0].replace('?autoStart=1','')[-8:] 
  infoLabels={ "Title": title,"Plot":desc}
  videos.append( [channel, id, title, '',infoLabels,'play'] )
      
  return videos
                    
def isHD(VideoURL) :
  m3u8 = utils.get_webcontent(VideoURL)
  if '1280x720' in m3u8 : return True
  else                  : return False
