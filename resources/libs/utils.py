import globalvar
import cplus
import pluzz
import arte
import favourites
import gulli
import tf1
import msix
import acine
import tara
import d8
import nrj12

import os
import sys
import urllib,urllib2
import json

def init():
    # append pydev remote debugger
    if globalvar.REMOTE_DBG:
        # Make pydev debugger works for auto reload.
        # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
        try:
            import pysrc.pydevd as pydevd
        # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
            pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
        except ImportError:
            sys.stderr.write("Error: " +
                "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")

    globalvar.channels = {'favourites': [ 'Favourites', favourites,False],
           'tf1': ['TF1', tf1,False],
           'tmc': ['TMC', tf1,False],
           'nt1': ['NT1', tf1,False],
           'france1': ['France 1', pluzz,False],
           'france2': ['France 2', pluzz,False],
           'france3': ['France 3', pluzz,False],
           'france4': ['France 4', pluzz,False],
           'france5': ['France 5', pluzz,False],
           'franceo': ['France O', pluzz,False],
           'cplus': ['Canal +', cplus,False],
           'arte': ['Arte', arte,False],
           'gulli': ['Gulli', gulli,False],
           'msix': ['M6', msix,False],
           'acine': ['AlloCine', acine,False],
           'D8': ['D8', d8,False],
           'D17': ['D17', d8,False],
           'nrj12': ['NRJ12', nrj12 ,False]
           }
    globalvar.ordered_channels=[
           'favourites',
           'tf1',
           'france2',
           'france3',
           'cplus',
           'arte',
           'D8',
           'nrj12',
           'tmc',
           'D17',
           'france1',
           'france4',
           'france5',
           'franceo',
           'nt1'
           ]
    
            
def firstRun():
    if not os.path.exists(globalvar.CACHE_DIR) :
        os.makedirs(globalvar.CACHE_DIR, mode=0777)
    #Download Pluzz Catalog
    if os.path.exists(globalvar.CATALOG_PLUZZ):
        os.remove(globalvar.CATALOG_PLUZZ)
    urllib.urlretrieve('http://webservices.francetelevisions.fr/catchup/flux/flux_main.zip',globalvar.CATALOG_PLUZZ)
    #Download Canal
    if os.path.exists(globalvar.CATALOG_CANAL):
        os.remove(globalvar.CATALOG_CANAL)
    urllib.urlretrieve('http://service.mycanal.fr/authenticate.json/Android_Tab/1.1?highResolution=1',globalvar.CATALOG_CANAL)
    #Download ARTE
    if os.path.exists(globalvar.CATALOG_ARTE):
        os.remove(globalvar.CATALOG_ARTE)
    urllib.urlretrieve('http://www.arte.tv/papi/tvguide-flow/sitemap/feeds/videos/F.xml',globalvar.CATALOG_ARTE)
        

    #Download M6 Catalog
    #if os.path.exists(globalvar.CATALOG_M6):
    #    os.remove(globalvar.CATALOG_M6)
    #urllib.urlretrieve('http://static.m6replay.fr/catalog/m6group_ipad/m6replay/catalogue.xml',globalvar.CATALOG_M6)
    
#def download_video(name, url):
    #downloader = simpledownloader.SimpleDownloader()
    
    #params = { "url": url, "download_path": globalvar.CACHE_DIR }
    #downloader.download('test', params)