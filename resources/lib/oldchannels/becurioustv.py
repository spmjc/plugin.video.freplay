#-*- coding: utf-8 -*-
from resources.lib import utils
import re 
import CommonFunctions
common = CommonFunctions   

title       = ['BeCurious TV']
img         = ['becurioustv']
readyForUse = False

url_root = 'http://becurioustv.com'
url_shows = '%s/fr/shows'%url_root
url_player = "http://cdnapi.kaltura.com"


def list_shows(channel,folder):
    shows = []
    filePath = utils.downloadCatalog(url_shows,'becurioustv.html',False,{}) # Page principale du replay
    html = open(filePath).read().decode("utf-8")
    shows_container = common.parseDOM(html,"div", attrs={"class": "shows-container background-pink"})
    
    if folder == 'none':
        for show in shows_container:
            title = common.parseDOM(show,"h1", attrs={"class": "color-magenta"})[0].encode('utf-8')
            show_icon = common.parseDOM(show,"div", attrs={"class": "shows__icon"})
            url_show = common.parseDOM(show_icon,"img", ret="src")[0].encode('utf-8')
            url_show = url_root+url_show
            shows.append([channel,title,title,url_show,'folder'])
    else:
        for show in shows_container:
            if folder in show.encode('utf-8'):
                item_list = common.parseDOM(show,"div", attrs={"class": "item"})
                for item in item_list: 
                    title = common.parseDOM(item,"h2")[0].encode('utf-8')
                    #title = common.replaceHTMLCodes(title)

                    episodes_length = common.parseDOM(item,"span")[0].encode('utf-8')

                    url_show = common.parseDOM(item,"a", ret="href")[0].encode('utf-8')
                    url_show = url_root+url_show

                    url_icon = common.parseDOM(item,"img", ret="src")[0].encode('utf-8')
                    url_icon = url_root+url_icon

                    shows.append([channel,url_show+'|'+title,title+" - "+episodes_length,url_icon,'shows'])
    return shows
            
def list_videos(channel,params):
    videos      = []                  
    program_url = params.split('|')[0]
    titre_program      = params.split('|')[1]

    filePath = utils.downloadCatalog(program_url,'becurioustv_'+titre_program+'.html',False,{})
    html     = open(filePath).read().decode("utf-8")

    season_grid = common.parseDOM(html,"div",attrs={"class":"seasons-grid tab-season"})

    for season in season_grid:
        list_li = common.parseDOM(season,"li")
        for li in list_li:
            title_h5 = common.parseDOM(li,"h5")
            title = common.parseDOM(title_h5,"a")[0].encode('utf-8')
            #title = common.replaceHTMLCodes(title)

            url_show = common.parseDOM(title_h5,"a", ret="href")[0].encode('utf-8')
            url_show = url_root+url_show

            url_icon = common.parseDOM(li,"img", ret="src")[0].encode('utf-8')

            episode_number = common.parseDOM(li,"div", attrs={"class":"user-info"})
            episode_number = common.parseDOM(episode_number, "a")[0].encode('utf-8')

            videos.append([channel,url_show+'|'+title,title,url_icon,{'Title':title+" - "+episode_number},'play'])
    return videos
    
def getVideoURL(channel,params):
    url_video = params.split('|')[0]
    title = params.split('|')[1]

    filePath = utils.downloadCatalog(url_video,"becurioutv_"+title+'.html',False,{}) 
    html = open(filePath).read().decode("utf-8")

    wid_line = re.search(r'wid:.*',html.encode('utf-8'),flags=0)
    wid_line = wid_line.group()
    wid_number = re.search(r'\d+',wid_line,flags=0)
    wid_number = wid_number.group()

    entry_id_line = re.search(r'entry_id:.*',html.encode('utf-8'),flags=0)
    entry_id_line = entry_id_line.group()
    entry_id = re.search(r'\".*\"',entry_id_line,flags=0)
    entry_id = entry_id.group()
    entry_id = entry_id[1:-1]
    
    url = url_player+"/p/"+wid_number+"/playManifest/entryId/"+entry_id+"/format/url/protocol/http/a.mp4"

    # Format de l'URL
    #http://cdnapi.kaltura.com/p/1819351/playManifest/entryId/1_r8ebyhur/format/url/protocol/http/a.mp4

    return url