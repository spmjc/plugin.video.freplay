#-*- coding: utf-8 -*-
import urllib2
import simplejson as json

title       = ['iTélé']
img         = ['itele']
readyForUse = True

def list_shows(channel,folder):
    shows      = []
    urls = {'http://service.itele.fr/iphone/topnews':'A la une', 
        'http://service.itele.fr/iphone/categorie_news?query=france':'France',
        'http://service.itele.fr/iphone/categorie_news?query=monde':'Monde',
        'http://service.itele.fr/iphone/categorie_news?query=politique':'Politique',
        'http://service.itele.fr/iphone/categorie_news?query=justice':'Justice',
        'http://service.itele.fr/iphone/categorie_news?query=economie':'Economie',
        'http://service.itele.fr/iphone/categorie_news?query=sport':'Sport',
        'http://service.itele.fr/iphone/categorie_news?query=culture':'Culture',
        'http://service.itele.fr/iphone/categorie_news?query=insolite':'Insolite',
        'http://service.itele.fr/iphone/dernieres_emissions':'Dernières émissions'
        }
    for url,title in urls.iteritems():
        shows.append([channel,url,title,'','shows'])
    return shows
            
def list_videos(channel,url):
    videos     = []
    webcontent = get_webcontent(url)
    catalogue  = json.loads(webcontent)
    for key, value in catalogue.iteritems():
        for item in value :
            video_infos={}
            video_infos['Title'] = item['title'].encode('utf-8')
            video_infos['Plot']  = item['description'].encode('utf-8')
            video_infos['Genre'] = item['category'].encode('utf-8')
            video_infos['Thumb'] = item['preview']
            videos.append([channel,item['video_url'],video_infos['Title'],video_infos['Thumb'],video_infos,'play'])
    return videos
    
def getVideoURL(channel,video_url):
    return video_url

def get_webcontent(url):
    req  = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0.1')           
    req.add_header('Referer',url)
    webcontent = urllib2.urlopen(req).read()
    return webcontent
    
#                     
# 00:18:53 T:5204  NOTICE: uid - vnws1209671429713603
# 00:18:53 T:5204  NOTICE: video_url - http://us-cplus-aka.canal-plus.com/i/1504/22/nip_NIP_52076_,200k,400k,800k,1500k,.mp4.csmil/master.m3u8
# 00:18:53 T:5204  NOTICE: urgent - 0
# 00:18:53 T:5204  NOTICE: preview169 - http://cache.itele.fr/content/videos/120967/image1/mea1/5537b2c420f43nip-nip-52076-640x360-umpjt.jpg
# 00:18:53 T:5204  NOTICE: diaporama - None
# 00:18:53 T:5204  NOTICE: category - Cinema
# 00:18:53 T:5204  NOTICE: video_urlhautedefinition - http://vod-flash.canalplus.fr/WWWPLUS/STREAMING/1504/22/nip_NIP_52076_1500k.mp4
# 00:18:53 T:5204  NOTICE: video_urlhautdebit - http://vod-flash.canalplus.fr/WWWPLUS/STREAMING/1504/22/nip_NIP_52076_800k.mp4
# 00:18:53 T:5204  NOTICE: title - "Avengers 2" en avant-première à Londres
# 00:18:53 T:5204  NOTICE: video_urlmobile - http://vod-flash.canalplus.fr/WWWPLUS/STREAMING/1504/22/nip_NIP_52076_200k.mp4
# 00:18:53 T:5204  NOTICE: site_url - http://www.itele.fr/culture/video/avengers-2-en-avant-premiere-a-londres-120967
# 00:18:53 T:5204  NOTICE: preview - http://cache.itele.fr/content/videos/120967/image1/library/5537b2c420f43nip-nip-52076-640x360-umpjt.jpg
# 00:18:53 T:5204  NOTICE: id_pfv - 1252716
# 00:18:53 T:5204  NOTICE: video_urlhd - http://us-cplus-aka.canal-plus.com/i/1504/22/nip_NIP_52076_,200k,400k,800k,1500k,.mp4.csmil/master.m3u8
# 00:18:53 T:5204  NOTICE: enable_webview - False
# 00:18:53 T:5204  NOTICE: description - Scarlett Johansson, Chris Evans, Robert Downey Jr, les acteurs du troisième plus grand succès de l'histoire du cinéma étaient réunis à l'avant-première du film organisée à Londres mardi. Les super héros de l'univers Marvel reviennent pour la deuxième fois sur grand écran, dans cette histoire complexe intitulée "L'ère d'Ultron".
# 00:18:53 T:5204  NOTICE: video_urlbasdebit - http://vod-flash.canalplus.fr/WWWPLUS/STREAMING/1504/22/nip_NIP_52076_400k.mp4
# 00:18:53 T:5204  NOTICE: date - 2015-04-22 16:40:03
# 00:18:53 T:5204  NOTICE: emission_id - None
# 00:18:53 T:5204  NOTICE: emission_type - None
# 00:18:53 T:5204  NOTICE: preview_url - http://cache.itele.fr/media/videos/120967/image1/{WIDTH-HEIGHT}/5537b2c420f43nip-nip-52076-640x360-umpjt.jpg
# 00:18:53 T:5204  NOTICE: previewhd - http://cache.itele.fr/content/videos/120967/image1/iphoneHD/5537b2c420f43nip-nip-52076-640x360-umpjt.jpg
# 00:18:53 T:5204  NOTICE: category_id - CULTURE
