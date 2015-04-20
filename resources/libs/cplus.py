import urllib,urllib2
import xml.dom.minidom
import globalvar
import json

def get_token():
    #Download Canal Catalog
    filPrgm=open(globalvar.CATALOG_CANAL).read()
    jsoncat     = json.loads(filPrgm)
    return jsoncat['token']

def list_shows(channel,folder):
    shows=[]
            
    if folder=='none':
        filPrgm=urllib2.urlopen('http://service.mycanal.fr/page/'+get_token()+'/1595.json').read()
        jsoncat     = json.loads(filPrgm)
        strates  = jsoncat['strates']
        for strate in strates :
            if strate['type']=='contentGrid':
                shows.append( [channel,strate['title'].encode('utf-8'), strate['title'].encode('utf-8'),'','folder'] )
    else:
        filPrgm=urllib2.urlopen('http://service.mycanal.fr/page/'+get_token()+'/1595.json').read()
        jsoncat     = json.loads(filPrgm)
        strates  = jsoncat['strates']
        for strate in strates :
            if strate['type']!='carrousel':
                if strate['title'].encode('utf-8')==folder:
                    contents  = strate['contents']
                    for content in contents:
                        shows.append( [channel,content['onClick']['URLPage'].replace(get_token(),'$$TOKEN$$').encode('utf-8'), content['title'].encode('utf-8'),content['URLImage'],'shows'] )
    
    return shows

def getVideoURL(channel,video_URL):
    filPrgm=urllib2.urlopen(video_URL).read()
    jsoncat     = json.loads(filPrgm)
    return jsoncat['detail']['informations']['VoD']['videoURL'].encode('utf-8')
    
def search(channel,keyWord):
    return list_shows(channel,keyWord)

def list_videos(channel,show_URL):
    videos=[] 
    
    show_URL=show_URL.replace('$$TOKEN$$',get_token())
    
    url=''
    title=''
    icon=''
    print show_URL
    filPrgm=urllib2.urlopen(show_URL).read()
    jsoncat     = json.loads(filPrgm)
    contents={}
    if 'contents' in jsoncat:	
        contents  = jsoncat['contents']
    else:
        strates  = jsoncat['strates']
        for strate in strates:
            if 'title' in strate:
	        if 'contents' in strate:
                    contents  = strate['contents']
                    break
    for content in contents:
	    
    	url=content['onClick']['URLPage'].encode('utf-8')
        if 'title' in content:
            title=content['title'].encode('utf-8')
        if 'subtitle' in content:
            title+=' - ' + content['subtitle'].encode('utf-8')
        icon=content['URLImage'].encode('utf-8')
        infoLabels={ "Title": title} 
        videos.append( [channel, url, title, icon,infoLabels,'play'] )
             
    return videos

