#-*- coding: utf-8 -*-
import urllib2
import re
import CommonFunctions
import base64
common = CommonFunctions 
from resources.lib import utils 
from bs4 import BeautifulSoup         

title=['CNES']
img=['cnes']
readyForUse=True

url_root = 'http://videotheque.cnes.fr'

def list_shows(channel,folder):
    shows=[]
    
    filePath=utils.downloadCatalog(url_root,channel + '.html',False,{})    
    html=open(filePath).read()

    if folder=='none':  
        match = re.compile(r'<div class="bottom">(.*?)<div class="titre"><div class="tiret1"><div class="titre_video"(.*?)">(.*?)</div></div><div class="titre_video"(.*?)">(.*?)</div>(.*?)<a href="(.*?)"><img src="(.*?)" alt=', re.DOTALL).findall(html)
        if match:
            for empty, empty2, title1, empty3, title2, empty4, link, img in match:
                title = title1 + title2

                title = " ".join(title.split())
                title = str(BeautifulSoup(title))

                link = url_root+link
                img = url_root+img
                shows.append( [channel,link+'|'+title, title , img,'shows'] )

  	return shows



def list_videos(channel,show): 
    
    videos=[]
    url_list = show.split('|')[0]
    title = show.split('|')[1]                                                                               
    
    another_page = True
    current_page = 1
    while another_page == True:
        url_page = url_list+'?&page='+str(current_page)
        filePath=utils.downloadCatalog(url_page ,channel +'_'+ title +'_'+str(current_page)+'.html',False,{})  
        html=open(filePath).read()

        if 'document.documentSelection.page.value='+str(current_page+1) in html:
            current_page += 1
        else:
            another_page = False

                                                       # empty         # year        #empty1        # duration     #empty2 #empty3 #title   #empty4 #desc      #empty5       #link       #empty6 
        match = re.compile(r'<div class="bloc_gauche_image">(.*?)<img src="(.*?)" border="0"(.*?)Date :</span>(.*?)</div>(.*?)Durée : </span>(.*?):(.*?):(.*?)</div>(.*?)<span(.*?)>(.*?)</span>(.*?)>(.*?)</span>(.*?)<a href="(.*?)" class=(.*?)',re.DOTALL).findall(html)

        if match:
            for empty0, img, empty, year, empty1, hour, minutes, seconds, empty2, empty3, title, empty4, desc, empty5, link, empty6 in match:
                link = url_root+"/"+link

                duration = int(hour)*3600 + int(minutes)*60 + int(seconds)
                #desc = " ".join(desc.split())
                date = "01/01/"+year
                infoLabels={ "Title": title, "Plot":desc, "Year":year, "Aired":date}
                videos.append( [channel, link, title, img,infoLabels,'play'] ) 

    return videos

def getVideoURL(channel,urlPage):
    urlPage = urlPage + "toto"
    match = re.compile(r'http(.*?)id_doc=(.*?)toto',re.DOTALL).findall(urlPage)
    id_doc = ''
    if match:
        for empty, id_d in match:
            id_doc = id_d
   
    url_api = 'https://videotheque.cnes.fr/empty.php?xmlhttp=1&urlaction=prepareVisu&method=QT&action=visu&pattern=_vis.mp4&id='+id_doc+'&type=document'
    html=urllib2.urlopen(url_api).read()
    url = ''
   
    match = re.compile(r'<mediaurl>(.*?)</mediaurl>',re.DOTALL).findall(html)
    if match:
        for url_mp4 in match:  
            url = url_mp4

    return url
