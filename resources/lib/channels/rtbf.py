# -*- coding: utf-8 -*-

from resources.lib import utils
import re

title = ['RTBF Auvio']
img = ['rtbf']
readyForUse = True

url_root = 'http://www.rtbf.be/auvio'

categories = {
    '/categorie/series?id=35': 'Séries',
    '/categorie/sport?id=9': 'Sport',
    '/categorie/divertissement?id=29': 'Divertissement',
    '/categorie/culture?id=18': 'Culture',
    '/categorie/films?id=36': 'Films',
    '/categorie/sport/football?id=11': 'Football',
    '/categorie/vie-quotidienne?id=44': 'Vie quotidienne',
    '/categorie/musique?id=23': 'Musique',
    '/categorie/info?id=1': 'Info',
    '/categorie/humour?id=40': 'Humour',
    '/categorie/documentaires?id=31': 'Documentaires',
    '/categorie/enfants?id=32': 'Enfants'
}


def list_shows(channel, param):
  shows = []
  if param == 'none':
    for url, title in categories.iteritems():
      shows.append([channel,url,title,'','shows'])
  return shows
    
def list_videos(channel, cat_url):  
  videos = []
  cat=cat_url[2:]  
  filePath=utils.downloadCatalog(url_root + cat_url ,'rtbf' + cat + '.html',False,{})
  html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
  match = re.compile(r'<h3 class="rtbf-media-item__title "><a href="(.*?)" title="(.*?)">',re.DOTALL).findall(html)
  for url,title in match:
    title=utils.formatName(title)   
    infoLabels={ "Title": title}
    videos.append( [channel, url , title , '',infoLabels,'play'] )

  return videos

def getVideoURL(channel, url_video):
    html = utils.get_webcontent(url_video).replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
    url=re.findall(r'<meta property="og:video" content="(.*?).mp4"', html)[0]
    return url+'.mp4'
