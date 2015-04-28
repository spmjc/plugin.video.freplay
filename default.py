#-*- coding: utf-8 -*-
import sys
import os, os.path
import urllib
import urlparse

import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon

import resources.lib.globalvar as globalvar
import resources.lib.utils as utils
import resources.lib.channels.favourites as favourites
import resources.lib.commondownloader as commondownloader 
import resources.lib.log as log

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def add_Channel(idChannel,nameChannel):
    url = build_url({'mode': 'folder', 'channel': idChannel, 'param':'none'})
    li = xbmcgui.ListItem(nameChannel, iconImage=os.path.join( globalvar.MEDIA, idChannel+".png"))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)

def buildShowsList(videos):
    for chan,video_url, video_title, video_icon,infoLabels,video_mode in videos:
        li = xbmcgui.ListItem(video_title, iconImage=video_icon,thumbnailImage=video_icon,path=video_url)
        if video_mode=='play':
            li.setInfo( type='Video', infoLabels=infoLabels)            
            li.setProperty('IsPlayable', 'true')
            li.addContextMenuItems([ ('Download', 'XBMC.RunPlugin(%s?mode=dl&channel=%s&param=%s&name=%s)' % (sys.argv[0],chan,urllib.quote_plus(video_url),urllib.quote_plus(video_title))),
                     ], replaceItems=True)
        url = build_url({'mode': video_mode, 'channel': chan, 'param':video_url})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=False)
        xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.setPluginCategory(addon_handle, 'episodes' )
        xbmcplugin.setContent(addon_handle, 'episodes')
    xbmc.executebuiltin('Container.SetViewMode(' + globalvar.VIEWID + ')')
    if channel=='favourites' and param=='unseen':
        notify('Check/Uncheck "Hide Watched" in the left panel',0)
        
def notify(text,channel):
    time = 3000  #in miliseconds 
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('FReplay',text, time, os.path.join( globalvar.ADDON_DIR, "icon.png")))

try:
  mode = args.get('mode', None)
  
  utils.init()
  
  if mode is None: 
      log.logEvent(mode,'Display','Home')
      for item in globalvar.ordered_channels:
        add_Channel(item[0],globalvar.channels[item[0]][0])
      
      xbmcplugin.endOfDirectory(addon_handle)
  else:    
      channel = args['channel'][0]
      param = args['param'][0]
      if mode[0]=='folder':        
          log.logEvent(channel,'Display',param)
          for chan,folder_param, folder_title, folder_icon, mode in globalvar.channels[channel][1].list_shows(channel,param):
              url = build_url({'mode': mode, 'channel': chan, 'param':folder_param})
              li = xbmcgui.ListItem(folder_title, iconImage=folder_icon)
              #Contextual Menu
              li.addContextMenuItems([], replaceItems=True)
              if mode=='shows' and channel!='favourites':
                  li.addContextMenuItems([ ('Add to FReplay Favourites', 'XBMC.RunPlugin(%s?mode=bkm&action=add&channel=%s&param=%s&display=%s)' % 
                      (sys.argv[0],chan,urllib.quote_plus(folder_param),urllib.quote_plus(folder_title))),
                           ], replaceItems=True)
              if mode=='shows' and channel=='favourites':
                  li.addContextMenuItems([ ('Remove from Favourites', 'XBMC.RunPlugin(%s?mode=bkm&action=rem&channel=%s&param=%s&display=%s)' % 
                  (sys.argv[0],chan,urllib.quote_plus(folder_param),urllib.quote_plus(folder_title))),
                           ], replaceItems=True)
              xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)
      elif mode[0]=='shows':     
          log.logEvent(channel,'Display',param)
          buildShowsList(globalvar.channels[channel][1].list_videos(channel,param))
      elif mode[0]=='play':   
          log.logEvent(channel,'Play',param)
          url=globalvar.channels[channel][1].getVideoURL(channel,param)
          item = xbmcgui.ListItem(path=url)
          xbmcplugin.setResolvedUrl(addon_handle, True, item)  
      elif mode[0]=='Search':      
          log.logEvent(channel,'Search',param)
          keyboard = xbmc.Keyboard('','Enter the search text')
          keyboard.doModal()
          if (keyboard.isConfirmed()):
              buildShowsList(globalvar.channels[channel][1].list_videos(channel,keyboard.getText()))
      elif mode[0]=='bkm':      
          log.logEvent(channel,'Favs',param)
          if args['action'][0]=='add':#Add to Favourites
              display = args['display'][0]
              result=favourites.add_favourite(channel,param,display)
          else:
              result=favourites.rem_favourite(channel,param)
              xbmc.executebuiltin("XBMC.Container.Refresh")
          notify(result,channel)
      elif mode[0]=='dl':      
          log.logEvent(channel,'Download',param)
          if globalvar.dlfolder=='':
              notify('You need to set the download folder first', channel)
          else:
              url=globalvar.channels[channel][1].getVideoURL(channel,param)
              extensionStart=url.rfind('.')
              extension=url[extensionStart:len(url)].upper()
              if extension=='.MP4':            
                  fileName=utils.format_filename(args['name'][0]+'.mp4')
                  commondownloader.download(url, os.path.join(globalvar.dlfolder,fileName))
              else:
                  notify(extension + ' not supported', channel)
      xbmcplugin.endOfDirectory( handle=int(addon_handle), succeeded=True, updateListing=False)
except Exception as e:
  log.logError(args,e)