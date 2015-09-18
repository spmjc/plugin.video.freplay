#-*- coding: utf-8 -*-
import urllib2
import json      
from resources.lib import globalvar
from resources.lib import utils      

#Channels Parameters
title=['HD1','NT1','TF1','TMC',]
img=['hd1','nt1','tf1','tmc']
readyForUse=True

#Channels Settings
bonus={'hd1':globalvar.ADDON.getSetting('hd1Bonus'),
       'nt1':globalvar.ADDON.getSetting('nt1Bonus'),
       'tf1':globalvar.ADDON.getSetting('tf1Bonus'),
       'tmc':globalvar.ADDON.getSetting('tmcBonus'),
      }

url_categories = {'hd1':'http://api.hd1.tv/hd1-genres/android-smartphone/',
                  'nt1':'http://api.nt1.tv/nt1-genres/android-smartphone/',
                  'tf1':'http://api.tf1.fr/tf1-genders/ipad/',
                  'tmc':'http://api.tmc.tv/tmc-genres/android-smartphone/'
                 }
url_shows      = {'hd1':'http://api.hd1.tv/hd1-programs/android-smartphone/',
                  'nt1':'http://api.nt1.tv/nt1-programs/android-smartphone/',
                  'tf1':'http://api.tf1.fr/tf1-programs/ipad/',
                  'tmc':'http://api.tmc.tv/tmc-programs/android-smartphone/'
                 }
url_videos     = {'hd1':'http://api.hd1.tv/hd1-vods/ipad/integral/1/program_id/',
                  'nt1':'http://api.nt1.tv/nt1-vods/ipad/integral/1/program_id/',
                  'tf1':'http://api.tf1.fr/tf1-vods/ipad/integral/1/program_id/',
                  'tmc':'http://api.tmc.tv/tmc-vods/ipad/integral/1/program_id/'
                 }
url_videos2    = {'hd1':'http://api.hd1.tv/hd1-vods/ipad/integral/0/program_id/',
                  'nt1':'http://api.nt1.tv/nt1-vods/ipad/integral/0/program_id/',
                  'tf1':'http://api.tf1.fr/tf1-vods/ipad/integral/0/program_id/',
                  'tmc':'http://api.tmc.tv/tmc-vods/ipad/integral/0/program_id/'
                 }

def list_shows(channel,folder):
    shows=[]
    if folder=='none':
        filPrgm=urllib2.urlopen(url_categories[channel]).read()
        jsoncat     = json.loads(filPrgm)
        for prtCat in jsoncat :
            childs  = prtCat['childs']
            for child in childs :
                shows.append( [channel,str(childs[child]['id']), childs[child]['name'].encode('utf-8'),'','folder'] )
    else:
        filPrgm=urllib2.urlopen(url_shows[channel]).read()
        jsoncat     = json.loads(filPrgm)
        #TMC...
        if channel in ('hd1','nt1','tmc'):
            folder='999'
        for prgm in jsoncat :
            if str(prgm['genderId'])==folder:
                img=prgm['images'][0]['url'] if prgm['images'] else ''
                shows.append( [channel,str(prgm['id']), prgm['shortTitle'].encode('utf-8'),img,'shows'] )
    return shows

def getVideoURL(channel,idVideo):
    VideoURL = 'http://wat.tv/get/ipad/'+idVideo+'.m3u8'
    if globalvar.ADDON.getSetting('tf1ForceHD')=='true' and isHD(VideoURL) :
        VideoURL += '?bwmin=2000000'
    return VideoURL

def list_videos(channel,show_title):
    videos=[]    
    fileVideos=urllib2.urlopen(url_videos[channel] + str(show_title)).read()
    jsonvid     = json.loads(fileVideos)
    for video in jsonvid : 
        video_url=''
        if 'watId' in video:
            video_url=str(video['watId'])
        name=video['shortTitle'].encode('utf-8')
        image_url=video['images'][0]['url']
        date=video['publicationDate'][:10]
        duration=int(video['duration']) / 60
        views=''
        desc=video['longTitle']
        rating=''
        infoLabels={ "Title": name,"Plot":desc,"Aired":date,"Duration": duration, "Year":date[:4]}
        videos.append( [channel, video_url, name, image_url,infoLabels,'play'] )
    if (bonus)[channel]=='true':
      fileVideos=urllib2.urlopen(url_videos2[channel] + str(show_title)).read()
      jsonvid     = json.loads(fileVideos)
      for video in jsonvid : 
          video_url=''
          if 'watId' in video:
              video_url=str(video['watId'])
          name='Bonus-' + video['shortTitle'].encode('utf-8')
          image_url=video['images'][0]['url']
          date=video['publicationDate'][:10]
          duration=int(video['duration']) / 60
          views=''
          desc=video['longTitle']
          rating=''
          infoLabels={ "Title": name,"Plot":desc,"Aired":date,"Duration": duration, "Year":date[:4]}
          videos.append( [channel, video_url, name, image_url,infoLabels,'play'] )
    return videos
    
def isHD(VideoURL) :
    m3u8 = utils.get_webcontent(VideoURL)
    if '1280x720' in m3u8 : return True
    else                  : return False