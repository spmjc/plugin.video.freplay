#-*- coding: utf-8 -*-
from resources.lib import utils
import re 
import CommonFunctions
common = CommonFunctions   
import base64   
import urllib2

title       = ['Chérie 25']
img         = ['cherie25']
readyForUse = True

url_root    = 'http://www.cherie25.fr'
url_catalog = '%s/replay-4272/collectionvideo/'%url_root
url_integra = 'http://prod-kernnrj12v5.integra.fr/videoinfo'

def list_shows(channel,folder):
    shows    = []
    filePath = utils.downloadCatalog(url_catalog,'cherie25.html',False,{})
    html     = open(filePath).read().decode("utf-8")
    line_s   = common.parseDOM(html,"div",attrs={"class":u"line replay magazines"})
    for line in line_s :
        title          = common.parseDOM(line,"div",attrs={"class":"title"})[0]
        categorie_name = common.parseDOM(title,"span")[0].encode("utf-8")
        if folder=='none' :
            shows.append([channel,categorie_name,categorie_name,'','folder'])
        elif folder==categorie_name :
            li_s = common.parseDOM(line,"li",attrs={"id":"liste_[0-9]"})
            for li in li_s :
                replay_hover_s = common.parseDOM(li,"div",attrs={"class":u"replay_hover"})
                if replay_hover_s :
                    image_div  = common.parseDOM(li,"div",attrs={"class":"image"})[0]
                    image_a_u  = common.parseDOM(image_div,"a")[0]
                    image_url  = common.parseDOM(image_a_u,"img",ret="src")[0]
                    titre_p    = common.parseDOM(li,"p",attrs={"class":"titre"})[0]
                    titre_u    = common.parseDOM(titre_p,"a")[0]
                    titre      = titre_u.encode("utf-8")
                    shows.append([channel,titre+'|'+image_url,titre,image_url,'shows'])
                else :
                    image_div   = common.parseDOM(li,"div",attrs={"class":"image"})[0]
                    image_a_u   = common.parseDOM(image_div,"a")[0]
                    image_url   = common.parseDOM(image_a_u,"img",ret="src")[0]
                    titre_p     = common.parseDOM(li,"p",attrs={"class":"titre"})[0]
                    titre_u     = common.parseDOM(titre_p,"a")[0]
                    titre       = titre_u.encode("utf-8")
                    video_url_u = url_root+common.parseDOM(titre_p,"a",ret="href")[0]
                    video_url   = video_url_u.encode("utf-8")
                    shows.append([channel,video_url+'|'+titre,titre,image_url,'shows'])                     
    return shows

def list_videos(channel,params):    
    videos      = []                  
    show        = params.split('|')[0]
    fanart      = params.split('|')[1]
    if show.startswith(url_root):
        video_url = show
        titre     = fanart
        videos.append([channel,video_url,titre,'',{'Title':titre},'play'])
    else :
        filePath    = utils.downloadCatalog(url_catalog,'cherie25.html',False,{})
        html        = open(filePath).read().decode("utf-8")
        line_replay = common.parseDOM(html,"div",attrs={"class":u"line replay magazines"})
        for line in line_replay :
            li_s = common.parseDOM(line,"li",attrs={"id":"liste_[0-9]"})
            for li in li_s :
                replay_hover_s = common.parseDOM(li,"div",attrs={"class":u"replay_hover"})
                if replay_hover_s :
                    titre_p = common.parseDOM(li,"p",attrs={"class":"titre"})[0]
                    titre   = common.parseDOM(titre_p,"a")[0].encode("utf-8")
                    if titre==show :
                        videos.extend(get_shows(show,li,fanart,channel))              
    return videos

def getVideoURL(channel,urlPage):
  html=urllib2.urlopen(urlPage).read().replace('\xe9', 'e').replace('\xe0', 'a')
  match = re.compile(r'data-url="(.*?)"',re.DOTALL).findall(html)
  url=base64.b64decode(match[0] + '=')
  return url

def get_shows(emission,liste,fanart,channel):
    videos = []
    replay_hover_s = common.parseDOM(liste,"div",attrs={"class":u"replay_hover"})
    if replay_hover_s :
        replay_hover = replay_hover_s[0]
        li_s         = common.parseDOM(replay_hover,"li",attrs={"id":"list_item_[0-9]"})
        for li in li_s :
            infoLabels = {}
            image_div  = common.parseDOM(li,"div",attrs={"class":"image"})[0]
            image_a_u  = common.parseDOM(image_div,"a")[0]
            image_url  = common.parseDOM(image_a_u,"img",ret="src")[0].encode("utf-8")
            titre_p    = common.parseDOM(li,"p",attrs={"class":"titre"})[0]
            titre      = common.parseDOM(titre_p,"a")[0].encode("utf-8")
            video_url  = url_root+common.parseDOM(titre_p,"a",ret="href")[0].encode("utf-8")
            infoLabels['Thumb'] = image_url
            infoLabels['Plot']  = get_video_desc(video_url)
            infoLabels['Title'] = titre
            videos.append([channel,video_url,titre,image_url,infoLabels,'play'])
    return videos
    
def get_video_desc(url):
    soup                       = utils.get_webcontent(url)
    html                       = soup.decode("utf-8")
    encart_titre_mea_mea_video = common.parseDOM(html,"div",attrs={"class":u"encart_titre_mea mea_video"})[0]
    text_infos                 = common.parseDOM(encart_titre_mea_mea_video,"div",attrs={"class":u"text-infos"})[0]
    text                       = common.parseDOM(text_infos,"div",attrs={"class":"text"})[0]
    video_desc                 = common.parseDOM(text,"p")[0]
    return video_desc.encode("utf-8")