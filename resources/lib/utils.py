#-*- coding: utf-8 -*-
import globalvar

import os,imp,inspect,time
import sys
import urllib,urllib2
import json
import string  
import log

def getOrderChannel(chanName):
  if globalvar.ADDON.getSetting('disp'+chanName):
    return int(globalvar.ADDON.getSetting('disp'+chanName))
  else:
    print chanName
    return 20

def init():
    for subdir, dirs, files in os.walk(globalvar.CHANNELS_DIR):    
      for file in files:
        extensionStart=file.rfind('.')
        extension=file[extensionStart:len(file)].upper()
        if extension=='.PY' and file!='__init__.py':
          f, filename, description = imp.find_module(file[:-3],[globalvar.CHANNELS_DIR])
          channelModule = imp.load_module(file[:-3], f, filename, description) 
          if channelModule.readyForUse :
            for i in range (0,len(channelModule.title)):
              order=getOrderChannel(channelModule.img[i])
              if order<>99:
                globalvar.channels[channelModule.img[i]]=[channelModule.title[i], channelModule,getOrderChannel(channelModule.img[i])] 
                globalvar.ordered_channels.append((channelModule.img[i],order))   
    globalvar.ordered_channels.sort(key=lambda channel: channel[0])
    globalvar.ordered_channels.sort(key=lambda channel: channel[1])
    globalvar.dlfolder=globalvar.ADDON.getSetting('dlFolder')
        
def downloadCatalog(url,fileName,force):  
  bDLFile=True
  iCtlgRefresh=int(globalvar.ADDON.getSetting('ctlgRefresh')) *60
  if not os.path.exists(globalvar.CACHE_DIR) :
    os.makedirs(globalvar.CACHE_DIR, mode=0777)
  filePath=os.path.join(globalvar.CACHE_DIR,fileName)   
  if os.path.exists(filePath):
    mtime = os.stat(filePath).st_mtime  
    bDLFile=(time.time()-mtime>iCtlgRefresh)
    print fileName,time.time()-mtime
  else:
    bDLFile=True
  if bDLFile:
    urllib.urlretrieve(url,filePath) 
    log.logDLFile(url)
  return filePath
        
def format_filename(s):
  """Take a string and return a valid filename constructed from the string.
Uses a whitelist approach: any characters not present in valid_chars are
removed. Also spaces are replaced with underscores. 
"""
  valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
  filename = ''.join(c for c in s if c in valid_chars)
  return filename

def get_webcontent(url):
  req  = urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0.1')           
  req.add_header('Referer',url)
  webcontent = urllib2.urlopen(req).read()
  return webcontent
        