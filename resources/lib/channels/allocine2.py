#-*- coding: utf-8 -*-
import urllib2
import re
import CommonFunctions
common = CommonFunctions 
from resources.lib import utils     
from resources.lib import globalvar

title=['Allocine']
img=['allocine']
readyForUse=True

def list_shows(channel,folder):
  shows=[]
  
  if folder=='none' :                                                       
    shows.append( [channel,'ba', 'Bandes Annonces'.encode('utf-8') , '','folder'] )
    shows.append( [channel,'158001|1', 'Webseries'.encode('utf-8') , '','folder'] )
    shows.append( [channel,'158002|1', 'Mangas'.encode('utf-8') , '','folder'] )
    shows.append( [channel,'158003|1', 'Parodies'.encode('utf-8') , '','folder'] )
    shows.append( [channel,'158004|1', 'Emissions dActu'.encode('utf-8') , '','folder'] )
    shows.append( [channel,'158005|1', 'Emissions Bonus'.encode('utf-8') , '','folder'] )
    shows.append( [channel,'158006|1', 'Stars'.encode('utf-8') , '','folder'] )
    
  else:
    if folder=='ba':        
      shows.append( [channel,'video/bandes-annonces/|1', 'A ne pas manquer'.encode('utf-8') , '','shows'] )
      shows.append( [channel,'/bandes-annonces/plus-recentes/|1', 'Les plus recentes'.encode('utf-8') , '','shows'] )
      shows.append( [channel,'/bandes-annonces/prochainement/|1', 'Bientot au cinema'.encode('utf-8') , '','shows'] )
    else:    
      if 'programme' in folder:
        filePath=utils.downloadCatalog('http://www.allocine.fr/' + folder ,'allocine' + folder.replace('\\','') +'.html',False,{})
        html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
        
        match = re.compile(r'<a class="button btn-primary btn-large" href="(.*?)">(.*?)</a>',re.DOTALL).findall(html)
        for url,title in match:
          shows.append( [channel,url + '|1', title.replace("<i class='icon-sign-plus'></i>","") ,'' ,'shows'] )  
                  
      else:   
        cat,page=folder.split('|')
        filePath=utils.downloadCatalog('http://www.allocine.fr/video/prgcat-' + cat + '/?page=' + page ,'allocine' + cat + '-' + page +'.html',False,{})
        html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
        
        match = re.compile(r'btn-primary btn-large (.*?)">(.*?)<i class="icon-arrow-(.*?)"></i>',re.DOTALL).findall(html)
        prev=False
        next=False
        for status,empty,arrow in match:
          if arrow=='left':
            prev=('disabled' not in status)
          if arrow=='right':
            next=('disabled' not in status)
            
        if prev:
          shows.append( [channel,cat + '|' + str(int(page)-1), '<<Page Precedente' ,'' ,'folder'] )
              
        match = re.compile(r'<h2 class="title "> <span > <a href="(.*?)">(.*?)</a> </span> </h2>',re.DOTALL).findall(html)
        for url,title in match:                                                          
          shows.append( [channel,url, title ,'' ,'folder'] )
        
        if next :
          shows.append( [channel,cat + '|' + str(int(page)+1), 'Page Suivante>>' ,'' ,'folder'] )
                             
      
  return shows          
  
def list_videos(channel,folder):  
  cat,page=folder.split('|')
    
  videos=[]
  filePath=utils.downloadCatalog('http://www.allocine.fr/' + cat + '/?page=' + page ,'allocine' + cat + '-' + page +'.html',False,{})
  html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
  
  match = re.compile(r'btn-primary btn-large (.*?)">(.*?)<i class="icon-arrow-(.*?)"></i>',re.DOTALL).findall(html)
  prev=False
  next=False
  for status,empty,arrow in match: 
    if arrow=='left':
      prev=('disabled' not in status)
    if arrow=='right':
      next=('disabled' not in status)
      
  if prev:
    shows.append( [channel,cat + '-' + str(int(page)-1), '<<Page Precedente' ,'',{} ,'folder'] )
  
  match = re.compile(r'<div class="layer-link-holder"><a href="/video/player_gen_cmedia=(.*?)&amp;cfilm=(.*?).html" class="layer-link">(.*?)</a></div>',re.DOTALL).findall(html)
  if match:
    for id,movie,title in match:
      title=title.replace('<strong>','').replace('</strong>','')
      infoLabels={ "Title": title}
      videos.append( [channel, id , title , '',infoLabels,'play'] )  
   
  match = re.compile(r'<h3 class="title "> <span > <a href="/video/video-(.*?)/" itemprop="url">(.*?)</a> </span> </h3>',re.DOTALL).findall(html) 
  if match:
    for idVideo,title in match:
      title=title.replace('<strong>','').replace('</strong>','')
      infoLabels={ "Title": title}
      videos.append( [channel, idVideo , title , '',infoLabels,'play'] )  
    
  if next :
    shows.append( [channel,cat + '-' + str(int(page)+1), 'Page Suivante>>' ,'',{} ,'folder'] )
  
  return videos

def getVideoURL(channel,idVideo):
  filePath=utils.downloadCatalog('http://www.allocine.fr/ws/AcVisiondataV4.ashx?media=%s' % (idVideo),'allocine%s.xml' % (idVideo),False,{}) 
  xml=open(filePath).read()
  
  
  ld=re.findall('ld_path="(.*?)"', xml)[0]
  md=re.findall('md_path="(.*?)"', xml)[0]
  hd=re.findall('hd_path="(.*?)"', xml)[0]
  return hd