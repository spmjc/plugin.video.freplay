# -*- coding: utf-8 -*-

import urllib2
from resources.lib import utils
import json

title = ['M6', 'W9', '6ter']
img = ['m6', 'w9', '6ter']
readyForUse = False

urlRoot = 'http://pc.middleware.6play.fr/6play/v1/platforms/' \
          'm6group_web/folders?serviceCode=%sreplay'

urlCategory = 'http://pc.middleware.6play.fr/6play/v1/platforms/' \
              'm6group_web/services/6play/folders/%s/programs' \
              '?limit=999&offset=0'

urlSubcategory = 'http://pc.middleware.6play.fr/6play/v1/platforms/' \
                 'm6group_web/services/6play/programs/%s'

urlVideos = 'http://pc.middleware.6play.fr/6play/v1/platforms/' \
            'm6group_web/services/6play/programs/%s/videos?' \
            'subcatId=%s&limit=999'

urlOtherVideos = 'http://pc.middleware.6play.fr/6play/v1/platforms/' \
                 'm6group_web/services/6play/programs/%s/videos?' \
                 'limit=999'

urlJsonVideo = 'https://pc.middleware.6play.fr/6play/v2/platforms/' \
               'm6group_web/services/6play/videos/clip_%s'\
               '?csa=6&with=clips,freemiumpacks'

urlVideo = 'http://www.6play.fr/%s-p_%s/%s-c_%s'
            #  program;code  program;id.   episode;code.   episode;id

urlImg = 'https://images.6play.fr/v1/images/%s/raw'


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
        filePath = utils.downloadCatalog(
            urlCategory % (category),
            '%s_%s.json' % (channel, category),
            False,
            {})
        filPrgm = open(filePath).read()
        jsonParser = json.loads(filPrgm)

        for array in jsonParser:
            programTitle = array['title'].encode('utf-8')
            programId = str(array['id'])
            programDesc = array['description'].encode('utf-8')
            programImgs = array['_embedded']['images']
            programImg = ''
            for img in programImgs:
                if img['role'].encode('utf-8') == 'vignette':
                    external_key = img['external_key'].encode('utf-8')
                    programImg = urlImg % (external_key)

            print 'programTitle ' + programTitle

            shows.append([
                channel,
                'subCategory|' + programId + '|' + programImg,
                programTitle,
                programImg,
                'folder'])

    elif 'subCategory' in folder:
        programId = folder.split('|')[1]
        programImg = folder.split('|')[2]
        programJson = urllib2.urlopen(urlSubcategory % (programId)).read()

        jsonParser = json.loads(programJson)
        for subCategory in jsonParser['programsubcats']:
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
            programId + '|other',
            'Les autres vidéos',
            programImg,
            'shows'])

    return shows


def list_videos(channel, id):
    videos = []

    programId = id.split('|')[0]
    subCategoryId = id.split('|')[1]

    if subCategoryId == 'other':
        programJson = urllib2.urlopen(
            urlOtherVideos % (programId)).read()
        print urlOtherVideos % (programId)

    else:
        programJson = urllib2.urlopen(
            urlVideos % (programId, subCategoryId)).read()
        print urlVideos % (programId, subCategoryId)
    jsonParser = json.loads(programJson)


    for video in jsonParser:

        programCode = video['program']['code'].encode('utf-8')
        programId = str(video['program']['id'])
        videoCode = video['code'].encode('utf-8')
        videoId = str(video['id'])

        title = video['title'].encode('utf-8')
        duration = video['duration']
        description = video['description'].encode('utf-8')
        dateDiffusion = video['last_diffusion'].encode('utf-8')
        dateDiffusion = dateDiffusion[:10]
        year = dateDiffusion[:4]
        img = ''

        if 'clip_has_images' in video:
            clip_has_images = video['clip_has_images']
            for array in clip_has_images:
                if array['image']['external_key']:
                    external_key = array['image']['external_key'].encode('utf-8')
                    img = urlImg % (external_key)

        infoLabels = {
            "Title": title,
            "Plot": description,
            'Duration': duration,
            "Aired": dateDiffusion,
            "Year": year}

        arg = programCode + '|' + programId + '|' + videoCode + '|' + videoId

        videos.append([
            channel,
            arg,
            title,
            img,
            infoLabels,
            'play'])

    return videos


def getVideoURL(channel, media_id):

    programCode = media_id.split('|')[0]
    programId = media_id.split('|')[1]
    videoCode = media_id.split('|')[2]
    videoId = media_id.split('|')[3]

    videoJson = urllib2.urlopen(urlJsonVideo % (videoId)).read()
    jsonParser = json.loads(videoJson)
    print 'getVideoURL : ' + urlJsonVideo % (videoId)

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
