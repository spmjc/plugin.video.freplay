#-*- coding: utf-8 -*-
import urllib2
import json
import CommonFunctions
common = CommonFunctions
from xml.dom import minidom
from resources.lib import utils           

title=['ARTE']
img=['arte']
readyForUse=True

def fix_text(text): 
  return text.replace('&amp;','&').encode('utf-8').replace('&#039;',' ')

def list_shows(channel,folder):
    shows=[]
    d=dict()
    
    filePath=utils.downloadCatalog('http://www.arte.tv/papi/tvguide-flow/sitemap/feeds/videos/F.xml','ARTE.XML',False)
    if folder=='none':
        xml = open(filePath).read()
        url=common.parseDOM(xml, "url")
        for i in range(0, len(url)):
            categoryTab=common.parseDOM(url[i], "video:category")
            if len(categoryTab)>0:
                category=fix_text(categoryTab[0])
                if category not in d:
                    shows.append( [channel,category,category,'','folder'] )
                    d[category]=category
    else:
        xml = open(filePath).read()
        url=common.parseDOM(xml, "url")
        for i in range(0, len(url)):
            titleTab=common.parseDOM(url[i], "video:title")
            if len(titleTab)>0:
                title=fix_text(titleTab[0])
            categoryTab=common.parseDOM(url[i], "video:category")
            if len(categoryTab)>0:
                if(fix_text(categoryTab[0])==folder and title not in d):                   
                    shows.append( [channel,title,title,'','shows'] )
                    d[title]=title
    return shows

def getVideoURL(channel,video_id):
    #Get JSON file
    jsonFile=urllib2.urlopen('http://arte.tv/papi/tvguide/videos/stream/player/F/'+ video_id + '/ALL/ALL.json').read()
    #Parse JSON to
    jsoncat = json.loads(jsonFile)
    url=jsoncat['videoJsonPlayer']['VSR']['HLS_SQ_1']['url']
    return url
    
def list_videos(channel,show_title):
    videos=[]                
    filePath=utils.downloadCatalog('http://www.arte.tv/papi/tvguide-flow/sitemap/feeds/videos/F.xml','ARTE.XML',False)
    xml = open(filePath).read()	
    url=common.parseDOM(xml, "url")
    
    for i in range(0, len(url)):   

        titleTab=common.parseDOM(url[i], "video:title")
        if len(titleTab)>0:
            title=fix_text(titleTab[0])
        if(title==show_title):       

            name=''
            image_url=''
            date=''
            duration=''
            views=''
            desc=''
            rating=''
            tmpTab=common.parseDOM(url[i], "video:publication_date")
            if len(tmpTab)>0:
                date=tmpTab[0][:10]
            tmpTab=common.parseDOM(url[i], "video:duration")
            if len(tmpTab)>0:
                duration=float(tmpTab[0])/60
            tmpTab=common.parseDOM(url[i], "video:view_count")
            if len(tmpTab)>0:
                views=tmpTab[0]
            tmpTab=common.parseDOM(url[i], "video:rating")
            if len(tmpTab)>0:
                rating=tmpTab[0]
            
            descriptionTab=common.parseDOM(url[i], "video:description")
            if len(descriptionTab)>0:
                name=fix_text(descriptionTab[0])
                desc=fix_text(descriptionTab[0])
                    
            tmpTab=common.parseDOM(url[i],"video:player_loc")
            if len(tmpTab)>0:
                if tmpTab[0]=="1":
                    tmpTab=common.parseDOM(url[i], "video:id")
                    if len(tmpTab)>0:
                        video_id=tmpTab[0][28:28+10] + "_PLUS7-F"
                else:
                    start=tmpTab[0].find("%2Fplayer%2FF%2F")
                    end=tmpTab[0].find("%2F", start+16)
                    video_id=tmpTab[0][start+16:end]
                    if video_id.find("EXTRAIT")>0 :
                        name="Extrait-" + name
           
            picTab=common.parseDOM(url[i], "video:thumbnail_loc")
            if len(picTab)>0:
                image_url=picTab[0]

                infoLabels={ "Title": name,"Plot":desc,"Aired":date,"Duration": duration, "Year":date[:4]}   
                videos.append( [channel, video_id, name, image_url,infoLabels,'play'] )
    return videos