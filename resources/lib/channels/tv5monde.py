#-*- coding: utf-8 -*-
import urllib2
import re
import CommonFunctions
import base64
common = CommonFunctions 
from resources.lib import utils          

title=['TV5 Monde']
img=['tv5monde']
readyForUse=True

url_root = 'http://mobile.tv5mondeplus.com'

def list_shows(channel,folder):
    shows=[]
    
    filePath=utils.downloadCatalog(url_root+'/menu/',channel + '.html',False,{})    
    html=open(filePath).read()

    if folder=='none':  
        match1 = re.compile(r'<ul data-role="listview" data-theme="a">(.*?)</ul>', re.DOTALL).findall(html)
        if match1:  
            match = re.compile(r'<li>(.*?)<a href="(.*?)">(.*?)</a>(.*?)</li>',re.DOTALL).findall(match1[0])
            if match:
                for empty, link, title, empty2    in match:
                  title = " ".join(title.split())
                  title = title.capitalize()
                  link = url_root+link
                  #img = url_root+img
                  shows.append( [channel,link+'|'+title, title , '','shows'] )

  	return shows




def get_mounth_number(original_name):
    Dic = {"janv."          :"01",
         "févr."            :"02",
         "mars"             :"03",
         "avr."             :"04",
         "mai"              :"05",
         "juin"             :"06",
         "juill."           :"07",
         "août"             :"08",
         "sept."            :"09",
         "oct."             :"10",
         "nov."             :"11",
         "déc."             :"12",
         }
    for key,value in Dic.iteritems():
        if original_name==key : return value
    return original_name

def list_videos(channel,show): 
    
    videos=[]
    link = show.split('|')[0]
    title = show.split('|')[1]                                                                               
    filePath=utils.downloadCatalog(link ,channel +'_'+ title +'.html',False,{})  
    html=open(filePath).read()
  
    match = re.compile(r'<li data-icon="false">(.*?)<a href="(.*?)">(.*?)<img src="(.*?)"/>(.*?)<p class="ui-li-aside">(.*?)</p>(.*?)<h3>(.*?)</h3>(.*?)<p>(.*?)</p>(.*?)</li>',re.DOTALL).findall(html)

    if match:
      for empty1, link, empty2, img, empty3, date, empty4, title, empty5, desc, empy6 in match:
        link = url_root+link
        
        desc = " ".join(desc.split())
        date = date.split()
        day = date[0]
        mounth = get_mounth_number(date[1])
        year = date[2]
        date2 = day+"/"+mounth+"/"+year
        infoLabels={ "Title": title, "Plot":desc, "Aired":date2, "Year":year}
        videos.append( [channel, link, title, img,infoLabels,'play'] ) 

    return videos


def getVideoURL(channel,urlPage):
    html=urllib2.urlopen(urlPage).read()
    url = ''
    match = re.compile(r'<video data-role="video"(.*?)src="(.*?)"',re.DOTALL).findall(html)
    if match:
        for empty1, src in match:  
            url=src

    return url
