import urllib,urllib2
import xml.etree.ElementTree as ET
import json

title=['D8','D17']
img=['D8','D17']
readyForUse=True

def list_shows(channel,folder):
    shows=[]
    filPrgm=urllib2.urlopen("http://static2.canalplus.fr/config_applications/" + channel +"/prodv1/" + channel +"Start_iPhone.json").read()
    jsoncat     = json.loads(filPrgm)
    strates  = jsoncat[0]['nomenclature']
    if folder=='none':
        for strate in strates :
            shows.append( [channel,strate['title'].encode('utf-8'), strate['title'].encode('utf-8'),'','folder'] )
    else:
        for strate in strates :
            if strate['title'].encode('utf-8')==folder:
                for topic in strate['content']:
                    shows.append( [channel,topic['targetURL'].encode('utf-8'), topic['title'].encode('utf-8'),'','shows'] )
    return shows

def getVideoURL(channel,video_URL):
    print video_URL
    video_URL="http://us-cplus-aka.canal-plus.com/i/geo2/1504/10/nip_NIP_50689_,200k,400k,800k,1500k,.mp4.csmil/master.m3u8"
    return video_URL
    
def search(channel,keyWord):
    return list_shows(channel,keyWord)

def list_videos(channel,show_URL):
    videos=[] 

    xml = urllib2.urlopen("http://service.canal-plus.com/video/rest/listeVideos/" + channel.lower() + "/"+show_URL).read()  
    root = ET.fromstring(xml)
    
    for contenu in root.findall('CONTENU'):
        name=''
        image_url=''
        date=''
        duration=''
        views=''
        desc=''
        rating=''
        url=''
        
        name = contenu.find('TITRE').text.encode('utf-8') + ' - ' + contenu.find('SOUS-TITRE').text.encode('utf-8')
        date=contenu.find("DATE_DIFFUSION").text
        duration=float(contenu.find("DURATION").text)/60
        views=contenu.find("NB_VUES").text
        desc=contenu.find("DESCRIPTION").text.encode('utf-8')
        rating=contenu.find("NOTE").text
        for elem in contenu.find("IMAGE").iterfind("URL"):
            if elem.get("TAILLE")=="GRANDE":
                image_url=elem.text.encode('utf-8')
        for elem in contenu.find("VIDEO").iterfind("URL"):
            if elem.get("TAILLE")=="HD":
                url=elem.text.encode('utf-8')
        
        infoLabels={ "Title": name,"Plot":desc,"Aired":date,"Duration": duration, "Year":date[:4]}   
        videos.append( [channel, url, name, image_url,infoLabels,'play'] )
    
    return videos

