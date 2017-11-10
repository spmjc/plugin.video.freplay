#-*- coding: utf-8 -*-
import urllib2
import re      

title=['dps']
img=['dps']
readyForUse=False

def list_shows(channel,folder):
    shows=[]
            
    if folder=='none':
        shows.append( [channel,'HD', 'HD','','folder'] )
        shows.append( [channel,'Films', 'Films','','shows'] )
        shows.append( [channel,'Series', 'Series','','folder'] )
        shows.append( [channel,'Mangas', 'Mangas','','folder'] )
    else:
        req = urllib2.Request('http://sokrostream.biz/categories/films')
        req.add_header('User-agent', 'Mozilla 5.10')
        html=urllib2.urlopen(req).read()
        
        match = re.compile(r'<span class="tr-dublaj"></span><img src="(.*?)" alt="(.*?)" .*?<div class="movief"><a href="(.*?)">',re.DOTALL).findall(html)
        
        if match:
            for img,title,link in match:
                shows.append( [channel,link, title , img,'folder'] )
    
    return shows

def getVideoURL(channel,video_URL):
    req = urllib2.Request(video_URL+'/5')
    req.add_header('User-agent', 'Mozilla 5.10')
    html=urllib2.urlopen(req).read()
    match=re.compile('<IFRAME SRC="(.*?)" FRAMEBORDER',re.DOTALL).findall(html)
    youwatchurl=match[0]
    
    req = urllib2.Request(youwatchurl)
    html=urllib2.urlopen(req).read()
    html=html.replace('|','/')
    
    stream=re.compile('/mp4/video/(.+?)/(.+?)/(.+?)/setup',re.DOTALL).findall(html)
    for videoid,socket,server in stream:
        continue
    stream_url='http://'+server+'.youwatch.org:'+socket+'/'+videoid+'/video.mp4?start=0'
    return stream_url

def list_videos(channel,show_URL):
    videos=[] 

    req = urllib2.Request('http://sokrostream.biz/categories/films')
    req.add_header('User-agent', 'Mozilla 5.10')
    html=urllib2.urlopen(req).read()
    
    name=''
    image_url=''
    date=''
    duration=''
    views=''
    desc=''
    rating=''
    url=''
    
    match = re.compile(r'<span class="tr-dublaj"></span><img src="(.*?)" alt="(.*?)" .*?<div class="movief"><a href="(.*?)">',re.DOTALL).findall(html)
    
    if match:
        for image_url,name,url in match:
    
            infoLabels={ "Title": name,"Plot":desc,"Aired":date,"Duration": duration, "Year":date[:4]}   
            videos.append( [channel, url, name, image_url,infoLabels,'play'] )
    
    return videos