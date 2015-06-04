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
    shows.append( [channel,'158001', 'Webseries'.encode('utf-8') , '','folder'] )  
    shows.append( [channel,'158003', 'Parodies'.encode('utf-8') , '','folder'] )
    shows.append( [channel,'158004', 'Emissions dActu'.encode('utf-8') , '','folder'] )
    shows.append( [channel,'158005', 'Emissions Bonus'.encode('utf-8') , '','folder'] )
    shows.append( [channel,'158006', 'Stars'.encode('utf-8') , '','folder'] )
    
  else:
    if folder.find('/')==-1 :
      filePath=utils.downloadCatalog('http://www.allocine.fr/video/prgcat-%s/' % (folder),'allocine%s1.html' % (folder),False)    
      html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
      
      nbPages=1
      pagesString=re.findall('<ul><li>(.*?)</li> </ul>', html)
      if pagesString:
        pages=re.findall('<a href="(.*?)">(.*?)</a>', pagesString[0])
        if pages:
          nbPages=len(pages)+1
      
      for i in range(1, nbPages+1): 
        filePath=utils.downloadCatalog('http://www.allocine.fr/video/prgcat-%s/?page=%s' % (folder,i),'allocine%s%s.html' % (folder,i),False)    
        html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
        
        images=re.findall('<div class="pos_rel thumbs " > <span class="(.*?)"> <img(.*?)src=\'(.*?)\' /> </span> </div>', html)
        
        items=re.findall('<h2 class="title "> <a href="(.*?)">(.*?)</a> </h2>', html)
        j=0
        for item in items:
          if images[j][1]!=' ':
             image= images[j][1].replace(' data-attr=\'{"src":"','').replace('"}\'','')
          else:
            image=images[j][2] 
          shows.append( [channel,item[0], item[1] ,image ,'folder'] )
          j=j+1
    else:
      filePath=utils.downloadCatalog('http://www.allocine.fr%s/' % (folder),'allocine%s.html' % (folder.replace('/','')),False) 
      html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
      
      seasons=re.findall('<a class="button btn-primary btn-large" href="(.*?)">', html)
      for season in seasons:
        filePath=utils.downloadCatalog('http://www.allocine.fr%s/' % (season),'allocine%s.html' % (season.replace('/','')),False) 
        html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
        
        print html
      
      
  return shows