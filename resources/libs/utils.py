#-*- coding: utf-8 -*-
import globalvar

import os,imp,inspect
import sys
import urllib,urllib2
import json
import string

def getOrderChannel(chanName):
  return globalvar.ADDON.getSetting('disp'+chanName)

def init():
    print globalvar.CHANNELS_DIR
    for subdir, dirs, files in os.walk(globalvar.CHANNELS_DIR):    
      for file in files:
        extensionStart=file.rfind('.')
        extension=file[extensionStart:len(file)].upper()
        if extension=='.PY':
          f, filename, description = imp.find_module(file[:-3],[globalvar.CHANNELS_DIR])
          channelModule = imp.load_module(file[:-3], f, filename, description) 
          if channelModule.readyForUse :
            for i in range (0,len(channelModule.title)):
              order=getOrderChannel(channelModule.img[i])
              if order<>'99':
                globalvar.channels[channelModule.img[i]]=[channelModule.title[i], channelModule,getOrderChannel(channelModule.img[i])] 
                globalvar.ordered_channels.append((channelModule.img[i],order))   
    
    globalvar.ordered_channels.sort(key=lambda channel: channel[1])
    globalvar.dlfolder=globalvar.ADDON.getSetting('dlFolder')
    
def firstRun():
    if not os.path.exists(globalvar.CACHE_DIR) :
        os.makedirs(globalvar.CACHE_DIR, mode=0777)
    #Download Pluzz Catalog
    if os.path.exists(globalvar.CATALOG_PLUZZ):
        os.remove(globalvar.CATALOG_PLUZZ)
    #urllib.urlretrieve('http://webservices.francetelevisions.fr/catchup/flux/flux_main.zip',globalvar.CATALOG_PLUZZ)
    #Download Canal
    if os.path.exists(globalvar.CATALOG_CANAL):
        os.remove(globalvar.CATALOG_CANAL)
    #urllib.urlretrieve('http://service.mycanal.fr/authenticate.json/Android_Tab/1.1?highResolution=1',globalvar.CATALOG_CANAL)
    #Download ARTE
    if os.path.exists(globalvar.CATALOG_ARTE):
        os.remove(globalvar.CATALOG_ARTE)
    #urllib.urlretrieve('http://www.arte.tv/papi/tvguide-flow/sitemap/feeds/videos/F.xml',globalvar.CATALOG_ARTE)
        

    #Download M6 Catalog
    #if os.path.exists(globalvar.CATALOG_M6):
    #    os.remove(globalvar.CATALOG_M6)
    #urllib.urlretrieve('http://static.m6replay.fr/catalog/m6group_ipad/m6replay/catalogue.xml',globalvar.CATALOG_M6)
    

def format_filename(s):
    """Take a string and return a valid filename constructed from the string.
Uses a whitelist approach: any characters not present in valid_chars are
removed. Also spaces are replaced with underscores.
 
Note: this method may produce invalid filenames such as ``, `.` or `..`
When I use this method I prepend a date string like '2009_01_15_19_46_32_'
and append a file extension like '.txt', so I avoid the potential of using
an invalid filename.
 
"""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    return filename