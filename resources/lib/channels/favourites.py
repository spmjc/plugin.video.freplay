#-*- coding: utf-8 -*-
from resources.lib import globalvar
import json
import os
import xbmcgui                         

title       = [globalvar.LANGUAGE(33007).encode('utf-8')]
img         = ['favourites']
readyForUse = True

def list_shows(channel,folder):
    shows=[] 
    if folder=='none':
        shows.append( [channel,'show_folder',globalvar.LANGUAGE(33000).encode('utf-8'),'','folder'] )
        shows.append( [channel,'unseen',globalvar.LANGUAGE(33001).encode('utf-8'),'','shows'] )
    elif folder=='show_folder':
        if os.path.exists(globalvar.FAVOURITES_FILE) :
            #Read favourites
            fileFav  = open(globalvar.FAVOURITES_FILE)
            jsonFav  = json.loads(fileFav.read())
            showsFav = jsonFav['favourites']
            fileFav.close()
            for show in showsFav :
                shows.append([x.encode('utf-8') for x in show])
    return shows

def list_videos(channel,show_title):
    videos=[]                
    if show_title=='unseen':
        if os.path.exists(globalvar.FAVOURITES_FILE) :
            #Read favourites
            fileFav = open(globalvar.FAVOURITES_FILE)
            jsonfav = json.loads(fileFav.read())
            pDialog = xbmcgui.DialogProgress()
            ret = pDialog.create(globalvar.LANGUAGE(33002).encode('utf-8'),'')
            i=1
            for show_folder in  jsonfav['favourites']:
                show_folder = [x.encode('utf-8') for x in show_folder]
                pDialog.update((i-1)*100/len(jsonfav['favourites']),globalvar.LANGUAGE(33003).encode('utf-8')+ show_folder[2] + ' - ' + str(i) + '/' +  str(len(jsonfav['favourites'])))
                videos+=(list_videos(show_folder[0],show_folder[1]));
                i+=1
            fileFav.close()
            pDialog.close()
    else:
        videos=globalvar.channels[channel][1].list_videos(channel,show_title) 
    return videos

def add_favourite(channel,param,display):
    result=''
    shows=list_shows('none','show_folder')
    for show in shows:
        if show[0]==channel and show[1]==param:
            result=globalvar.LANGUAGE(33004).encode('utf-8')
    if result=='':
        shows.append( [channel,param, display,'','shows'] )
        f1=open(globalvar.FAVOURITES_FILE, 'w+')
        print >>f1, json.dumps({'favourites': shows})
        result=globalvar.LANGUAGE(33005).encode('utf-8')
    return result

def rem_favourite(channel,param):
    result=''
    shows=list_shows('none','show_folder')
    for show in shows:
        if show[0]==channel and show[1]==param:
            shows.remove(show)
            f1=open(globalvar.FAVOURITES_FILE, 'w+')
            print >>f1, json.dumps({'favourites': shows})
            result=globalvar.LANGUAGE(33006).encode('utf-8')
    return result
    