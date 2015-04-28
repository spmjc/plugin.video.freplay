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
    ctime = os.stat(filePath).st_ctime  
    bDLFile=(time.time()-ctime>iCtlgRefresh)
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
        