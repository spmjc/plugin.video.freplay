import urllib,urllib2
import json
import time
from hashlib import sha1
from base64 import b64encode
from ordereddict import OrderedDict

nbByPage=25
__partner_key__ = "100043982026"
__secret_key__ = "29d185d98c984a359e6e6f26a0474269"
__base_url__ = "http://api.allocine.fr/rest/v3/"

def list_shows(channel,folder):
    shows=[]
    
    if folder=='none':
        shows.append( [channel,'toptrailer$$1', 'BA A ne pas manquer','','shows'] )
        shows.append( [channel,'trailer:nowshowing$$1', 'BA Au Cinema','','shows'] )
        shows.append( [channel,'emi', 'Emissions','','folder'] )
        shows.append( [channel,'itvw', 'Interviews','','shows'] )
    else:
        method = 'termlist'
        query_params = OrderedDict([
                ('partner', __partner_key__),
                ('filter', 'acshow'),
                ('format', 'json')
        ])
        print get_signed_url(method, query_params)
        jsonFeed     = json.loads(urllib2.urlopen(get_signed_url(method, query_params)).read())
        for show in jsonFeed['feed']['term'] :
            shows.append( [channel,'acshow:' + show['nameShort'] + '$$1', show['$'],'','shows'] )
    return shows

def list_videos(channel,show_title):
    videos=[] 
    type_filter=show_title.split('$$')[0]
    page=int(show_title.split('$$')[1])
    
    method = 'videolist'
    query_params = OrderedDict([
            ('partner', __partner_key__),
            ('count',nbByPage),
            ('mediafmt','mp4'),
            ('page',page),
            ('format', 'json'),
            ('filter', type_filter)
    ])
    print get_signed_url(method, query_params)
    jsonFeed     = json.loads(urllib2.urlopen(get_signed_url(method, query_params)).read())
    nbResults=int(jsonFeed['feed']['totalResults'])
    nbPage=round(nbResults/nbByPage)
    if page!=1:
        infoLabels={}
        videos.append( [channel, type_filter + '$$' + str(page-1), "Page " + str(page-1) + '/' + str(nbPage), '',infoLabels,'shows'])
    for show in jsonFeed['feed']['media'] :
        sizeMax=0
        for rend in show['rendition']:
            if sizeMax<rend['size']:
                url=rend['href']
                sizeMax=rend['size']
        title=show['title']
        icon=show['poster']['href']
        desc='Vues :' + str(show['statistics']['viewCount'])
        date=show['modificationDate'][:10]
        try:
            duration=show['runtime']
        except:
            duration=0
        infoLabels={ "Title": title,"Plot":desc,"Aired":date,"Duration": duration, "Year":date[:4]}
        videos.append( [channel, url, title, icon,infoLabels,'play'])
    if page<nbPage:
        infoLabels={}
        videos.append( [channel, type_filter + '$$' + str(page+1), "Page " + str(page+1) + '/' + str(nbPage), '',infoLabels,'shows'])
    return videos

def getVideoURL(channel,video_URL):
    return video_URL

def get_signed_url(method, query_params):
    # Generate signed url
    # Translated from php code available at https://github.com/gromez/allocine-api
    
    sed = str(time.strftime ('%Y%m%d'))
    
    # urlencode replaces "," by "%2C" but the api does not accept urls like that.
    # So just re-replace the "%2C" by "," after urlencode... damn this api is annoying...
    query_string = urllib.urlencode(query_params).replace("%2C", ",").replace('%3A',':') + "&sed=" + sed

    # Again, put "," a safe character because the api does not accept "%2C"
    sig = urllib.quote(b64encode(sha1(__secret_key__ + query_string).digest()), ',')
    signed_url = __base_url__ + method + '?' + query_string + "&sig=" + sig
    return signed_url
