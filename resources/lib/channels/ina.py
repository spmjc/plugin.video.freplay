#-*- coding: utf-8 -*-
import re, json, time, threading
from string import ascii_lowercase
from resources.lib import utils 
from HTMLParser import HTMLParser
from operator import itemgetter

title       = ['INA']
img         = ['ina']
readyForUse = True

bypass_cache = False
lsLowercase  = list(ascii_lowercase)

detail_re        = re.compile(r'recherche.initialise\("(.*?)","(.*?)"\)')
emissions_re     = re.compile(r'<a href="(.*?)"><img .* alt="(.*?)" src="(.*?)".*</a>')
emission_json_re = re.compile(r'<img .*? src="(.*?)".*?<h2>.*?<a href="(.*?)">(.*?)</a>', re.DOTALL)
emission_url_re  = re.compile(r'<video controls src=(.*?) ', re.DOTALL)
root_url         = "http://m.ina.fr"
url_byletter     = root_url + "/layout/set/ajax/listes/emissions?classObject=ina_emission&letter="

def list_shows(channel,folder):
    allshows = []
    begin = time.time()        
    
    #launch 1 thread for each letter
    threads = [];
    for letter in lsLowercase:
        thread = ShowLoadingThread(letter, allshows)
        threads.append(thread)
        thread.start()
        
    #wait for all threads to complete
    for thread in threads:
        thread.join()    
    
    #flatten list 
    allshows = [val for sublist in allshows for val in sublist]
    #list is populated by several threads in random order, order by name
    allshows = sorted(allshows, key=itemgetter(2))
    print("%s: took %ss to list all shows"%(channel, time.time()-begin))
    
    return allshows

def list_videos(channel, emission_page):
    print("%s: list videos  for emission %s"%(channel, emission_page))    
    shows        = []    
    ajaxcall     = get_search_url_for_emission(channel, emission_page)    
    tempfile     = "%s_listvideos_%s.json"%(channel, emission_page)    
    file_path    = utils.downloadCatalog(ajaxcall, tempfile, bypass_cache,{})    
    raw          = open(file_path).read()
    jsoncontent  = json.loads(raw)    
    htmlcontent  = jsoncontent["content"].encode("UTF-8")
    match        = emission_json_re.findall(str(htmlcontent), re.DOTALL)
    parser       = HTMLParser();
    if match:
        for pic, url, name in match:
            shows.append([channel,url,parser.unescape(name.decode("UTF-8")).encode("UTF-8") , pic, {},'play'] )
    else:
        print("no regexp match found in emission data !")            
    #TODO load image
    #TODO info labels    
    return shows
    
def getVideoURL(channel,asset_id): 
    print("INA get video URL: " + asset_id)    
    url       = root_url + asset_id    
    tempfile  = "%s_videourl_%s.html"%(channel, asset_id)    
    file_path = utils.downloadCatalog(url, tempfile, False,{})
    raw       = open(file_path).read()    
    videolink = emission_url_re.search(raw).group(1)
    print("%s: Video link for asset %s : %s"%(channel, asset_id, videolink))
    return videolink
    
def load_emissions_for_letter(letter):
    print("Loading emissions for letter  " + letter)    
    start     = time.time()    
    shows     = []        
    tempfile  = "%s_emissionletter_%s.html"%(title[0], letter)    
    #Load json result (ajax call from mobile app
    file_path = utils.downloadCatalog(url_byletter+letter, tempfile, bypass_cache,{})    
    raw       = open(file_path).read()    
    #Treat as json, extract content field
    jsoncontent = json.loads(raw)    
    htmlcontent = jsoncontent["content"].encode("utf-8")    
    #Apply regexp
    match = emissions_re.findall(htmlcontent)    
    #Convert regexp groups to array of values
    if match:
        for url, name, pic in match:
            shows.append( [title[0], url, name , root_url + pic,'shows'] )    
    print("took %ss to load emissions for letter %s"%(time.time()-start, letter))    
    return shows  
 
def get_search_url_for_emission(channel, emission_page):
    emission_page = root_url + emission_page    
    tempfile      = "%s_details_%s.html "%(channel, emission_page)    
    file_path     = utils.downloadCatalog(emission_page, tempfile, bypass_cache,{})    
    raw           = open(file_path).read()    
    result        = detail_re.search(raw)
    return root_url + result.group(1) + '?' + result.group(2)
    
class ShowLoadingThread(threading.Thread):
    
    def __init__(self, letter, dest):
        threading.Thread.__init__(self)
        self.letter = letter
        self.shows  = dest        
        
    def run(self):
        results = load_emissions_for_letter(self.letter)
        self.shows.append(results)
     
      