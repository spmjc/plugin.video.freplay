# -*- coding: utf-8 -*-

import urllib2
import json
import CommonFunctions as common
from resources.lib import utils
from resources.lib import globalvar
import HTMLParser

title = ['ARTE']
img = ['arte']
readyForUse = True
url_xml = 'http://www.arte.tv/papi/tvguide-flow/sitemap/feeds/videos/F.xml'
url_player = ('http://arte.tv/papi/tvguide/videos/stream/'
              'player/F/%s/ALL/ALL.json')
dic = {
    "musique": "Musique",
    "serie-fiction": "Série fiction",
    "serie-documentaire": "Série documentaire",
    "documentaire": "Documentaire",
    "film": "Film",
    "reportage": "Reportage",
    "magazine": "Magazine",
    "telefilm": "Téléfilm"
}


def fix_text(text):
    return HTMLParser.HTMLParser().unescape(text).encode('utf-8')


def typo_correction(original_name):
    for key, value in dic.iteritems():
        if original_name == key:
            return value
    return original_name


def list_shows(channel, folder):
    shows = []
    d = dict()

    filePath = utils.downloadCatalog(url_xml, 'ARTE.XML', False, {})
    xml = open(filePath).read()
    url = common.parseDOM(xml, "url")
    if folder == 'none':
        for i in range(0, len(url)):
            categoryTab = common.parseDOM(url[i], "video:category")
            if len(categoryTab) > 0:
                category = typo_correction(fix_text(categoryTab[0]))
                if category not in d:
                        shows.append([
                            channel,
                            category,
                            category,
                            '',
                            'folder'])
                        d[category] = category
    else:
        for i in range(0, len(url)):
            categoryTab = common.parseDOM(url[i], "video:category")
            if len(categoryTab) > 0:
                show_titleTab = common.parseDOM(url[i], "video:show_title")
                if len(show_titleTab) > 0:
                    title = fix_text(show_titleTab[0])
                if globalvar.ADDON.getSetting('arteFull') == 'true':
                    videoTag = common.parseDOM(url[i], "video:tag")[0]
                else:
                    videoTag = 'ARTE+7'
                if(typo_correction(fix_text(categoryTab[0])) == folder and
                        title not in d and
                        videoTag == 'ARTE+7'):
                    shows.append([
                        channel,
                        title,
                        title,
                        '',
                        'shows'])
                    d[title] = title

    return shows


def list_videos(channel, show_title):
    videos = []
    filePath = utils.downloadCatalog(url_xml, 'ARTE.XML', False, {})
    xml = open(filePath).read()
    url = common.parseDOM(xml, "url")

    for i in range(0, len(url)):
        titleTab = common.parseDOM(url[i], "video:show_title")
        if len(titleTab) > 0:
            title = fix_text(titleTab[0])
        if title == show_title:
            title = ''
            name = ''
            image_url = ''
            date = ''
            duration = ''
            views = ''
            desc = ''
            rating = ''

            titleTab = common.parseDOM(url[i], "video:title")
            if len(titleTab) > 0:
                title = fix_text(titleTab[0])
            tmpTab = common.parseDOM(url[i], "video:publication_date")
            if len(tmpTab) > 0:
                date = tmpTab[0][:10]
            tmpTab = common.parseDOM(url[i], "video:duration")
            if len(tmpTab) > 0:
                duration = float(tmpTab[0])
            tmpTab = common.parseDOM(url[i], "video:view_count")
            if len(tmpTab) > 0:
                views = tmpTab[0]
            tmpTab = common.parseDOM(url[i], "video:rating")
            if len(tmpTab) > 0:
                rating = tmpTab[0]

            descriptionTab = common.parseDOM(url[i], "video:description")
            if len(descriptionTab) > 0:
                name = fix_text(descriptionTab[0])
                desc = fix_text(descriptionTab[0])

            tmpTab = common.parseDOM(url[i], "video:player_loc")
            if len(tmpTab) > 0:
                    if tmpTab[0] == "1":
                        tmpTab = common.parseDOM(url[i], "video:id")
                        if len(tmpTab) > 0:
                            video_id = tmpTab[0][28:28 + 10] + "_PLUS7-F"
                    else:
                        start = tmpTab[0].find("%2Fplayer%2FF%2F")
                        end = tmpTab[0].find("%2F", start + 16)
                        video_id = tmpTab[0][start + 16:end]
                        if video_id.find("EXTRAIT") > 0:
                            name = "Extrait-" + name

            videoTag = common.parseDOM(url[i], "video:tag")[0]
            picTab = common.parseDOM(url[i], "video:thumbnail_loc")
            if len(picTab) > 0:
                image_url = picTab[0]

            infoLabels = {
                "Title": title,
                "Plot": desc,
                "Aired": date,
                "Duration": duration,
                "Year": date[:4]}
            if not(globalvar.ADDON.getSetting('arteFull') == 'true' and
                    videoTag != 'ARTE+7'):
                videos.append([
                    channel,
                    video_id,
                    title,
                    image_url,
                    infoLabels,
                    'play'])
    return videos


def getVideoURL(channel, video_id):
    # Get JSON file
    jsonFile = urllib2.urlopen(url_player % (video_id)).read()
    # Parse JSON to
    jsoncat = json.loads(jsonFile)

    url = ''
    if globalvar.ADDON.getSetting('%sQuality' % (channel)) == 'HD':
        # HD HTTP
        if 'HTTP_MP4_SQ_1' in jsoncat['videoJsonPlayer']['VSR']:
            url = jsoncat['videoJsonPlayer']['VSR']['HTTP_MP4_SQ_1']['url']

        # HD RTMP
        else:
            url = jsoncat['videoJsonPlayer']['VSR']['RTMP_SQ_1']['streamer']
            url = url + jsoncat['videoJsonPlayer']['VSR']['RTMP_SQ_1']['url']
    if (globalvar.ADDON.getSetting('%sQuality' % (channel)) == 'SD' or
            url == ' '):
        # SD HTTP
        if 'HLS_SQ_1':
            url = jsoncat['videoJsonPlayer']['VSR']['HLS_SQ_1']['url']

        # SD RTMP
        else:
            url = jsoncat['videoJsonPlayer']['VSR']['RTMP_MQ_1']['streamer']
            url = url + jsoncat['videoJsonPlayer']['VSR']['RTMP_MQ_1']['url']

    return url
