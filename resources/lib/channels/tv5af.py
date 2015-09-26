#-*- coding: utf-8 -*-
import urllib2
import json
import CommonFunctions
common = CommonFunctions
from resources.lib import utils        

title=['TV5+ Afrique']
img=['tv5af']
readyForUse=True

urlIMG='http://vodflash.tv5monde.com/webtv_afrique/vignettes/%s.jpg'
urlVideo='http://vodflash.tv5monde.com/tv_conn/1/afrique/%s.mp4'

def list_shows(channel,folder):
  shows=[]
  dType=dict()
  dTitre=dict()
  
  filePath=utils.downloadCatalog('http://www.tv5mondeplusafrique.com/dotscreen/exportAfrique.xml','TV5AF.XML',False,{})
  xml = open(filePath).read()
  item=common.parseDOM(xml, "item")
  lids = common.parseDOM(xml, "item", ret = "lid")
  if folder=='none':
    for i in range(0, len(item)):
      types=common.parseDOM(item[i], "type")
      if len(types)>0:
        type=types[0]
        type=type[9:-3].replace('Episode ','')
        if type not in dType:
          shows.append( [channel,type,type,'','folder'] )
          dType[type]=type
  else:     
    for i in range(0, len(item)):
      types=common.parseDOM(item[i], "type")
      if len(types)>0:
        type=types[0]
        type=type[9:-3].replace('Episode ','')
        if type==folder:
          titres=common.parseDOM(item[i], "titre")
          if len(titres)>0:
            titre=titres[0]
            titre=titre[9:-3]
            if '-EP' in titre:
              titre=titre[:titre.find('-EP')]
            if titre not in dTitre:
              shows.append( [channel,titre,titre,urlIMG % (lids[i]),'shows'] )
              dTitre[titre]=titre
    
  return shows
  
def list_videos(channel,show_title):
  videos=[]                
  filePath=utils.downloadCatalog('http://www.tv5mondeplusafrique.com/dotscreen/exportAfrique.xml','TV5AF.XML',False,{})
  xml = open(filePath).read()
  item=common.parseDOM(xml, "item")
  lids = common.parseDOM(xml, "item", ret = "lid")
  
  for i in range(0, len(item)):
    titres=common.parseDOM(item[i], "titre")
    if len(titres)>0:
      titre=titres[0]
      titre=titre[9:-3]
      if '-EP' in titre:
        titreFilter=titre[:titre.find('-EP')]
        titre=titre[titre.find('-EP')+1:]
        
    if titreFilter==show_title:
      plots=common.parseDOM(item[i], "descriptif")
      if len(plots)>0:
        plot=plots[0]
        plot=plot[9:-3] 
        
      durees=common.parseDOM(item[i], "duree")
      if len(durees)>0:
        sDuree=durees[0]
        duree=int(sDuree[0:2])*60+int(sDuree[3:5])
        
      dates=common.parseDOM(item[i], "dateCreation")
      if len(dates)>0:
        date=dates[0]
    
      infoLabels={ "Title": titre,"Plot":plot,"Aired":date,"Duration": duree}
      videos.append( [channel, lids[i], titre.encode('utf-8'), urlIMG % (lids[i]),infoLabels,'play'] )
  return videos
  
def getVideoURL(channel,video_id):
  return urlVideo % (video_id)