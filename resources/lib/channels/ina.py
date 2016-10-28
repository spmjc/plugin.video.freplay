import json
import re
from string import ascii_lowercase
from resources.lib import utils 

title=['INA']
img=['INA']
readyForUse=True

root_url="http://m.ina.fr"
url_byletter=root_url + "/layout/set/ajax/listes/emissions?classObject=ina_emission&letter="
emissions_re = re.compile(r'<a href="(.*?)"><img .* alt="(.*?)" src="(.*?)".*</a>')


def list_shows(channel,folder):
    allshows = []
    for letter in ascii_lowercase:
        allshows.extend(loadEmissionsForLetter(letter,title[0]))
        
    return allshows

def list_videos(channel,folderIdSet):
    print "list videos INA"    

def getVideoURL(channel,assetId): 
    print "get video URL INA"    

def loadEmissionsForLetter(letter, channel):
    shows=[]
    
    #Load json result (ajax call from mobile app
    filePath=utils.downloadCatalog(url_byletter + letter, letter, False,{})    
    raw=open(filePath).read()
    
    #Treat as json, extract content field
    jsoncontent=json.loads(raw)    
    htmlcontent = jsoncontent["content"].encode("utf-8")
    
    #Apply regexp
    match = emissions_re.findall(htmlcontent)
    
    #Convert regexp groups to array of values
    if match:
        for url, title, img in match:
            shows.append( [channel,url, title , root_url + img,'shows'] )
    
    return shows      
 
      