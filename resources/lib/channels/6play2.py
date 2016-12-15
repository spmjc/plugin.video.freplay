# -*- coding: utf-8 -*-

import urllib2
from resources.lib import utils
import json

title = ['M6', 'W9', '6ter']
img = ['m6', 'w9', '6ter']
readyForUse = True

# Pour connaitre les catégories de la chaine
# (Info, Divertissement, Séries ...)
# On récuère un id
urlRoot = 'http://pc.middleware.6play.fr/6play/v2/platforms/' \
          'm6group_web/services/%sreplay/folders?limit=10000&offset=0'

# Pour connaitre les programmes de cette catégorie
# (Le meilleur patissier, La france à un incroyable talent, ...)
# On récupère un id
urlCategory = 'http://pc.middleware.6play.fr/6play/v2/platforms/' \
              'm6group_web/services/6play/folders/%s/programs' \
              '?limit=1000&offset=0&csa=9&with=parentcontext'

# Pour connaitres les dossiers de ce programme
# (Saison 5, Les meilleurs moments, les recettes pas à pas, ...)
# On récupère un id
urlSubcategory = 'http://pc.middleware.6play.fr/6play/v2/platforms/' \
                 'm6group_web/services/6play/programs/%s' \
                 '?with=links,subcats,rights'


# Pour connaitre les videos de ce dossier
# (Episode 1, Episode 2, ...)
urlVideos = 'http://pc.middleware.6play.fr/6play/v2/platforms/' \
            'm6group_web/services/6play/programs/%s/videos?' \
            'csa=6&with=clips,freemiumpacks&type=vi,vc,playlist&limit=9999'\
            '&offset=0&subcat=%s&sort=subcat'


# Pour aller sur la page de la video
urlJsonVideo = 'https://pc.middleware.6play.fr/6play/v2/platforms/' \
               'm6group_web/services/6play/videos/%s'\
               '?csa=9&with=clips,freemiumpacks'


urlImg = 'https://images.6play.fr/v1/images/%s/raw'


hdr = {
    'User-Agent': 'Mozilla/5.0'
}


def list_shows(channel, folder):
    shows = []

    if folder == 'none':
        filePath = utils.downloadCatalog(
            urlRoot % (channel),
            '%s.json' % (channel),
            False,
            {})
        filPrgm = open(filePath).read()
        jsonParser = json.loads(filPrgm)

        for array in jsonParser:
            categoryId = str(array['id'])
            categoryName = array['name'].encode('utf-8')

            shows.append([
                channel,
                'category|' + categoryId,
                categoryName,
                '',
                'folder'])

    elif 'category' in folder:
        category = folder.split('|')[1]
        req = urllib2.Request(urlCategory % (category), headers=hdr)
        filPrgm = urllib2.urlopen(req).read()
        jsonParser = json.loads(filPrgm)

        for array in jsonParser:
            programTitle = array['title'].encode('utf-8')
            programId = str(array['id'])
            programDesc = array['description'].encode('utf-8')
            programImgs = array['images']
            programImg = ''
            for img in programImgs:
                if img['role'].encode('utf-8') == 'vignette':
                    external_key = img['external_key'].encode('utf-8')
                    programImg = urlImg % (external_key)

            shows.append([
                channel,
                'subCategory|' + programId + '|' + programImg,
                programTitle,
                programImg,
                'folder'])

    elif 'subCategory' in folder:
        programId = folder.split('|')[1]
        programImg = folder.split('|')[2]
        req = urllib2.Request(urlSubcategory % (programId), headers=hdr)
        print urlSubcategory % (programId)
        programJson = urllib2.urlopen(req).read()

        jsonParser = json.loads(programJson)
        for subCategory in jsonParser['program_subcats']:
            subCategoryId = str(subCategory['id'])
            subCategoryTitle = subCategory['title'].encode('utf-8')

            shows.append([
                channel,
                programId + '|' + subCategoryId,
                subCategoryTitle,
                programImg,
                'shows'])

    return shows


def list_videos(channel, id):
    videos = []

    programId = id.split('|')[0]
    subCategoryId = id.split('|')[1]
    req = urllib2.Request(
        urlVideos % (programId, subCategoryId),
        headers=hdr)
    programJson = urllib2.urlopen(req).read()
    print urlVideos % (programId, subCategoryId)
    jsonParser = json.loads(programJson)

    for video in jsonParser:
        videoId = str(video['id'])

        title = video['title'].encode('utf-8')
        duration = video['clips'][0]['duration']
        description = video['description'].encode('utf-8')
        dateDiffusion = video['clips'][0]['product']['last_diffusion']
        dateDiffusion = dateDiffusion.encode('utf-8')
        dateDiffusion = dateDiffusion[:10]
        year = dateDiffusion[:4]
        img = ''

        programImgs = video['clips'][0]['images']
        programImg = ''
        for img in programImgs:
                if img['role'].encode('utf-8') == 'vignette':
                    external_key = img['external_key'].encode('utf-8')
                    programImg = urlImg % (external_key)

        infoLabels = {
            "Title": title,
            "Plot": description,
            'Duration': duration,
            "Aired": dateDiffusion,
            "Year": year}

        videos.append([
            channel,
            videoId,
            title,
            programImg,
            infoLabels,
            'play'])

    return videos


def getVideoURL(channel, media_id):

    req = urllib2.Request(
        urlJsonVideo % (media_id),
        headers=hdr)
    videoJson = urllib2.urlopen(req).read()
    jsonParser = json.loads(videoJson)

    videoAssets = jsonParser['clips'][0]['assets']
    url = ''
    for asset in videoAssets:
        if 'ism' in asset['video_container'].encode('utf-8'):
            url = asset['full_physical_path'].encode('utf-8')
        if 'mp4' in asset['video_container'].encode('utf-8'):
            if 'hd' in asset['video_quality'].encode('utf-8'):
                url2 = asset['full_physical_path'].encode('utf-8')

    if url:
        return url
    else:
        return url2
