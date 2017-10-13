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
    shows.append( [channel,'158001-1', 'Webseries'.encode('utf-8') , '','folder'] )
    shows.append( [channel,'158002-1', 'Mangas'.encode('utf-8') , '','folder'] )
    shows.append( [channel,'158003-1', 'Parodies'.encode('utf-8') , '','folder'] )
    shows.append( [channel,'158004-1', 'Emissions dActu'.encode('utf-8') , '','folder'] )
    shows.append( [channel,'158005-1', 'Emissions Bonus'.encode('utf-8') , '','folder'] )
    shows.append( [channel,'158006-1', 'Stars'.encode('utf-8') , '','folder'] )
    
  else:
    if folder=='ba':        
      shows.append( [channel,'/bandes-annonces/', 'A ne pas manquer'.encode('utf-8') , '','folder'] )
      shows.append( [channel,'/bandes-annonces/plus-recentes/', 'Les plus recentes'.encode('utf-8') , '','folder'] )
      shows.append( [channel,'/bandes-annonces/prochainement/', 'Bientot au cinema'.encode('utf-8') , '','folder'] )
    else:
      cat,page=folder.split('-')
      filePath=utils.downloadCatalog('http://www.allocine.fr/video/prgcat-' + cat + '/?page=' + page ,'allocine' + cat + '-' + page +'.html',False,{})
      html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
      
      match = re.compile(r'btn-primary btn-large (.*?)">(.*?)<i class="icon-arrow-(.*?)"></i>',re.DOTALL).findall(html)
      for status,empty,arrow in match:
        print status + '-' + arrow
        if arrow=='left':
          prev=('disabled' not in status)
        if arrow=='right':
          next=('disabled' not in status)
          
      if prev:
        shows.append( [channel,cat + '-' + str(int(page)-1), '<<Page Precedente' ,'' ,'folder'] )
            
      match = re.compile(r'<h2 class="title "> <span > <a href="(.*?)">(.*?)</a> </span> </h2>',re.DOTALL).findall(html)
      for url,title in match:                                                          
        shows.append( [channel,url, title ,'' ,'shows'] )
      
      if next :
        shows.append( [channel,cat + '-' + str(int(page)+1), 'Page Suivante>>' ,'' ,'folder'] )
                             
      
  return shows