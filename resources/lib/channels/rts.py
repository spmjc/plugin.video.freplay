#-*- coding: utf-8 -*-
import json       
import urllib,urllib2
import resources.lib.utils as utils 
from resources.lib import globalvar          

title       = ['RTS']
img         = ['rts']
readyForUse = True

urlCatalog = 'http://il.srgssr.ch/integrationlayer/1.0/ue/rts/tv/topic.json'
showsList       = 'http://il.srgssr.ch/integrationlayer/1.0/ue/rts/video/editorialPlayerLatestByTopic/%s.json'
urlVideo         = 'http://il.srf.ch/integrationlayer/1.0/ue/rts/video/play/%s.json'
imgFormat='/scale/width/512'

def list_shows(channel,folder):  
  shows      = []       
  uniqueItem = dict()  
          
  if folder=='none':
    filePath   = utils.downloadCatalog(urlCatalog ,'rts.json',False,{})  
    filPrgm    = open(filePath).read()
    jsonParser = json.loads(filPrgm)   
    topics  = jsonParser['Topics']['Topic']
    for topic in topics :           
      shows.append( [channel,topic['id'], topic['title'].encode('utf-8'),'','folder'] )  
  else:        
    filePath   = utils.downloadCatalog(showsList % folder ,'rts%s.json' % folder,False,{})  
    filPrgm    = open(filePath).read()
    jsonParser = json.loads(filPrgm)   
    videos  = jsonParser['Videos']['Video']
    for video in videos :    
      print video  
      idSet=video['AssetSet']['Show']['id']
      if idSet not in uniqueItem:
        uniqueItem[idSet]=idSet
        imgURL=video['AssetSet']['Show']['Image']['ImageRepresentations']['ImageRepresentation'][0]['url']+imgFormat    
        shows.append( [channel,folder + '-' + idSet, video['AssetSet']['title'].encode('utf-8'),imgURL.encode('utf-8'),'shows'] )
      
  return shows
  
def list_videos(channel,folderIdSet):
  shows     = []   
   
  params= folderIdSet.split('-')
  folder=params[0]
  paramIdSet=params[1]
  
  filePath   = utils.downloadCatalog(showsList % folder ,'rts%s.json' % folder,False,{})  
  filPrgm    = open(filePath).read()
  jsonParser = json.loads(filPrgm)   
  videos  = jsonParser['Videos']['Video']
  for video in videos :      
    print video 
    idSet=video['AssetSet']['Show']['id']
    if idSet==paramIdSet:
      imgURL=video['Image']['ImageRepresentations']['ImageRepresentation'][0]['url']+imgFormat    
      titre=video['AssetSet']['Show']['title'].encode('utf-8') + '-' +  video['AssetMetadatas']['AssetMetadata'][0]['title'].encode('utf-8') 
      description=video['AssetMetadatas']['AssetMetadata'][0]['description'].encode('utf-8')    
      assetId=video['AssetMetadatas']['AssetMetadata'][0]['assetId']        
      infoLabels = { "Title": titre,"Plot":description}
      shows.append( [channel, assetId, titre, imgURL.encode('utf-8'),infoLabels,'play'] )    
  return shows    
  
def getVideoURL(channel,assetId): 
  filPrgm    = utils.get_webcontent(urlVideo % assetId)      
  jsonParser = json.loads(filPrgm)   
  for plst in jsonParser['Video']['Playlists']['Playlist']:
    if plst['@protocol']=='HTTP-HLS':
      for url in plst['url']:
        if url['@quality']=='HD':
          return url['text']