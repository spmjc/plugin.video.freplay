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