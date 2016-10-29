import json
import re
from string import ascii_lowercase
from resources.lib import utils 

from multiprocessing.dummy import Pool as ThreadPool 
from operator import itemgetter
import time

channel = 'INA'
title=[channel]
img=[channel]
readyForUse=True


bypass_cache = True

root_url="http://m.ina.fr"
url_byletter=root_url + "/layout/set/ajax/listes/emissions?classObject=ina_emission&letter="
emissions_re = re.compile(r'<a href="(.*?)"><img .* alt="(.*?)" src="(.*?)".*</a>')
detail_re = re.compile(r'recherche.initialise\("(.*?)","(.*?)"\)')
emission_json_re = re.compile(r'<h2>.*?<a href="(.*?)">(.*?)</a>', re.DOTALL)
emission_url_re = re.compile(r'<video controls src=(.*?) ', re.DOTALL)

thread_count = len(ascii_lowercase)

def list_shows(channel,folder):
    begin = time.time()
    
<<<<<<< HEAD
    print "Thread pool size: {}".format(thread_count)
=======
    print "Thread pool size: " + thread_count
>>>>>>> branch 'master' of https://github.com/gdusart/plugin.video.freplay
    pool = ThreadPool(thread_count);    
        
    allshows = pool.map(loadEmissionsForLetter, ascii_lowercase)
    pool.close()
    pool.join()

    #flatten list
    allshows = [val for sublist in allshows for val in sublist]
       
    #list is populated by several threads in random order, order by name
    allshows = sorted(allshows, key=itemgetter(2))
    
    print "{}: took {}s to list all shows".format(channel, time.time() - begin)
    
    return allshows

def list_videos(channel, emissionPage):
    print "{}: list videos  for emission {}".format(channel, emissionPage)    
    
    shows = []
    
    ajaxcall = getSearchUrlForEmission(channel, emissionPage)
    
    tempfile = "{}_listvideos_{}.json".format(channel, emissionPage)
    
    filePath=utils.downloadCatalog(ajaxcall, tempfile, bypass_cache,{})    
    raw=open(filePath).read()
    jsoncontent=json.loads(raw)    
    htmlcontent = jsoncontent["content"].encode("UTF-8")
            
    match = emission_json_re.findall(str(htmlcontent), re.DOTALL)
    
    if match:
        for url, title in match:
            #TODO: unescape string (HTML entities)
            shows.append( [channel,url,title , '', {},'play'] )
    else:
        print "no regexp match found in emission data !"
            
    #TODO load image
    #TODO info labels
    
    return shows
    

def getVideoURL(channel,assetId): 
    print "INA get video URL: " + assetId
    
    url = root_url + assetId    
    
    tempfile = "{}_videourl_{}.html".format(channel, assetId)
    
    filePath=utils.downloadCatalog(url, tempfile, False,{})
    raw=open(filePath).read()    
    
    videolink = emission_url_re.search(raw).group(1)
    print "{}: Video link for asset {} : {}".format(channel, assetId, videolink)
    return videolink
    

def loadEmissionsForLetter(letter):
    start = time.time()
    
    shows=[]
        
    print "Loading emissions for letter  " + letter
    
    tempfile = "{}_emissionletter_{}.html".format(channel, letter)
    
    #Load json result (ajax call from mobile app
    filePath=utils.downloadCatalog(url_byletter + letter, tempfile, bypass_cache,{})    
    raw=open(filePath).read()
    
    #Treat as json, extract content field
    jsoncontent=json.loads(raw)    
    htmlcontent = jsoncontent["content"].encode("utf-8")
    
    #Apply regexp
    match = emissions_re.findall(htmlcontent)
    
    #Convert regexp groups to array of values
    if match:
        for url, title, img in match:
            shows.append( [channel, url, title , root_url + img,'shows'] )
    
    print "took {}s to load emissions for letter {}".format(time.time() - start, letter)
    
    return shows  
 
def getSearchUrlForEmission(channel, emissionPage):
    emissionPage = root_url + emissionPage
    
    tempfile = "{}_details_{}.html ".format(channel, emissionPage)
    
    filePath=utils.downloadCatalog(emissionPage, tempfile, bypass_cache,{})    
    raw=open(filePath).read()
    
    result = detail_re.search(raw)
    return root_url + result.group(1) + '?' + result.group(2)
     
      