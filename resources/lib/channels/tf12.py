#-*- coding: utf-8 -*-    
from resources.lib import utils
import base64
import hashlib
import json
import urllib
import urllib2
import urlparse
from resources.lib import globalvar

title=['TF1','NT1','HD1','TMC','XTRA']
img=['tf1','nt1','hd1','tmc','xtra']
readyForUse=True          

#urlCatalog='http://api.mytf1.tf1.fr/mobile/init?device=ios-tablet'
urlCatalog='http://api.mytf1.tf1.fr/mobile/2/init?device=ios-tablet'

def list_shows(channel,param):  
  shows=[]
  
  filePath=utils.downloadCatalog(urlCatalog,'tf1.json',False,{}) 
  filPrgm=open(filePath).read()
  jsonParser     = json.loads(filPrgm) 
  uniqueItem = dict()  
  
  if param=='none':
    for prgm in jsonParser['programs'] :
      if channel in prgm['channels']:
        if prgm['category'] not in uniqueItem: 
          shows.append( [channel,prgm['categorySlug'], prgm['category'].encode('utf-8'),'','folder'] )
          uniqueItem[prgm['category']] = prgm['category']
  else:
    for prgm in jsonParser['programs'] : 
      if channel in prgm['channels']:
        if prgm['categorySlug']==param: 
          shows.append( [channel,prgm['id'], prgm['title'].encode('utf-8'),'','shows'] )
  return shows
  
def list_videos(channel, id):
  videos=[]
  
  filePath=utils.downloadCatalog(urlCatalog,'tf1.json',False,{}) 
  filPrgm=open(filePath).read()
  jsonParser     = json.loads(filPrgm) 
  
  for vid in jsonParser['videos'] :
    if vid['programId'] ==id:
      if globalvar.ADDON.getSetting(channel + 'Bonus')=='true' or vid['videoType']['type']=='replay' or vid['videoType']['type']=='video':
        title=vid['title'].encode('utf-8')         
        plot, duration = '', ''
        if 'summary' in vid : plot=vid['summary'].encode('utf-8')       
        if 'length' in vid  :duration=vid['length']/60 
        infoLabels = { "Title": title,"Plot":plot,"Duration": duration}
        videos.append( [channel, vid['streamId'], title, '',infoLabels,'play'] )
          
  return videos          
  
def getVideoURLSimple(channel,id):
  VideoURL= 'http://wat.tv/get/ipad/' + id
  if globalvar.ADDON.getSetting('tf1ForceHD')=='true' and isHD(VideoURL) :
    VideoURL += '?bwmin=2000000'
  return VideoURL
 
def isHD(VideoURL) :
  m3u8 = utils.get_webcontent(VideoURL)
  if '1280x720' in m3u8 : return True
  else                  : return False 
  
def getVideoURL(channel, media_id):
  """Returns the URL to use to read the given video."""
  def get_timestamp():
    """Returns the current server timestamp."""
    servertime = urllib2.urlopen('http://www.wat.tv/servertime').read()
    timestamp = servertime.split(u"""|""")[0].encode('utf-8')
    return int(timestamp)

  def get_auth_key(app_name, media_id, timestamp):
    """Return the AuthKey to use to get the Video URL."""
    secret = base64.b64decode('VzNtMCMxbUZJ')
    string = '%s-%s-%s-%s-%d' % (media_id, secret, app_name, secret, timestamp)
    #auth_key = hashlib.md5(bytearray(string)).hexdigest() + '/' + str(timestamp)
    auth_key = hashlib.md5(string).hexdigest() + '/' + str(timestamp)
    return auth_key

  user_agent = 'myTF1/60010000.15040209 CFNetwork/609 Darwin/13.0.0'
  app_name = 'sdk/Iphone/1.0'
  method = 'getUrl'
  timestamp = get_timestamp()
  version = '1.4.32'
  auth_key = get_auth_key(app_name, media_id, timestamp)
  hosting_application_name = 'com.tf1.applitf1'
  hosting_application_version = '60010000.15040209'

  req = urllib2.Request('http://api.wat.tv/services/Delivery')
  req.add_header('User-Agent', user_agent)
  req.add_data(
      ('appName=%s&method=%s&mediaId=%s&authKey=%s&version=%s'
       '&hostingApplicationName=%s&hostingApplicationVersion=%s')
      % (app_name, method, media_id, auth_key, version,
         hosting_application_name, hosting_application_version))
  print 'Loading ' + req.get_full_url() + ' ' + req.get_data()
  data = json.loads(urllib2.urlopen(req).read())
  print 'Response: ' + repr(data)
  if int(data['code']) != 200:
    # Something is not working, fall back to the simple url scheme.
    return 'http://wat.tv/get/ipad/' + media_id + '.m3u8'

  m3u8_url = data['message']

  if globalvar.ADDON.getSetting('tf1ForceHD') == 'true':
    scheme, netloc, path, query_string, fragment = urlparse.urlsplit(m3u8_url)
    query_params = urlparse.parse_qs(query_string)
    query_params.pop('bwmax', None)
    new_query_string = urllib.urlencode(query_params, doseq=True)
    m3u8_url = urlparse.urlunsplit((scheme, netloc, path, new_query_string,
                                    fragment))

  # The URL returned by '/services/Delivery' will return a 302 and this seems
  # to confuse the media player. So we first follow and 302 chain and return
  # the final real address.
  req = urllib2.Request(m3u8_url)
  req.add_header('User-Agent', user_agent)
  print 'Loading ' + req.get_full_url()
  response = urllib2.urlopen(req)
  return response.url + '|User-Agent=' + urllib2.quote(user_agent) 
