import globalvar
import json
import os
import xbmcgui

def list_shows(channel,folder):
    shows=[]
    if folder=='none':
        shows.append( [channel,'show_folder', 'By Show','','folder'] )
        shows.append( [channel,'unseen', 'All Unseen Episodes','','shows'] )
    elif folder=='show_folder':
        if os.path.exists(globalvar.FAVOURITES_FILE) :
            #Read favourites
            fileFav=open(globalvar.FAVOURITES_FILE)
            jsonfav     = json.loads(fileFav.read())
            shows  = jsonfav['favourites']
            fileFav.close()
    return shows

def list_videos(channel,show_title):
    videos=[]
    if show_title=='unseen':
        if os.path.exists(globalvar.FAVOURITES_FILE) :
            #Read favourites
            fileFav=open(globalvar.FAVOURITES_FILE)
            jsonfav     = json.loads(fileFav.read())
            pDialog = xbmcgui.DialogProgress()
            ret = pDialog.create( 'Getting list of episodes', '' )
            i=1
            for show_folder in  jsonfav['favourites']:
                pDialog.update((i-1)*100/len(jsonfav['favourites']), 'Checking shows: '+ show_folder[2] + ' - ' + str(i) + '/' +  str(len(jsonfav['favourites'])))
                videos+=(list_videos(show_folder[0],show_folder[1]));
                i+=1
            fileFav.close()
            
            pDialog.close()
    else:
        print str(channel) + ' : ' + show_title
        videos=globalvar.channels[channel][1].list_videos(channel,show_title) 
    return videos

def add_favourite(channel,param,display):
    result=''
    shows=list_shows('none','show_folder')
    for show in shows:
        if show[0]==channel and show[1]==param:
            result='Show already in list'
    if result=='':
        shows.append( [channel,param, display,'','shows'] )
        f1=open(globalvar.FAVOURITES_FILE, 'w+')
        print >>f1, json.dumps({'favourites': shows})
        result='Show added to Favourites'
    
    return result

def rem_favourite(channel,param):
    result=''
    shows=list_shows('none','show_folder')
    for show in shows:
        print str(channel) + ':' + param
        print str(show[0]) + ':' + show[1]
        if show[0]==channel and show[1]==param:
            shows.remove(show)
            f1=open(globalvar.FAVOURITES_FILE, 'w+')
            print >>f1, json.dumps({'favourites': shows})
            result='Removed From Favourites'
            
    return result
    