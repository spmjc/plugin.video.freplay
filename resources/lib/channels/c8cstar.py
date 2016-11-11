#-*- coding: utf-8 -*-
import urllib2
import simplejson as json
from resources.lib import utils

title       = ['C8','CStar']
img         = ['c8','cstar']
readyForUse = True

url_lab_api   = 'http://lab.canal-plus.pro/web/app_prod.php/api'
url_pg_infos  = '%s/pfv' %(url_lab_api)
channel_index = {'c8':1,'cstar':2}

def list_shows(channel,folder):
    shows      = []
    webcontent = utils.get_webcontent('%s/replay/%s' %(url_lab_api,channel_index[channel]))
    catalogue  = json.loads(webcontent)
    if folder=='none':
        for categorie in catalogue :
            title = categorie['title'].encode('utf-8')
            shows.append([channel,title,title,'','folder'])
    else :
        for categorie in catalogue :
            if categorie['title'].encode('utf-8')==folder :
                programs = categorie['programs']
                for program in programs :
                    title = program['title'].encode('utf-8')
                    shows.append([channel,'%s|%s'%(folder,title),title,'','shows'])
    return shows
            
def list_videos(channel,params):
    videos     = []
    webcontent = utils.get_webcontent('%s/replay/%s' %(url_lab_api,channel_index[channel]))
    catalogue  = json.loads(webcontent)
    param_cat  = params.split('|')[0]
    param_show = params.split('|')[1]
    for categorie in catalogue :
            if categorie['title'].encode('utf-8') == param_cat :
                programs = categorie['programs']
                for program in programs :
                    if program['title'].encode('utf-8') == param_show :
                        video_done  = []
                        videos_list = []
                        videos_list.append(program['videos_recent'])
                        videos_list.append(program['videos_view'])
                        videos_list.append(program['videos_hot'])
                        for item in videos_list :
                            url_video_info = '%s/list/%s/%s' %(url_pg_infos,channel_index[channel],item)
                            webcontent     = utils.get_webcontent(url_video_info)
                            video_infos    = json.loads(webcontent)
                            for video in video_infos :
                              try :
                                  video_id = video['ID']
                                  if video_id not in video_done :
                                      infos          = {}
                                      infos['Plot']  = video['INFOS']['DESCRIPTION'].encode('utf-8')
                                      infos['Title'] = video['INFOS']['TITRAGE']['TITRE'].encode('utf-8')
                                      infos['Sub']   = video['INFOS']['TITRAGE']['SOUS_TITRE'].encode('utf-8')
                                      if infos['Sub'] != "" :
                                          infos['Title'] = "%s - [I]%s[/I]" %(infos['Title'],infos['Sub'])
                                      infos['Thumb'] = video['MEDIA']['IMAGES']['GRAND'].encode('utf-8')
                                      video_fanart   = video['MEDIA']['IMAGES']['GRAND'].encode('utf-8')
                                      video_name     = infos['Title']
                                      videos.append([channel,video_id,video_name,infos['Thumb'],infos,'play'])
                                      video_done.append(video_id)
                              except :
                                  pass
    return videos
    
def getVideoURL(channel,video_id):
    url_infos   = '%s/video/%s/%s' %(url_pg_infos,channel_index[channel],video_id)
    webcontent = utils.get_webcontent(url_infos)
    infosdic   = json.loads(webcontent)
    url_video  = infosdic['main']['MEDIA']['VIDEOS']['HLS']
    if url_video == '' :
        url_video = infosdic['main']['MEDIA']['VIDEOS']['IPAD']
    return url_video