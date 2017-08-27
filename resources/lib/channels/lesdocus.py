#-*- coding: utf-8 -*-
from resources.lib import utils
from bs4 import BeautifulSoup as bs
import re


title       = ['Les docus']
img         = ['lesdocus']
readyForUse = True
bypass_cache = True

def load_soup(url, cache_key):
    file_path = utils.downloadCatalog(url, cache_key, bypass_cache, {})
    html = open(file_path).read()
    return bs(html, 'html.parser')

#**list_shows(channel,folder)**: Utilise pour recuperer la liste des menus.
# Channel est toujours renseigne.Folder est un parametre remseigbne a none la 1ere fois et contient votre parametre les fois suivantes.
# Retourne un tableau **Ligne=[ channel, parameter pour prochain passage dans fonction, Titre pour menu, image pour menu, action effectuee quand clic sur menu]**
#_Dernier parametre : 'folder' : retour dans meme fonctions, 'shows' prochain passage est dans "list_videos"
def list_shows(channel,folder):
    return []


#**list_videos(channel,show_URL)**: Fonctionne de maniere similaire.
# Retourne un tableau **Ligne=[ channel, param pour passage dans fonction getvideoURL, Titre pour menu, image pour menu, infoLabels, 'play']**
def list_videos(channel,show_name):
    return []


#getVideoURL(channel,video_URL)**: Retourne l'URL qui devra etre lu par KODI
def getVideoURL(channel,video_url):
    return ''

