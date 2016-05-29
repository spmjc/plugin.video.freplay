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

url_root    = 'http://www.nrj-play.fr'
url_catalog = '%s/cherie25/replay'%url_root

def list_shows(channel,folder):
    shows    = []
    filePath = utils.downloadCatalog(url_catalog,'cherie25.html',False,{})
    html     = open(filePath).read().decode("utf-8")
    line_s   = common.parseDOM(html,"li", attrs={"class": "subNav-menu-item"}) # Menu avec les différentes catégories (Magzines, Séries, Films ...)

    for line in line_s:
        categorie_name         = common.parseDOM(line,"a")[0].encode("utf-8")
        categorie_link         = common.parseDOM(line,"a", ret="href")[0].encode("utf-8")
        if folder=='none' :
            shows.append([channel, categorie_link, categorie_name,'','folder']) 

        elif folder==categorie_link : # On est rentré dans une catégorie
            url_categorie = url_root+folder
            filePath = utils.downloadCatalog(url_categorie,categorie_link+'.html',False,{}) # On télécharge la page de cette catéogrie
            html     = open(filePath).read().decode("utf-8")
            linkProgram_s = common.parseDOM(html,"div",attrs={"class":"linkProgram large"}) 
            linkProgram_s = linkProgram_s + common.parseDOM(html,"div",attrs={"class":"linkProgram"}) # On a l'ensemble des programmes proposés dans cette catégorie
            for linkProgram in linkProgram_s:
                linkProgram_infos  = common.parseDOM(linkProgram_s,"div",attrs={"class":"linkProgram-infos"})
                linkProgram_details  = common.parseDOM(linkProgram,"div",attrs={"class":"linkProgram-details"})
                
                image_a  = common.parseDOM(linkProgram_infos[linkProgram_s.index(linkProgram)],"a")[0]
                image_url  = common.parseDOM(image_a,"img",ret="src")[0].encode("utf-8")
                
                titre_h2    = common.parseDOM(linkProgram_details,"h2")[0].encode("utf-8")
                titre_h2 = common.replaceHTMLCodes(titre_h2)
                titre_h2 = titre_h2.title()

                url_program = common.parseDOM(linkProgram_details, "a", ret="href")[0].encode("utf-8")

                shows.append([channel,url_program+'|'+titre_h2+'|'+image_url,titre_h2,image_url,'shows'])                   
    return shows

def list_videos(channel,params):
    videos      = []                  
    program_url = params.split('|')[0]
    titre_program      = params.split('|')[1]
    image_url_show = params.split('|')[2]

    program_url_page = url_root+program_url
    filePath = utils.downloadCatalog(program_url_page,'cherie25_'+titre_program+'.html',False,{})
    html     = open(filePath).read().decode("utf-8")

    section_replay = common.parseDOM(html,"section",attrs={"class":"section-replay"}) # Carousel des replays
    item_s = common.parseDOM(section_replay, "div", attrs={"class":"item"}) # Un item correspond à une video

    if len(section_replay) > 0:
        for item in item_s :
            thumbnail_infos = common.parseDOM(item,"div", attrs={"class":"thumbnail-infos"})
            caption = common.parseDOM(item,"div", attrs={"class":"caption"})

            url_video = common.parseDOM(thumbnail_infos, "a", ret="href")[0].encode("utf-8")
            image = common.parseDOM(thumbnail_infos, "img", ret="src")[0].encode("utf-8")

            try:
                date = common.parseDOM(caption, "time")[0].encode("utf-8")
            except Exception:
                date = ""
            titre = common.parseDOM(caption, "a")[0].encode("utf-8")
            titre = common.replaceHTMLCodes(titre)
            titre = titre.title()
            videos.append([channel,url_video,titre,image,{'Title':titre+" - "+date},'play'])
    else:
        player_video_title_header = common.parseDOM(html,"div",attrs={"class":"playerVideo-title-header"})

        date = common.parseDOM(player_video_title_header, "small")[0].encode("utf-8")
        date = date.split()
        date_2 = ""
        for x in date:
            date_2 = date_2+" "+x
        videos.append([channel,program_url,titre_program,image_url_show,{'Title':titre_program+" - "+date_2},'play'])
      
    return videos



def getVideoURL(channel,urlPage):
    url_page_video = url_root+urlPage
    filePath = utils.downloadCatalog(url_page_video,urlPage+'.html',False,{}) 
    html     = open(filePath).read().decode("utf-8")
    player_video_wrapper = common.parseDOM(html,"div",attrs={"class":"playerVideo-wrapper"})
    url = common.parseDOM(player_video_wrapper, "meta", attrs={"itemprop":"contentUrl"}, ret="content")[0].encode("utf-8")
    return url