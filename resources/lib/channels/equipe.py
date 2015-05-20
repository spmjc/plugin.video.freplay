#-*- coding: utf-8 -*-
import urllib,urllib2
import json    
import re

title=['LEquipe.fr']
img=['equipefr']
readyForUse=True

def list_shows(channel,param):  
  shows=[]
           
  jsonFile=urllib2.urlopen('http://iphdata.lequipe.fr/iPhoneDatas/EFR/STD/ALL/V2/navigation.json').read()
  jsonParser= json.loads(jsonFile)
  for menu in jsonParser['homes_general']:
    if 'url_video' in menu:
      shows.append( [channel,menu['url_video'], menu['nom'].encode('utf-8'),'','shows'] )
  for menu in jsonParser['homes_evenement']:
    if 'url_video' in menu:
      shows.append( [channel,menu['url_video'], menu['nom'].encode('utf-8'),'','shows'] )
    
  return shows
  
def list_videos(channel,show_url):
  videos=[] 
  
  jsonFile=urllib2.urlopen(show_url).read()
  print show_url
  jsonParser= json.loads(jsonFile)
  for video in jsonParser['dernieres'] :
    lien_dm=video['lien_dm'].replace(':','')   
    title=video['titre'].encode('utf-8')      
    icon=video['vignette_tablette_retina']
    duration=video['duree']/60
    infoLabels={ "Title": title,"Duration": duration} 
    videos.append( [channel, lien_dm, title, icon,infoLabels,'play'] )     
    
  return videos

def getVideoURL(channel,videoId):
  dmFile=urllib2.urlopen('http://www.dailymotion.com/embed/%s?autoplay=true' % (videoId)).read()
  dmFile=urllib2.urlopen('http://www.dailymotion.com/embed/video/k5FqRVcNLkephybdrFt').read()
  
  video_url=temp(dmFile)
  print 'temp',video_url    
  
  print 'http://www.dailymotion.com/embed/%s' % (videoId)
  info = re.search(r'var info = ({.*?}),$', dmFile,re.MULTILINE)
  info=info.group(1)
  jsonParser= json.loads(info)
  video_url= jsonParser['stream_h264_hd_url']
  video_url=urllib.unquote_plus(video_url).replace("\\/", "/")
        
  print 'func',video_url 
  
  return video_url 

def temp(link):
#         if link.find('"error":') >= 0:
#             err_title = re.compile('"title":"(.+?)"').findall(link)[0]
#             if not err_title:
#                 err_title = 'Content not available.'
#             
#             err_message = re.compile('"message":"(.+?)"').findall(link)[0]
#             if not err_message:
#                 err_message = 'No such video or the video has been removed due to copyright infringement issues.'
#             
#             raise UrlResolver.ResolverError(err_message)
        
  
  dm_live = re.compile('live_rtsp_url":"(.+?)"', re.DOTALL).findall(link)
  dm_1080p = re.compile('"stream_h264_hd1080_url":"(.+?)"', re.DOTALL).findall(link)
  dm_720p = re.compile('"stream_h264_hd_url":"(.+?)"', re.DOTALL).findall(link)
  dm_high = re.compile('"stream_h264_hq_url":"(.+?)"', re.DOTALL).findall(link)
  dm_low = re.compile('"stream_h264_url":"(.+?)"', re.DOTALL).findall(link)
  dm_low2 = re.compile('"stream_h264_ld_url":"(.+?)"', re.DOTALL).findall(link)
  
  videoUrl = []
  if dm_live:
      liveVideoUrl = urllib.unquote_plus(dm_live[0]).replace("\\/", "/")
      liveVideoUrl = liveVideoUrl.replace("protocol=rtsp", "protocol=rtmp")
      liveVideoUrl = self.net.http_GET(liveVideoUrl).content
      videoUrl.append(liveVideoUrl)
  else:
      if dm_1080p:
          videoUrl.append(urllib.unquote_plus(dm_1080p[0]).replace("\\/", "/"))
          print videoUrl[len(videoUrl) - 1]
      if dm_720p:
          videoUrl.append(urllib.unquote_plus(dm_720p[0]).replace("\\/", "/"))
          print videoUrl[len(videoUrl) - 1]
      if dm_high:
          videoUrl.append(urllib.unquote_plus(dm_high[0]).replace("\\/", "/"))
          print videoUrl[len(videoUrl) - 1]
      if dm_low:
          videoUrl.append(urllib.unquote_plus(dm_low[0]).replace("\\/", "/")) 
          print videoUrl[len(videoUrl) - 1]
      if dm_low2:
          videoUrl.append(urllib.unquote_plus(dm_low2[0]).replace("\\/", "/"))
          print videoUrl[len(videoUrl) - 1]
  
  
  print len(videoUrl)
  vUrl = ''
  vUrlsCount = len(videoUrl)
  if vUrlsCount > 0:
      q = 0
      if q == '0':
          # Highest Quality
          vUrl = videoUrl[0]
      elif q == '1':
          # Medium Quality
          vUrl = videoUrl[(int)(vUrlsCount / 2)]
      elif q == '2':
          # Lowest Quality
          vUrl = videoUrl[vUrlsCount - 1]
  
  return vUrl  