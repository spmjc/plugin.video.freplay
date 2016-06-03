#-*- coding: utf-8 -*-    
from resources.lib import utils
import json                   
import urllib,urllib2

title=['Tou.tv']
img=['toutv']
readyForUse=True          

urlCatalog='http://ici.tou.tv/presentation/section/rattrapage?v=2&d=ipad&includePartnerTeaser=false'

def canPlay(item):
  if item['IsFree'] and item['IsActive']:
    return True

def list_shows(channel,param):  
  shows=[]
  
  filePath=utils.downloadCatalog(urlCatalog,'TouTV.json',False,{}) 
  filPrgm=open(filePath).read()
  jsonParser     = json.loads(filPrgm) 
  uniqueItem = dict()  
  
  for lineup in jsonParser['Lineups'] :
    for lineupitem in lineup['LineupItems'] :
      if canPlay(lineupitem):
        if lineupitem['Title'] is not None: 
          if lineupitem['Title'] not in uniqueItem: 
            shows.append( [channel,lineupitem['Title'].encode('utf-8'), lineupitem['Title'].encode('utf-8'),lineupitem['ImageUrl'].encode('utf-8'),'shows'] )
            uniqueItem[lineupitem['Title']] = lineupitem['Title']
            
  return shows
  
def list_videos(channel,param):
  videos=[] 
  
  filePath=utils.downloadCatalog(urlCatalog,'TouTV.json',False,{}) 
  filPrgm=open(filePath).read()
  jsonParser     = json.loads(filPrgm) 
  
  for lineup in jsonParser['Lineups'] :
    for lineupitem in lineup['LineupItems'] :  
      if canPlay(lineupitem):
        if lineupitem['Title'] is not None: 
          if lineupitem['Title'].encode('utf-8') == param: 
            details=lineupitem['Details']
            plot           = details['Description'].encode('utf-8')
            duration   = details['Length']/60
            titre          = param
            if lineupitem['PromoDescription'] is not None:
              titre+='-' + lineupitem['PromoDescription'].encode('utf-8')  
            image      = details['ImageUrl'].encode('utf-8') 
            url= lineupitem['Url'].encode('utf-8')
            infoLabels = { "Title": titre,"Plot":plot,"Duration": duration}
            videos.append( [channel, url, titre, image,infoLabels,'play'] )
           
  return videos               

def getVideoURL(channel,video_URL):
    filPrgm=urllib2.urlopen('http://ici.tou.tv/presentation%s?v=2&d=ipad&includePartnerTeaser=false' % (video_URL)).read()
    jsonParser     = json.loads(filPrgm)
    IdMedia=jsonParser['IdMedia']
    IdMedia=122445
    filPrgm=urllib2.urlopen('http://api.radio-canada.ca/ValidationMedia/v1/Validation.html?appCode=toutv&idMedia=%s&deviceType=ipad&output=json'% (IdMedia)).read()
    print 'http://api.radio-canada.ca/ValidationMedia/v1/Validation.html?appCode=toutv&idMedia=%s&deviceType=ipad&output=json'% (IdMedia) 
    jsonParser     = json.loads(filPrgm)
    return jsonParser['url'] 
    
