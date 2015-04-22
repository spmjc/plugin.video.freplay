import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon

import os

ADDON_NAME='plugin.video.freplay'
ADDON     = xbmcaddon.Addon(ADDON_NAME)
SETTINGS  = ADDON
LANGUAGE  = ADDON.getLocalizedString
ADDON_DIR = ADDON.getAddonInfo( "path" )
RESOURCES = os.path.join( ADDON_DIR, "resources" )   
CHANNELS_DIR= os.path.join( RESOURCES, "libs","channels" ) 
MEDIA     = os.path.join( RESOURCES, "media")
ADDON_DATA= xbmc.translatePath( "special://profile/addon_data/%s/" % ADDON_NAME )
CACHE_DIR = os.path.join( ADDON_DATA, "cache")
FAVOURITES_FILE = os.path.join( ADDON_DATA, "favourites.json")
CATALOG_M6=os.path.join(CACHE_DIR,'m6.xml')
CATALOG_PLUZZ        = os.path.join(CACHE_DIR,'PluzzMobileCatalog.zip')
CATALOG_CANAL        = os.path.join(CACHE_DIR,'CANAL.json')
CATALOG_ARTE        = os.path.join(CACHE_DIR,'ARTE.xml')

LOGLEVEL=1 #From to 3
DEVMODE=True

VIEWID='503'

LANG='fr'
QLTY='hd'

dirCheckList        = (CACHE_DIR,)
channels=dict()
ordered_channels=[]

