#-*- coding: utf-8 -*-
import urllib2
import re
import CommonFunctions
common = CommonFunctions 
from resources.lib import utils     
from resources.lib import globalvar

title=['Allocine']
img=['allocine']
readyForUse=False

def list_shows(channel,folder):
  shows=[]
  
  if folder=='none' :                                                       
    shows.append( [channel,'ba', 'Bandes Annonces'.encode('utf-8') , '','folder'] )
    shows.append( [channel,'158003', 'Parodies'.encode('utf-8') , '','folder'] )
    shows.append( [channel,'158004', 'Emissions dActu'.encode('utf-8') , '','folder'] )
    shows.append( [channel,'158005', 'Emissions Bonus'.encode('utf-8') , '','folder'] )
    
  else:
    if folder=='ba':        
      shows.append( [channel,'/bandes-annonces/', 'A ne pas manquer'.encode('utf-8') , '','folder'] )
      shows.append( [channel,'/bandes-annonces/plus-recentes/', 'Les plus recentes'.encode('utf-8') , '','folder'] )
      shows.append( [channel,'/bandes-annonces/prochainement/', 'Bientot au cinema'.encode('utf-8') , '','folder'] )
    
    
    elif folder.find('/')==-1 or  folder.find('bandes-annonces')!=-1:
      if folder.find('bandes-annonces')!=-1:          
        filePath=utils.downloadCatalog('http://www.allocine.fr/video%s' % (folder),'allocine%s1.html' % (folder),False,{}) 
      else:
        filePath=utils.downloadCatalog('http://www.allocine.fr/video/prgcat-%s/' % (folder),'allocine%s1.html' % (folder),False,{})    
      html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
      nbPages=1
      pages=re.findall('<li><a href="(.*?)">(.*?)</a></li>', html)
      if pages:
        nbPages=len(pages)+1
      for i in range(1, nbPages+1): 
        if folder.find('bandes-annonces')!=-1:          
          filePath=utils.downloadCatalog('http://www.allocine.fr/video%s?page=%s' % (folder,i),'allocine%s%s.html' % (folder,i),False,{}) 
        else:
          filePath=utils.downloadCatalog('http://www.allocine.fr/video/prgcat-%s/?page=%s' % (folder,i),'allocine%s%s.html' % (folder,i),False,{})
        
        html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
        
        images=re.findall('<div class="pos_rel thumbs.*?" > <span class="(.*?)"> <img(.*?)src=\'(.*?)\' /> </span> </div>', html)
        
        items=re.findall('<h2 class="title "> <span > <a href="(.*?)">(.*?)</a>', html)
        print html
        j=0
        image=''
        for item in items:
          if images[j][1]!=' ':
             image= images[j][1].replace(' data-attr=\'{"src":"','').replace('"}\'','')
          else:
            image=images[j][2]
          if folder.find('bandes-annonces')!=-1: 
            videoId=re.findall('player_gen_cmedia=(.*?)&cfilm',item[0])[0]   
            infoLabels={ "Title": formatTitle(item[1])}
            shows.append( [channel, videoId, formatTitle(item[1]), image,'play'] )   
          else:        
            shows.append( [channel,item[0], formatTitle(item[1]) ,image ,'folder'] )
          j=j+1
    else:
      filePath=utils.downloadCatalog('http://www.allocine.fr%s' % (folder),'allocine%s.html' % (folder),False,{})
      html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
                                                                                                                                 
      seasons=re.findall('<a class="button btn-primary btn-large" href="(.*?)">(.*?)</a>', html)
      for season in seasons:                                                          
        shows.append( [channel,season[0], formatTitle(season[1]) ,'' ,'shows'] )
              
  return shows
  
def list_videos(channel,show_url):
  videos=[] 
  
  filePath=utils.downloadCatalog('http://www.allocine.fr%s' % (show_url),'allocine%s.html' % (show_url.replace('/','')),False,{}) 
  html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
  
  items=re.findall('<h3 class="title "> <span > <a href="/video/video-(.*?)/" itemprop="url">(.*?)</a>', html)
  for item in items:        
    infoLabels={ "Title": formatTitle(item[1])}
    videos.append( [channel, item[0], formatTitle(item[1]), '',infoLabels,'play'] )      
  
  return videos       

def getVideoURL(channel,idVideo):
  filePath=utils.downloadCatalog('http://www.allocine.fr/ws/AcVisiondataV4.ashx?media=%s' % (idVideo),'allocine%s.xml' % (idVideo),False,{}) 
  xml=open(filePath).read()
  
  
  ld=re.findall('ld_path="(.*?)"', xml)[0]
  md=re.findall('md_path="(.*?)"', xml)[0]
  hd=re.findall('hd_path="(.*?)"', xml)[0]
  return hd
  
def formatTitle(str):
  return str.replace('<strong>','').replace('</strong>','').replace('<i class=\'icon-sign-plus\'></i>','')