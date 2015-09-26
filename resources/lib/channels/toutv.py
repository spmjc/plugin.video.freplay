#-*- coding: utf-8 -*-    
from resources.lib import utils
import json                   
import urllib,urllib2

title=['Tou.tv']
img=['toutv']
readyForUse=True          

def list_shows(channel,param):  
  shows=[]
  
  filePath=utils.downloadCatalog('http://www.tou.tv/presentation/section/a-z?AkamaiDevice=phone&smallWidth=320&mediumWidth=640&largeWidth=640&isPhone=True','TouTV.json',False,{}) 
  filPrgm=open(filePath).read()
  jsonParser     = json.loads(filPrgm)
  
  if param=='none':
    for menu in jsonParser['Lineups'] :
      shows.append( [channel,menu['Name'], menu['Title'].encode('utf-8'),'','folder'] )
  else:
    for menu in jsonParser['Lineups'] :
      if param==menu['Name']:
        for item in menu['LineupItems']:
          if item['BookmarkKey']:
            shows.append( [channel,item['Url'], item['Title'].encode('utf-8'),item['ImageUrl'],'shows'] )  

  return shows
  
def list_videos(channel,show_URL):
    videos=[] 
    
    filPrgm=urllib2.urlopen('http://www.tou.tv/presentation%s?AkamaiDevice=phone&excludeLineups=False&playerWidth=0' % (show_URL)).read()
    jsonParser     = json.loads(filPrgm)
    
    url=''
    title=jsonParser['Title'].encode('utf-8')
    icon=''
    
    if jsonParser['SeasonLineups']:
      for season in jsonParser['SeasonLineups'] :
        for item in season['LineupItems'] :
          url=item['Url']
          title+='-'.encode('utf-8') + item['Title'].encode('utf-8')
          icon=item['ImageUrl']
          desc=item['Details']['Description'].encode('utf-8')
          date=item['Details']['AirDate']
          duration=item['Details']['Length']
          
          infoLabels={ "Title": title,"Plot":desc,"Aired":date,"Duration": duration, "Year":date[:4]}
          videos.append( [channel, url, title, icon,infoLabels,'play'] )
    else:
      url=show_URL
      title=jsonParser['Title'].encode('utf-8')
      icon=jsonParser['ImageUrl']
      desc=jsonParser['Details']['Description'].encode('utf-8')
      date=jsonParser['Details']['AirDate']
      duration=jsonParser['Details']['Length']
      
      infoLabels={ "Title": title,"Plot":desc,"Aired":date,"Duration": duration, "Year":date[:4]}
      videos.append( [channel, url, title, icon,infoLabels,'play'] )
             
    return videos               

def getVideoURL(channel,video_URL):
    filPrgm=urllib2.urlopen('http://www.tou.tv/presentation%s?AkamaiDevice=phone&excludeLineups=true&playerWidth=0' % (video_URL)).read()
    jsonParser     = json.loads(filPrgm)
    filPrgm=urllib2.urlopen('http://api.radio-canada.ca/validationMedia/v1/Validation.html?deviceType=ipad&appCode=thePlatform&connectionType=broadband&output=json&idMedia='+ jsonParser['IdMedia']).read()
    jsonParser     = json.loads(filPrgm)
    return jsonParser['url'] 
    
