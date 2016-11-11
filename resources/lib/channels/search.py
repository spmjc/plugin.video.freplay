#-*- coding: utf-8 -*-   
import xbmc, xbmcgui            
import os
import resources.lib.globalvar as globalvar


title=['Search']
img=['search']

readyForUse=False        

def list_shows(channel,folder):
  shows=[]                                
  progress = xbmcgui.DialogProgress()
  progress.create('Progress', 'This is a progress bar.')
  i=0
  for item in globalvar.ordered_channels:   
    chan_id=item[0]
    chan_title=globalvar.channels[item[0]][0]     
        
    if chan_id!='favourites' and chan_id!='mostviewed' and chan_id!=channel:

      percent = int( ( i / len(globalvar.channels)-3 ) * 100)
      message = chan_title + str( i ) + '-' + str(len(globalvar.channels)-3) + '-' + str(i / (len(globalvar.channels)-3 ))
      progress.update( percent, "", message, "" )
      if progress.iscanceled():
        break    
        
      shows.append( [channel,chan_id, chan_title , os.path.join( globalvar.MEDIA, chan_id +".png"),'shows'] )
      shows_channel=globalvar.channels[chan_id][1].list_shows(chan_id,'none') 
      shows.extend(shows_channel)
      i = i + 1
        
  progress.close()
  return shows