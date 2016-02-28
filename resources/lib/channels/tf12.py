#-*- coding: utf-8 -*-
import urllib2, json, hashlib, base64
import requests     
from resources.lib import globalvar
from resources.lib import utils      

#Channels Parameters
title=['HD1','NT1','TF12','TMC',]
img=['hd1','nt1','tf12','tmc']
readyForUse=False

#Channels Settings
bonus={'hd1':globalvar.ADDON.getSetting('hd1Bonus'),
       'nt1':globalvar.ADDON.getSetting('nt1Bonus'),
       'tf1':globalvar.ADDON.getSetting('tf1Bonus'),
       'tmc':globalvar.ADDON.getSetting('tmcBonus'),
      }

url_categories = {'hd1':'http://api.hd1.tv/hd1-genres/android-smartphone/',
                  'nt1':'http://api.nt1.tv/nt1-genres/android-smartphone/',
                  'tf12':'http://api.tf1.fr/tf1-genders/ipad/',
                  'tmc':'http://api.tmc.tv/tmc-genres/android-smartphone/'
                 }
url_shows      = {'hd1':'http://api.hd1.tv/hd1-programs/android-smartphone/',
                  'nt1':'http://api.nt1.tv/nt1-programs/android-smartphone/',
                  'tf12':'http://api.tf1.fr/tf1-programs/ipad/',
                  'tmc':'http://api.tmc.tv/tmc-programs/android-smartphone/'
                 }
url_videos     = {'hd1':'http://api.hd1.tv/hd1-vods/ipad/integral/1/program_id/',
                  'nt1':'http://api.nt1.tv/nt1-vods/ipad/integral/1/program_id/',
                  'tf12':'http://api.tf1.fr/tf1-vods/ipad/integral/1/program_id/',
                  'tmc':'http://api.tmc.tv/tmc-vods/ipad/integral/1/program_id/'
                 }
url_videos2    = {'hd1':'http://api.hd1.tv/hd1-vods/ipad/integral/0/program_id/',
                  'nt1':'http://api.nt1.tv/nt1-vods/ipad/integral/0/program_id/',
                  'tf12':'http://api.tf1.fr/tf1-vods/ipad/integral/0/program_id/',
                  'tmc':'http://api.tmc.tv/tmc-vods/ipad/integral/0/program_id/'
                 }

WebSession = requests.Session()

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
    mediaId  = idVideo
    VideoURL = get_wat_m3u8_url(channel,mediaId)
    return VideoURL
#     VideoURL = 'http://wat.tv/get/ipad/'+idVideo+'.m3u8'
#     if globalvar.ADDON.getSetting('tf1ForceHD')=='true' and isHD(VideoURL) :
#         VideoURL += '?bwmin=2000000'
#     return VideoURL
    
def get_wat_m3u8_url(channel,mediaId) :
    url       = 'http://api.wat.tv/services/Delivery'
    appName   = 'sdk/Iphone/1.0'
    method    = 'getUrl'
    timestamp = get_timestamp()
    version   = '1.4.32'
    authKey   = get_authKey(appName,mediaId,method,timestamp,version)
    hostingApplicationName    = 'com.tf1.applitf1'
    hostingApplicationVersion = '60010000.15040209'
    headers = {'User-Agent': 'myTF1/60010000.15040209 CFNetwork/609 Darwin/13.0.0',
               'Host':'api.wat.tv',
              }
    payload = {'appName':appName,
               'method':method,
               'mediaId':mediaId,
               'authKey':authKey,
               'version':version,
               'hostingApplicationName':hostingApplicationName,
               'hostingApplicationVersion':hostingApplicationVersion,
              }
    req = WebSession.post(url,data=payload,headers=headers)    
    print 'TEXT :'+req.text
    url = req.json()['message']
    return url#+'|User-Agent='+urllib2.quote('AppleCoreMedia/1.0.0.10A551 (iPhone; U; CPU OS 6_0_2 like Mac OS X; fr_fr)')+'&Host='+urllib2.quote('www.wat.tv')+'&Cookie='+urllib2.quote('seen='+mediaId)

def get_authKey(appName,mediaId,method,timestamp,version):
    secret  = base64.b64decode('VzNtMCMxbUZJ')
    string  = "%s-%s-%s-%s-%d"%(mediaId, secret,appName,secret,timestamp)
    authKey = hashlib.md5(bytearray(string)).hexdigest()+'/'+str(timestamp)
    print 'AUTHKEY : '+authKey
    return authKey
    
    
def get_timestamp():                                 
    soup = utils.get_webcontent('http://www.wat.tv/servertime')
    html = soup.decode("utf-8")
    print 'GET TIMESTAMP : '+html.encode('utf-8')
    timestamp = html.split(u"""|""")[0].encode("utf-8")
    print 'TIMESTAMP :'+timestamp
    return int(timestamp)

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
    #if (bonus)[channel]=='true':                                                   
    if 'r'=='true':
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