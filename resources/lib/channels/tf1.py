#-*- coding: utf-8 -*-
import base64
import hashlib
import json
import urllib
import urllib2
import urlparse
from resources.lib import globalvar

# Channels Parameters
title = ['HD1', 'NT1', 'TF1', 'TMC']
img = ['hd1', 'nt1', 'tf1', 'tmc']
readyForUse = False

# Channels Settings
BONUS = {'hd1': globalvar.ADDON.getSetting('hd1Bonus'),
         'nt1': globalvar.ADDON.getSetting('nt1Bonus'),
         'tf1': globalvar.ADDON.getSetting('tf1Bonus'),
         'tmc': globalvar.ADDON.getSetting('tmcBonus')}

URL_CATEGORIES = {'hd1': 'http://api.hd1.tv/hd1-genres/android-smartphone/',
                  'nt1': 'http://api.nt1.tv/nt1-genres/android-smartphone/',
                  'tf1': 'http://api.tf1.fr/tf1-genders/ipad/',
                  'tmc': 'http://api.tmc.tv/tmc-genres/android-smartphone/'}
URL_SHOWS = {'hd1': 'http://api.hd1.tv/hd1-programs/android-smartphone/',
             'nt1': 'http://api.nt1.tv/nt1-programs/android-smartphone/',
             'tf1': 'http://api.tf1.fr/tf1-programs/ipad/',
             'tmc': 'http://api.tmc.tv/tmc-programs/android-smartphone/'}
URL_VIDEOS = {
    'hd1': 'http://api.hd1.tv/hd1-vods/ipad/integral/1/program_id/',
    'nt1': 'http://api.nt1.tv/nt1-vods/ipad/integral/1/program_id/',
    'tf1': 'http://api.tf1.fr/tf1-vods/ipad/integral/1/program_id/',
    'tmc': 'http://api.tmc.tv/tmc-vods/ipad/integral/1/program_id/'
}
URL_VIDEOS2 = {
    'hd1': 'http://api.hd1.tv/hd1-vods/ipad/integral/0/program_id/',
    'nt1': 'http://api.nt1.tv/nt1-vods/ipad/integral/0/program_id/',
    'tf1': 'http://api.tf1.fr/tf1-vods/ipad/integral/0/program_id/',
    'tmc': 'http://api.tmc.tv/tmc-vods/ipad/integral/0/program_id/'
}


def flatten(list_of_list):
  """Flattens a list of list.

  For [[a, b], [c]], returns [a, b, c].
  """
  return [item for sublist in list_of_list for item in sublist]


def list_shows(channel, folder):
  print 'COUCOU'
  """Returns the programs of the given gender, or the list genders."""

  def list_genders():
    """Returns the list of genders for the current channel."""

    def convert(gender):
      """Returns a list of of all leaf gender

      If the passed in 'gender' has some children, recursively convert
      them. Otherwise, just convert the current gender to the expected
      format.
      """
      if gender['childs']:
        return flatten([convert(child) for child in gender['childs'].values()])
      else:
        gender_title = gender['name'].encode('utf-8')
        return [[channel, str(gender['id']), gender_title, '', 'folder']]

    url = URL_CATEGORIES[channel]
    print 'Loading ' + url
    genders = json.loads(urllib2.urlopen(url).read())
    return flatten([convert(gender) for gender in genders])

  def list_programs():
    """Returns the list of programs of the given (channel, gender)."""

    def convert(program):
      """Converts a Json program description to a list."""
      image = program['images'][0]['url'] if program['images'] else ''
      short_title = program['shortTitle'].encode('utf-8')
      return [channel, str(program['id']), short_title, image, 'shows']

    url = URL_SHOWS[channel]
    print 'Loading ' + url
    programs = json.loads(urllib2.urlopen(url).read())

    # Only TF1 has working support for folder. For the other one just
    # return everything.
    gender = folder
    if channel in ('hd1', 'nt1', 'tmc'):
      gender = '999'
    return [convert(p) for p in programs if str(p['genderId']) == gender]

  if folder == 'none':
    return list_genders()
  else:
    return list_programs()


def list_videos(channel, show_title):
  """Returns the list of video for the given show name."""
  def convert(video):
    """Convert a Json video description to a list."""
    video_url = ''
    if 'watId' in video:
      video_url = str(video['watId'])
    name = video['shortTitle'].encode('utf-8')
    image_url = video['images'][0]['url']
    date = video['publicationDate'][:10]
    duration = int(video['duration'])
    desc = video['longTitle']
    info_labels = {'Title': name,
                  'Plot': desc,
                  'Aired': date,
                  'Duration': duration,
                  'Year': date[:4]}
    return [channel, video_url, name, image_url, info_labels, 'play']

  urls = [URL_VIDEOS[channel] + str(show_title)]
  if (BONUS)[channel] == 'true':
    urls.append(URL_VIDEOS2[channel] + str(show_title))
  print 'Loading ' + repr(urls)
  videos = flatten([json.loads(urllib2.urlopen(url).read()) for url in urls])
  return [convert(video) for video in videos]

 
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
