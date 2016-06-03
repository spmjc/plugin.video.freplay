#-*- coding: utf-8 -*-
from resources.lib import utils
import re 
import CommonFunctions
from bs4 import BeautifulSoup
common = CommonFunctions   

title       = ['Télé-Québec']
img         = ['telequebec']
readyForUse = False

url_root = 'http://zonevideo.telequebec.tv'
url_shows = '%s/a-z'%url_root



def list_shows(channel,folder):
    shows = []
    filePath = utils.downloadCatalog(url_shows,'telequebec.html',False,{}) # Page principale du replay
    html = open(filePath).read().decode("utf-8")
    list_az = common.parseDOM(html,"div", attrs={"class": "list"})
    list_li = common.parseDOM(list_az, "li")
    
    if folder == 'none':
        for li in list_li:
            a = common.parseDOM(li, "a")

            title = a[0].encode('utf-8')
            title = str(BeautifulSoup(title))

            #show_icon = common.parseDOM(show,"div", attrs={"class": "shows__icon"})
            url_show = common.parseDOM(li,"a", ret="href")[0].encode('utf-8')
            url_show = url_root+url_show

            shows.append([channel,url_show+'|'+title,title,'','folder'])
    else:
        url_show = folder.split('|')[0]
        title = folder.split('|')[1]
        filePath = utils.downloadCatalog(url_show,'telequebec_'+title+'.html',False,{}) 
        html = open(filePath).read().decode("utf-8")
        saison_container = common.parseDOM(html,"div", attrs={"class":"saisonsContainer"})
        list_item = common.parseDOM(saison_container,"div", attrs={"class":"item"})
        for item in list_item:
            url_video = common.parseDOM(item,"a", ret="href")[0].encode('utf-8')
            url_video = url_root+url_video

            url_img = common.parseDOM(item,"img", ret="src")[0].encode('utf-8')

            title = common.parseDOM(item,"a")[1].encode('utf-8')

            infos = common.parseDOM(item,"p")[0].encode('utf-8')

            shows.append([channel,url_video+'|'+title,title+" - "+infos,url_img,'shows'])
    return shows
            
def list_videos(channel,params):
    videos      = []                  
    program_url = params.split('|')[0]
    titre_program      = params.split('|')[1]

    filePath = utils.downloadCatalog(program_url,'telequebec_'+titre_program+'.html',False,{})
    html     = open(filePath).read().decode("utf-8")

    # season_grid = common.parseDOM(html,"div",attrs={"class":"seasons-grid tab-season"})

    # for season in season_grid:
    #     list_li = common.parseDOM(season,"li")
    #     for li in list_li:
    #         title_h5 = common.parseDOM(li,"h5")
    #         title = common.parseDOM(title_h5,"a")[0].encode('utf-8')
    #         #title = common.replaceHTMLCodes(title)

    #         url_show = common.parseDOM(title_h5,"a", ret="href")[0].encode('utf-8')
    #         url_show = url_root+url_show

    #         url_icon = common.parseDOM(li,"img", ret="src")[0].encode('utf-8')

    #         episode_number = common.parseDOM(li,"div", attrs={"class":"user-info"})
    #         episode_number = common.parseDOM(episode_number, "a")[0].encode('utf-8')

    #videos.append([channel,program_url+'|'+'title','title','url_icon',{'Title':'title'+" - "+'episode_number'},'play'])
    return videos
    
def getVideoURL(channel,params):
    url = "https://player.telequebec.tv/Content/swf/tq-video-player-swf-20160321T1530-r10.swf/playerForm=67c4a18ac2ff4d4caa90ec139f5571cc&mediaId=732725448adf47559560d60e9fab7e61&mediaID=732725448adf47559560d60e9fab7e61&playerID=LlPlayer_558279764373&autoPlay=true&permalink=http://zonevideo.telequebec.tv/media/24617/les-rats/100-animal&showSharingTools=true&skin="
    # url_video = params.split('|')[0]
    # title = params.split('|')[1]

    # filePath = utils.downloadCatalog(url_video,"becurioutv_"+title+'.html',False,{}) 
    # html = open(filePath).read().decode("utf-8")

    # wid_line = re.search(r'wid:.*',html.encode('utf-8'),flags=0)
    # wid_line = wid_line.group()
    # wid_number = re.search(r'\d+',wid_line,flags=0)
    # wid_number = wid_number.group()

    # entry_id_line = re.search(r'entry_id:.*',html.encode('utf-8'),flags=0)
    # entry_id_line = entry_id_line.group()
    # entry_id = re.search(r'\".*\"',entry_id_line,flags=0)
    # entry_id = entry_id.group()
    # entry_id = entry_id[1:-1]
    
    # url = url_player+"/p/"+wid_number+"/playManifest/entryId/"+entry_id+"/format/url/protocol/http/a.mp4"

    # Format de l'URL
    #http://cdnapi.kaltura.com/p/1819351/playManifest/entryId/1_r8ebyhur/format/url/protocol/http/a.mp4

    return url