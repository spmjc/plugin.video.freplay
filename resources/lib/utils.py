# -*- coding: utf-8 -*-
import globalvar                  
import simplejson as json    
import re
import os
import imp
import time
import urllib
import urllib2
import string
import log
import logging
import requests       
import YDStreamExtractor     
import HTMLParser
from random import randint

default_ua = "Mozilla/5.0 (Windows NT 6.1; WOW64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/55.0.2883.87 Safari/537.36"

user_agents = [
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36'
    ' (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14'
    ' (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14'
    ' (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/55.0.2883.87 Safari/537.36'
]


class ChromeURLopener(urllib.FancyURLopener):
    version = default_ua


urllib._urlopener = ChromeURLopener()


def getOrderChannel(chanName):
    if globalvar.ADDON.getSetting('disp' + chanName):
        return int(globalvar.ADDON.getSetting('disp' + chanName))
    else:
        print 'Missing Settings for :' + chanName
        return 20


def init():
    for subdir, dirs, files in os.walk(globalvar.CHANNELS_DIR):
        for file in files:
            filename, extension = os.path.splitext(file)
            extension = extension.upper()
            if extension == '.PY' and file != '__init__.py':
                f, filepath, description = imp.find_module(
                    filename, [globalvar.CHANNELS_DIR])
                try:
                    channelModule = imp.load_module(
                        filename, f, filepath, description)
                except Exception:
                    logging.exception(
                        "Error loading channel module " + filepath)

                if channelModule.readyForUse:
                    for i in range(0, len(channelModule.title)):
                        order = getOrderChannel(channelModule.img[i])
                        if order != 99:
                            globalvar.channels[channelModule.img[i]] = [channelModule.title[i], channelModule, order]
                            globalvar.ordered_channels.append((
                                channelModule.img[i],
                                order))
                        else:
                            globalvar.hidden_channels.append(
                                channelModule.title[i])
                            globalvar.hidden_channelsName.append(
                                channelModule.img[i])

    globalvar.ordered_channels.sort(key=lambda channel: channel[0])
    globalvar.ordered_channels.sort(key=lambda channel: channel[1])

    for i in range(len(globalvar.ordered_channels)):
        if globalvar.ordered_channels[i][1] != i:
            globalvar.ordered_channels[i] = (
                globalvar.ordered_channels[i][0],
                i)
            globalvar.ADDON.setSetting(
                'disp' + globalvar.ordered_channels[i][0],
                str(i))
    globalvar.dlfolder = globalvar.ADDON.getSetting('dlFolder')


def get_random_ua_hdr():
    ua = user_agents[randint(0, len(user_agents) - 1)]
    return {
        'User-Agent': ua
    }


def download_catalog(
        url,
        file_name,
        force_dl=False,
        request_type='get',
        post_dic={},
        random_ua=False,
        specific_headers={}):
        
    file_name = format_filename(file_name)
    iCtlgRefresh = int(globalvar.ADDON.getSetting('ctlgRefresh')) * 60

    if not os.path.exists(globalvar.CACHE_DIR):
        os.makedirs(globalvar.CACHE_DIR, mode=0777)
    file_path = os.path.join(globalvar.CACHE_DIR, file_name)

    if os.path.exists(file_path):
        mtime = os.stat(file_path).st_mtime
        dl_file = (time.time() - mtime > iCtlgRefresh)
    else:
        dl_file = True
    if dl_file or force_dl:
        if random_ua:
            ua = user_agents[randint(0, len(user_agents) - 1)]
        else:
            ua = default_ua

        if specific_headers:
            headers = specific_headers
            if 'User-Agent' not in headers:
                headers['User-Agent'] = ua
        else:
            headers = {'User-Agent': ua}

        if request_type == 'get':
            r = requests.get(url, headers=headers)

        elif request_type == 'post':
            r = requests.get(url, headers=headers, data=post_dic)

        with open(file_path, 'wb') as f:
            f.write(r.content)
            
        log.logDLFile(url)
    return file_path


# def downloadCatalog(url, fileName, force, dicPost, specificHeaders=None):
#     bDLFile = True
#     fileName = format_filename(fileName)
#     iCtlgRefresh = int(globalvar.ADDON.getSetting('ctlgRefresh')) * 60
#     if not os.path.exists(globalvar.CACHE_DIR):
#         os.makedirs(globalvar.CACHE_DIR, mode=0777)
#     filePath = os.path.join(globalvar.CACHE_DIR, fileName)
#     if os.path.exists(filePath):
#         mtime = os.stat(filePath).st_mtime
#         bDLFile = (time.time() - mtime > iCtlgRefresh)
#     else:
#         bDLFile = True
#     if bDLFile:
#         if dicPost:
#             data = urllib.urlencode(dicPost)
#             print data
#             urllib.urlretrieve(url, filePath, None, data)
#         else:
#             urllib.urlretrieve(url, filePath)
#         log.logDLFile(url)
#     return filePath


# Compatibilité avec les anciennes chaines
def downloadCatalog(url, fileName, force, dicPost, specificHeaders=None):
    return download_catalog(
        url=url,
        file_name=fileName,
        force_dl=force,
        post_dic=dicPost,
        specific_headers=specificHeaders)


def format_filename(s):
    """Take a string and return a valid filename constructed from the string.
    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores.
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    return filename


def get_webcontent(url):
    req = urllib2.Request(url)
    req.add_header(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0.1')
    req.add_header('Referer', url)
    webcontent = urllib2.urlopen(req).read()
    return webcontent


def move_up(order):
    globalvar.ADDON.setSetting(
        'disp' + globalvar.ordered_channels[order][0],
        str(order - 1))
    globalvar.ADDON.setSetting(
        'disp' + globalvar.ordered_channels[order - 1][0],
        str(order))


def move_down(order):
    globalvar.ADDON.setSetting(
        'disp' + globalvar.ordered_channels[order][0],
        str(order + 1))
    globalvar.ADDON.setSetting(
        'disp' + globalvar.ordered_channels[order + 1][0],
        str(order))


def hide(order):
    globalvar.ADDON.setSetting(
        'disp' + globalvar.ordered_channels[order][0],
        '99')


def unhide(order):
    globalvar.ADDON.setSetting(
        'disp' + globalvar.hidden_channelsName[order],
        str(len(globalvar.ordered_channels)))

def formatName(text):
  return HTMLParser.HTMLParser().unescape(text).title().encode('utf-8')
  
def getExtURL(urlPage):
  print 'YoutubeDL decoding ' + urlPage
  
  vid = YDStreamExtractor.getVideoInfo(urlPage,quality=2) #quality is 0=SD, 1=720p, 2=1080p and is a maximum
  stream_url = vid.streamURL() #This is what Kodi (XBMC) will play
  
  return stream_url
  
def getDMURL(urlPage):
  html     = get_webcontent(urlPage)
  jsonFile=re.compile('var config = (.+?)};', re.DOTALL).findall(html)
  jsonParser = json.loads(jsonFile[0] + '}') 
  qualities=[]
  auto_url=jsonParser['metadata']['qualities']['auto'][0]['url']
  html=get_webcontent(auto_url)
  video_urls = re.compile(r'https:(.+?)core',re.DOTALL).findall(html)
  
  video_url_len = len(video_urls)
  if video_url_len > 0:
    q = globalvar.ADDON.getSetting('DMQuality')
    if q == 'HD' or q=='0':
      # Highest Quality
      video_url = video_urls[video_url_len - 1]
    elif q == 'MD' or q=='1':
      # Medium Quality
      video_url = video_urls[(int)(video_url_len / 2)]
    elif q == 'SD' or q=='2':
      # Lowest Quality
      video_url = video_urls[0] 
  return 'https:%score' % video_url
  
def getVimeoURL(urlPage):
  html     = get_webcontent(urlPage)
  jsonFile=re.compile('var t=(.+?)};', re.DOTALL).findall(html)
  print jsonFile[0] + '}'
  jsonParser = json.loads(jsonFile[0] + '}')
  qualities= jsonParser['request']['files']['progressive'] 
  lenQ=len(qualities)
  print qualities[lenQ-1]['url'] 
  return qualities[lenQ-1]['url']
