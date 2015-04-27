#-*- coding: utf-8 -*-
import urllib
import xml.dom.minidom
import os
from resources.lib import globalvar

title=['M6']
img=['msix']
readyForUse=False

url_catalogue='http://static.m6replay.fr/catalog/m6group_ipad/m6replay/catalogue.xml'

def list_shows(channel,folder):
    shows=[]
    

    if folder=='none':
        shows.append( [channel,'emissions', 'Emissions','','shows'] )

    return shows

def getVideoURL(channel,video_URL):
    return video_URL

def list_videos(channel,show_URL):
    videos=[]
    url='http://vod-and.llnw.cdn.m6web.fr/phls-vod/Bones_c11359058_Saison-9-episode-11_600k.mp4.m3u8'
    infoLabels={ "Title": 'test'} 
    videos.append( [channel, url, 'test', '',infoLabels,'play'] )
    return videos