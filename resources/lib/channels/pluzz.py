#-*- coding: utf-8 -*-
import zipfile
import json
import resources.lib.utils as utils           

title=['France 1','France 2', 'France 3', 'France 4', 'France 5', 'France O']
img=['france1' ,'france2','france3','france4','france5','franceo']
readyForUse=True

filePath=utils.downloadCatalog('http://webservices.francetelevisions.fr/catchup/flux/flux_main.zip','Pluzz.zip',False)
catalogconffilename = "message_FT.json"
catalogcatfilename  = "categories.json"
url_base_videos= "http://medias2.francetv.fr/catchup-mobile"
url_base_images= "http://www.pluzz.fr"
    
def list_shows(channel,folder):
    shows=[]
    
    if folder=='none':                     
        zf          = zipfile.ZipFile(filePath)
        data        = zf.read(catalogcatfilename)
        jsoncat     = json.loads(data.decode('iso-8859-1'))
        categories  = jsoncat['categories']
        for cat in categories :
            shows.append( [channel,cat['titre'].encode('utf-8'), cat['titre'].encode('utf-8'),'','folder'] )
    else:
        zf          = zipfile.ZipFile(filePath)
        data        = zf.read('catch_up_' + channel + '.json')
        jsoncatalog = json.loads(data)
        programmes  = jsoncatalog['programmes']
        d=dict()
        for programme in programmes :
            video_cat = programme['rubrique'].encode("utf-8")
            if video_cat == folder:
                video_name  = programme['titre'].encode("utf-8")
                if video_name not in d :
                    d[video_name]=video_name
                    video_url   = ''
                    video_image = ''
                    video_infos = {}
                    if programme['accroche'] :
                        video_infos['Plot']  = programme['accroche'].encode("utf-8")
                    if programme['realisateurs'] :
                        video_infos['Cast']      = programme['acteurs'].encode("utf-8")
                    if programme['realisateurs'] :
                        video_infos['Director']  = programme['realisateurs'].encode("utf-8")
                    if programme['format'] :
                        video_infos['Genre']     = programme['format'].encode("utf-8")
                    shows.append( [channel,video_name,video_name,'','shows'] )
  
    return shows    

def getVideoURL(channel,video_URL):
    return video_URL

def list_videos(channel,show_title):
    videos=[]     
    
    zf          = zipfile.ZipFile(filePath)
    data        = zf.read('catch_up_' + channel + '.json')
    jsoncatalog = json.loads(data)
    programmes  = jsoncatalog['programmes']
    for programme in programmes :
        name  = programme['titre'].encode("utf-8")
        if name == show_title :
            desc=''
            duration=0
            date=''
            if programme['date'] :
                date      = str(programme['date'].split('-')[2])+'-'+str(programme['date'].split('-')[1])+'-'+str(programme['date'].split('-')[0])
                
            if programme['sous_titre'] != "" :
                name  = name +' : '+programme['sous_titre'].encode("utf-8") 
            else:
                name+=' - ' + date
            video_url   = url_base_videos+programme['url_video'].encode("utf-8")
            image_url = url_base_images+programme['url_image_racine'].encode("utf-8")+'.'+programme['extension_image'].encode("utf-8")
            if programme['accroche'] :
                desc      = programme['accroche'].encode("utf-8")
            if programme['duree'] :
                duration  = programme['duree'].encode("utf-8")
            infoLabels={ "Title": name,"Plot":desc,"Aired":date,"Duration": duration, "Year":date[:4]}
            videos.append( [channel, video_url, name, image_url,infoLabels,'play'] )

    return videos