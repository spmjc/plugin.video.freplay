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
detail_re = re.compile(r'recherche.initialise\("(.*?)","(.*?)"\)')
emission_json_re = re.compile(r'<h2>.*?<a href="(.*?)">(.*?)</a>', re.DOTALL)

def list_shows(channel,folder):
    allshows = []
    for letter in ascii_lowercase:
        allshows.extend(loadEmissionsForLetter(letter,title[0]))
        
    return allshows

def list_videos(channel, emissionPage):
    print "list videos INA"    
    
    shows = []
    
    ajaxcall = getSearchUrlForEmission(channel, emissionPage)
    filePath=utils.downloadCatalog(ajaxcall, channel+"_"+emissionPage+ ".json", False,{})    
    raw=open(filePath).read()
    jsoncontent=json.loads(raw)    
    htmlcontent = jsoncontent["content"].encode("UTF-8")
            
    match = emission_json_re.findall(str(htmlcontent), re.DOTALL)
    
    if match:
        print "match"
        for url, title in match:
            print "title: " + title
            shows.append( [channel,url, title , '', {},'play'] )
    else:
        print "no match !"
    
    #TODO load image
    #TODO info labels
    
    return shows
    

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
 
def getSearchUrlForEmission(channel, emissionPage):
    emissionPage = root_url + emissionPage
    filePath=utils.downloadCatalog(emissionPage, channel + '_details_' + emissionPage + '.html', False,{})    
    raw=open(filePath).read()
    
    result = detail_re.search(raw)
    return root_url + result.group(1) + '?' + result.group(2)
     
      