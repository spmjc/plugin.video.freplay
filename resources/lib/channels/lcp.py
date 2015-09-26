#-*- coding: utf-8 -*-
from resources.lib import utils
from resources.lib import globalvar
from bs4 import BeautifulSoup
import HTMLParser
html_parser = HTMLParser.HTMLParser()
import re

title       = ['LCP']
img         = ['lcp']
readyForUse = True

url_catalog = 'http://www.lcp.fr/spip.php?page=iphone-main'

def list_shows(channel,folder):
    shows    = []
    if folder=='none' :
        shows.append([channel,'shows',globalvar.LANGUAGE(33011),'','folder'])
        shows.append([channel,'reportages',globalvar.LANGUAGE(33010),'','shows'])
    else :
        filePath = utils.downloadCatalog(url_catalog,'%s.xml'%(channel),False,{})
        fileCat  = open(filePath).read().replace('\n','').decode('utf-8')
        cat      = re.findall('<key>'+folder+'</key> +<array> +(.+?) +</array>',fileCat)[0]
        shows_s  = re.findall('<dict> +(.+?) +</dict>',cat)
        for show in shows_s :
            show_title,show_thumb,show_infos,show_url = parse_dict(show)
            shows.append([channel,show_url,show_title,show_thumb,'shows'])
    return shows
            
def list_videos(channel,params):
    videos     = []
    if params=='reportages' :
        filePath = utils.downloadCatalog(url_catalog,'%s.xml'%(channel),False,{})
        fileCat  = open(filePath).read().replace('\n','').decode('utf-8')
        cat      = re.findall('<key>'+params+'</key> +<array> +(.+?) +</array>',fileCat)[0]
    else : 
        cat = utils.get_webcontent(params).replace('\n','').decode('utf-8')
    video_s  = re.findall('<dict> +(.+?) +</dict>',cat)
    for video in video_s :
        video_title,video_thumb,video_infos,video_url = parse_dict(video)
        videos.append([channel,video_url,video_title,video_thumb,video_infos,'play'])
    return videos
    
def getVideoURL(channel,url_video):
    return url_video
    
def parse_dict(dictText) :
    infos = {}
    try :
        infos['Thumb']   = html_parser.unescape(re.findall('<key>thumbnail_big</key> +<string>(.+?)</string>',dictText)[0]).encode('utf-8')
    except : 
        infos['Thumb']   = html_parser.unescape(re.findall('<key>thumbnail_small</key> +<string>(.+?)</string>',dictText)[0]).encode('utf-8')
    infos['Plot']        = BeautifulSoup(html_parser.unescape(re.findall('<key>full_description</key> +<string>(.+?)</string>',dictText)[0])).get_text().encode('utf-8')
    infos['PlotOutline'] = BeautifulSoup(html_parser.unescape(re.findall('<key>short_description</key> +<string>(.+?)</string>',dictText)[0])).get_text().encode('utf-8')
    title                = BeautifulSoup(html_parser.unescape(re.findall('<key>title</key> +<string>(.+?)</string>',dictText)[0])).get_text().encode('utf-8')
    url                  = html_parser.unescape(re.findall('<key>url</key> +<string>(.+?)</string>',dictText)[0]).encode('utf-8')
    return title,infos['Thumb'],infos,url