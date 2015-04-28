#-*- coding: utf-8 -*-
import urllib
import xml.dom.minidom    

title=['Gulli']
img=['gulli']
readyForUse=False

url_base='http://sslreplay.gulli.fr/replay/api?call=%7B%22api_key%22%3A%22andphone_72abef4bfc0c64d99b87b939ad32edf7%22%2C%22method%22%3A%22programme.getLatestEpisodes%22%2C%22params%22%3A%7B%22category_id%22%3A%22$$CATEG$$%22%2C%22episode_image_thumb%22%3A%5B285%2C213%5D%2C+%22episode_image_thumb_fiche%22%3A%5B0%2C0%5D%2C+%22program_image_thumb%22%3A%5B540%2C405%5D%2C+%22episode_image_fiche%22%3A%5B1080%2C810%5D%7D%7D'
url_basf='http://sslreplay.gulli.fr/replay/api?call=%7B%22api_key%22%3A%22andphone_72abef4bfc0c64d99b87b939ad32edf7%22%2C%22method%22%3A%22programme.getLatestEpisodes%22%2C%22params%22%3A%7B%22category_id%22%3A%22emissions%22%2C%22episode_image_thumb%22%3A%5B285%2C213%5D%2C+%22episode_image_thumb_fiche%22%3A%5B0%2C0%5D%2C+%22program_image_thumb%22%3A%5B540%2C405%5D%2C+%22episode_image_fiche%22%3A%5B1080%2C810%5D%7D%7D'
url_basd='http://sslreplay.gulli.fr/replay/api?call=%7B%22api_key%22%3A%22andphone_72abef4bfc0c64d99b87b939ad32edf7%22%2C%22method%22%3A%22programme.getLatestEpisodes%22%2C%22params%22%3A%7B%22category_id%22%3A%22series%22%2C%22episode_image_thumb%22%3A%5B285%2C213%5D%2C+%22episode_image_thumb_fiche%22%3A%5B0%2C0%5D%2C+%22program_image_thumb%22%3A%5B540%2C405%5D%2C+%22episode_image_fiche%22%3A%5B1080%2C810%5D%7D%7D'
def list_shows(channel,folder):
    shows=[]
    shows.append( [channel,'dessins-animes','Dessins Animes','','shows'] )
    shows.append( [channel,'emissiions','Emissions','','shows'] )
    shows.append( [channel,'series','Series et films','','shows'] )
    
    return shows

def getVideoURL(channel,url):
    html=urllib.urlopen(url).read()
    start=html.find('urlsVideoIPad: [')+17
    end=html.find('.m3u8:',start)
    return 'http://wat.tv/get/ipad/' + id + '.m3u8'
        
def list_videos(channel,category):
    videos=[] 
    dom = xml.dom.minidom.parse(urllib.urlopen(url_base.replace('$$CATEG$$',category)).read())
    ITEM=dom.getElementsByTagName('res')
    for nodeITEM in ITEM:
        title=nodeITEM.getElementsByTagName('program_title')
        infoLabels={ "Title": title} 
        videos.append( [channel,'url', title, '',infoLabels,'play'] )
    return videos