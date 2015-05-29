#-*- coding: utf-8 -*-
import resources.lib.utils as utils 
import simplejson as json    
import re, urllib
from resources.lib import globalvar 

title       = ['L\'Equipe.fr']
img         = ['lequipefr']
readyForUse = True

def list_shows(channel,param):  
  shows      = []           
  jsonFile   = utils.get_webcontent('http://iphdata.lequipe.fr/iPhoneDatas/EFR/STD/ALL/V2/navigation.json')
  jsonParser = json.loads(jsonFile)
  for menu in jsonParser['homes_general']:
    if 'url_video' in menu:
      shows.append( [channel,menu['url_video'], menu['nom'].encode('utf-8'),'','shows'] )
  for menu in jsonParser['homes_evenement']:
    if 'url_video' in menu:
      shows.append( [channel,menu['url_video'], menu['nom'].encode('utf-8'),'','shows'] )    
  return shows
  
def list_videos(channel,show_url):
  videos     = []  
  jsonFile   = utils.get_webcontent(show_url)
  jsonParser = json.loads(jsonFile)
  for video in jsonParser['dernieres'] :
    video_id   = video['lien_dm'].split('://')[1]   
    title      = video['titre'].encode('utf-8')      
    icon       = video['vignette_tablette_retina']
    duration   = video['duree']/60
    infoLabels = {"Title": title,"Duration": duration} 
    videos.append([channel,video_id,title,icon,infoLabels,'play'])     
  return videos

def getVideoURL(channel,video_id):
    web_url  = 'http://www.dailymotion.com/embed/video/%s' % video_id
    html     = utils.get_webcontent(web_url)    
    if html.find('"error":') >= 0: return False    
    dm_live  = re.compile('live_rtsp_url":"(.+?)"', re.DOTALL).findall(html)
    dm_1080p = re.compile('"stream_h264_hd1080_url":"(.+?)"', re.DOTALL).findall(html)
    dm_720p  = re.compile('"stream_h264_hd_url":"(.+?)"', re.DOTALL).findall(html)
    dm_high  = re.compile('"stream_h264_hq_url":"(.+?)"', re.DOTALL).findall(html)
    dm_low   = re.compile('"stream_h264_url":"(.+?)"', re.DOTALL).findall(html)
    dm_low2  = re.compile('"stream_h264_ld_url":"(.+?)"', re.DOTALL).findall(html)    
    video_urls = []        
    if dm_live :
        liveVideoUrl = urllib.unquote_plus(dm_live[0]).replace("\\/", "/")
        liveVideoUrl = liveVideoUrl.replace("protocol=rtsp", "protocol=rtmp")
        liveVideoUrl = utils.get_webcontent(liveVideoUrl)
        video_urls.append(liveVideoUrl)
    else:
        if dm_1080p:
            video_urls.append(urllib.unquote_plus(dm_1080p[0]).replace("\\/", "/"))
        if dm_720p:
            video_urls.append(urllib.unquote_plus(dm_720p[0]).replace("\\/", "/"))
        if dm_high:
            video_urls.append(urllib.unquote_plus(dm_high[0]).replace("\\/", "/"))
        if dm_low:
            video_urls.append(urllib.unquote_plus(dm_low[0]).replace("\\/", "/"))
        if dm_low2:
            video_urls.append(urllib.unquote_plus(dm_low2[0]).replace("\\/", "/"))    
    video_url     = ''
    video_url_len = len(video_urls)
    if video_url_len > 0:
        q = globalvar.ADDON.getSetting('lequipefrQuality')
        if q == '0':
            # Highest Quality
            video_url = video_urls[0]
        elif q == '1':
            # Medium Quality
            video_url = video_urls[(int)(video_url_len / 2)]
        elif q == '2':
            # Lowest Quality
            video_url = video_urls[video_url_len - 1]    
    return video_url
 