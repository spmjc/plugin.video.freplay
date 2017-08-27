#-*- coding: utf-8 -*-
from resources.lib import utils
from bs4 import BeautifulSoup as bs
import re


title       = ['Têtes à claques']
img         = ['tac']
readyForUse = True
bypass_cache = False

root_url         = "https://www.tetesaclaques.tv"
categories_url     = root_url
categories_links_selector = "#menu-videos > ul > li > a"
clip_selector = 'div[class^=wrapCapsule]'
video_id_re  = re.compile(r'AtedraVideo.video_id = "(.*)";')
personnages_folder = 'personnages'
personnages_url = root_url + '/' + personnages_folder
personnages_link_selector = 'div.wrapThumb > a'

def load_soup(url, cache_key):
    file_path = utils.downloadCatalog(url, cache_key, bypass_cache, {})
    html = open(file_path).read()
    return bs(html, 'html.parser')


#**list_shows(channel,folder)**: Utilise pour recuperer la liste des menus.
# Channel est toujours renseigne.Folder est un parametre remseigbne a none la 1ere fois et contient votre parametre les fois suivantes.
# Retourne un tableau **Ligne=[ channel, parameter pour prochain passage dans fonction, Titre pour menu, image pour menu, action effectuee quand clic sur menu]**
#_Dernier parametre : 'folder' : retour dans meme fonctions, 'shows' prochain passage est dans "list_videos"
def list_shows(channel,folder):
    print("List show for folder " + folder)
    if (folder == personnages_folder):
        return load_personnages(channel)
    else:
        return load_categories(channel)


def load_categories(channel):
    categories = []

    print("Loading categories")
    soup = load_soup(categories_url, 'categories.html');

    links = soup.select(categories_links_selector)
    for link in links:
        folder_path = link.get('href').encode('utf-8')
        type = 'folder' if folder_path == personnages_folder else 'shows'
        categories.append([channel, folder_path, link.getText().encode("utf-8"), '', type])

    print("Categories: %s"%(categories))
    return categories


def load_personnages(channel):
    personnages = []

    print("Loading personnages")
    soup = load_soup(personnages_url, 'personnages.html')

    links = soup.select(personnages_link_selector)
    for link in links:
        path = root_url + link.get('href')
        image = root_url + link.select_one('img').attrs['src']
        title = link.attrs['title'].encode('utf-8')
        personnages.append([channel, path, title, image, 'shows'])

    return personnages



#**list_videos(channel,show_URL)**: Fonctionne de maniere similaire.
# Retourne un tableau **Ligne=[ channel, param pour passage dans fonction getvideoURL, Titre pour menu, image pour menu, infoLabels, 'play']**
def list_videos(channel,show_name):
    print('loading videos for ' + show_name)
    videos = []

    #current page is page 1
    pagenumber = 1
    folder_url = root_url + '/' + show_name
    tempfile = '%s_%d'%(show_name, pagenumber)

    #parse first page
    print('Loading first page for %s from %s: '%(show_name, folder_url))
    soup = load_soup(folder_url, tempfile)
    parse_clips_page(soup, videos, channel)

    #get last page link
    pagelinks = soup.select('a.pageNum');
    if (len(pagelinks) == 0):
        #no page links (single result page), return first page results
        return videos

    #several pages to parse
    #determine last page number and generate base pagination link
    lastpage_link = pagelinks[-1]
    lastpage_number = int(lastpage_link.getText().encode('utf-8'))
    lastpage_href = root_url + lastpage_link.attrs['href'].encode('utf-8')

    #remove trailing page number from string
    base_page_href = re.sub( r"\/\d*$", '/', lastpage_href)

    #parse pages 2 to last by adding page number to pagination links
    for pagenumber in range(2, lastpage_number + 1):
        page_url = '%s%d'%(base_page_href, pagenumber)
        tempfile = '%s_%s'%(show_name, pagenumber)

        print('Loading page %s for %s on %s...' % (pagenumber, show_name, page_url))
        soup = load_soup(page_url, tempfile)
        parse_clips_page(soup, videos, channel)

    print("Found %d videos for %s"%(len(videos), show_name))
    return videos


def parse_clips_page(soup, results, channel):
    for item in soup.select(clip_selector):
        link = root_url + item.select_one('a').attrs['href']
        image = item.select_one('img')
        imagelink = root_url + '/' + image.attrs['src']
        title = image.attrs['alt'].encode('utf-8')
        results.append([channel, link, title, imagelink, '', 'play'])


#getVideoURL(channel,video_URL)**: Retourne l'URL qui devra etre lu par KODI
def getVideoURL(channel,video_url):
    file_path = utils.downloadCatalog(video_url, video_url, bypass_cache, {})
    html = open(file_path).read()
    videoId  = video_id_re.search(html).group(1)
    result = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid='+videoId;
    print("RESULT : " + result)
    return result;
