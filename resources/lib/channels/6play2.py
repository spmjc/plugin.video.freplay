# -*- coding: utf-8 -*-

import os
import urllib2
from resources.lib import utils
from resources.lib import globalvar
from resources.lib import log
import json

title = ['M6', 'W9', '6ter']
img = ['m6', 'w9', '6ter']
readyForUse = True

# Pour connaitre les catégories de la chaine
# (Info, Divertissement, Séries ...)
# On récuère un id
urlRoot = 'http://pc.middleware.6play.fr/6play/v2/platforms/' \
          'm6group_web/services/%sreplay/folders?limit=999&offset=0'

# Pour connaitre les programmes de cette catégorie
# (Le meilleur patissier, La france à un incroyable talent, ...)
# On récupère un id
urlCategory = 'http://pc.middleware.6play.fr/6play/v2/platforms/' \
              'm6group_web/services/6play/folders/%s/programs' \
              '?limit=999&offset=0&csa=1&with=parentcontext'

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
            'csa=6&with=clips,freemiumpacks&type=vi,vc,playlist&limit=999'\
            '&offset=0&subcat=%s&sort=subcat'

urlVideos2 = 'https://pc.middleware.6play.fr/6play/v2/platforms/' \
             'm6group_web/services/6play/programs/%s/videos?' \
             'csa=6&with=clips,freemiumpacks&type=vi&limit=999&offset=0'

# Pour aller sur la page de la video
urlJsonVideo = 'https://pc.middleware.6play.fr/6play/v2/platforms/' \
               'm6group_web/services/6play/videos/%s'\
               '?csa=6&with=clips,freemiumpacks'


urlImg = 'https://images.6play.fr/v1/images/%s/raw'


def list_shows(channel, folder):
    shows = []

    if folder == 'none':
        filePath = utils.download_catalog(
            urlRoot % (channel),
            '%s.json' % (channel),
            False,
            random_ua=True)
        filPrgm = open(filePath).read()
        jsonParser = json.loads(filPrgm)

        # do not cache failed catalog fetch
        # the error format is:
        #   {"error":{"code":403,"message":"Forbidden"}}
        if isinstance(jsonParser, dict) and \
                'error' in jsonParser.keys():
            os.remove(filePath)
            raise Exception('Failed to fetch the 6play catalog')

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
        req = urllib2.Request(
            urlCategory % (category),
            headers=utils.get_random_ua_hdr())
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
        req = urllib2.Request(
            urlSubcategory % (programId),
            headers=utils.get_random_ua_hdr())
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

        shows.append([
                channel,
                programId + '|' + 'null',
                'Toutes les vidéos',
                programImg,
                'shows'])

    return shows


def list_videos(channel, id):
    videos = []

    programId = id.split('|')[0]
    subCategoryId = id.split('|')[1]
    if subCategoryId == 'null':
        url = urlVideos2 % programId
    else:
        url = urlVideos % (programId, subCategoryId)
    req = urllib2.Request(
        url,
        headers=utils.get_random_ua_hdr())
    programJson = urllib2.urlopen(req).read()
    jsonParser = json.loads(programJson)

    for video in jsonParser:
        videoId = str(video['id'])

        title = video['title'].encode('utf-8')
        duration = video['clips'][0]['duration']/60
        description = video['description'].encode('utf-8')
        try:
            dateDiffusion = video['clips'][0]['product']['last_diffusion']
            dateDiffusion = dateDiffusion.encode('utf-8')
            dateDiffusion = dateDiffusion[:10]
            year = dateDiffusion[:4]

        except:
            dateDiffusion = ''
            year = ''
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
        headers=utils.get_random_ua_hdr())
    videoJson = urllib2.urlopen(req).read()
    jsonParser = json.loads(videoJson)

    videoAssets = jsonParser['clips'][0]['assets']
    url = ''
    url2 = ''
    url3 = ''
    for asset in videoAssets:
        if 'ism' in asset['video_container'].encode('utf-8'):
            url = asset['full_physical_path'].encode('utf-8')
        if 'mp4' in asset['video_container'].encode('utf-8'):
            if 'hd' in asset['video_quality'].encode('utf-8'):
                url2 = asset['full_physical_path'].encode('utf-8')
        else:
            url3 = asset['full_physical_path'].encode('utf-8')
    manifest_url = ''
    if url:
        manifest_url = url
    elif url2:
        manifest_url = url2
    else:
        manifest_url = url3

    req = urllib2.Request(
        manifest_url,
        headers=utils.get_random_ua_hdr())
    manifest = urllib2.urlopen(req).read()
    if 'drm' in manifest:
        msg = 'Vidéo protégée par DRM'
        log.logError(msg, msg)
        return ''

    if globalvar.ADDON.getSetting('6playQuality') == 'Auto':
        return manifest_url

    root = os.path.dirname(manifest_url)

    url_sd = ''
    url_hd = ''
    url_ultra_sd = ''
    url_ultra_hd = ''

    lines = manifest.splitlines()
    for k in range(0, len(lines) - 1):
        if 'RESOLUTION=400' in lines[k]:
            url_ultra_sd = root + '/' + lines[k + 1]
        elif 'RESOLUTION=640' in lines[k]:
            url_sd = root + '/' + lines[k + 1]
        elif 'RESOLUTION=720' in lines[k]:
            url_hd = root + '/' + lines[k + 1]
        elif 'RESOLUTION=1080' in lines[k]:
            url_ultra_hd = root + '/' + lines[k + 1]

    if globalvar.ADDON.getSetting('6playQuality') == 'Force HD':
        if url_ultra_hd:
            return url_ultra_hd
        elif url_hd:
            return url_hd
        return manifest_url

    elif globalvar.ADDON.getSetting('6playQuality') == 'Force SD':
        if url_ultra_sd:
            return url_ultra_sd
        elif url_sd:
            return url_sd
        return manifest_url
