# -*- coding: utf-8 -*-
from resources.lib import utils
import base64
import hashlib
import json
import urllib
import urllib2
import urlparse
from resources.lib import globalvar
from bs4 import BeautifulSoup
import re

title = ['TF1', 'NT1', 'HD1', 'TMC', 'XTRA']
img = ['tf1', 'nt1', 'hd1', 'tmc', 'xtra']
readyForUse = True

urlRoot = "http://www.tf1.fr/"


def list_shows(channel, param):
    shows = []

    filePath = utils.downloadCatalog(
        urlRoot + channel + '/programmes-tv',
        channel + '.html', False, {})
    rootHtml = open(filePath).read()
    rootSoup = BeautifulSoup(rootHtml, "html.parser")

    if param == 'none':  # Affichage des catégories
        categoriesSoup = rootSoup.find(
            'ul',
            attrs={'class': 'filters_2 contentopen'})
        for category in categoriesSoup.findAll('a'):
            categoryName = category.getText().encode('utf-8')
            categoryLink = category['data-target'].encode('utf-8')

            shows.append([channel, categoryLink, categoryName, '', 'folder'])

    else:  # Affichage des programmes de la catégorie
        programsSoup = rootSoup.find(
            'ul',
            attrs={'id': 'js_filter_el_container'})
        for program in programsSoup.findAll('li'):
            category = program['data-type'].encode('utf-8')
            if param == category or param == 'all':
                href = program.find(
                    'div',
                    attrs={'class': 'description'})
                href = href.find('a')['href'].encode('utf-8')
                programName = program.find(
                    'p',
                    attrs={'class': 'program'}).getText().encode('utf-8')
                img = program.find('img')
                try:
                    img = img['data-srcset'].encode('utf-8')
                except:
                    img = img['srcset'].encode('utf-8')

                img = 'http:' + img.split(',')[-1].split(' ')[0]

                shows.append([channel, href, programName, img, 'shows'])

    return shows


def list_videos(channel, id):
    videos = []

    prograHtml = urllib2.urlopen(urlRoot + id + '/videos').read()
    programSoup = BeautifulSoup(prograHtml, "html.parser")

    grid = programSoup.find(
        'ul',
        attrs={'class': 'grid'})

    for li in grid.findAll('li'):
        videoType = li.find('strong')
        videoType = videoType.getText().encode('utf-8').lower()

        if 'playlist' not in videoType:
            if 'replay' in videoType or \
               'video' in videoType or \
               globalvar.ADDON.getSetting(channel + 'Bonus') == 'true':

                title = li.find('p', attrs={'class': 'title'})
                title = title.getText().encode('utf-8')

                try:
                    stitle = li.find('p', attrs={'class': 'stitle'})
                    stitle = stitle.getText().encode('utf-8')
                except:
                    stitle = ''

                try:
                    duration = li.find(
                        'span',
                        attrs={'data-format': 'duration'})
                    duration = int(duration.getText().encode('utf-8'))
                except:
                    duration = 0

                img = li.find('img')
                try:
                    img = img['data-srcset'].encode('utf-8')
                except:
                    img = img['srcset'].encode('utf-8')

                img = 'http:' + img.split(',')[-1].split(' ')[0]

                aired = li.find(
                    'span',
                    attrs={'data-format': None, 'class': 'momentDate'})
                aired = aired.getText().encode('utf-8')
                aired = aired.split('T')[0]

                programId = li.find('a')
                programId = programId['href'].encode('utf-8')

                infoLabels = {
                    "Title": title,
                    "Plot": stitle,
                    'Duration': duration,
                    "Aired": aired,
                    "Year": aired[:4]}

                videos.append([
                    channel,
                    programId,
                    title,
                    img,
                    infoLabels,
                    'play'])

    return videos


def getVideoURL(channel, media_id):
    videoHtml = urllib2.urlopen(urlRoot + media_id).read()

    media_id = re.findall(
        r'data-src="http://www.wat.tv/embedframe/(.+?)"',
        videoHtml)

    if len(media_id) == 0:
        media_id = re.findall(
            r'data-src="//www.wat.tv/embedframe/(.+?)"',
            videoHtml)
    media_id = media_id[0]

    if '?noExport=1' in media_id or '?noExport=0' in media_id:
        media_id = media_id[:-11]

    media_id = media_id[-8:]

    """Returns the URL to use to read the given video."""
    def get_timestamp():
        """Returns the current server timestamp."""
        servertime = urllib2.urlopen('http://www.wat.tv/servertime').read()
        timestamp = servertime.split(u"""|""")[0].encode('utf-8')
        return int(timestamp)

    def get_auth_key(app_name, media_id, timestamp):
        """Return the AuthKey to use to get the Video URL."""
        secret = base64.b64decode('VzNtMCMxbUZJ')
        string = '%s-%s-%s-%s-%d' % (
            media_id,
            secret,
            app_name,
            secret,
            timestamp)
        #  auth_key = hashlib.md5(
        #    bytearray(string)).hexdigest() + '/' + str(timestamp)
        auth_key = hashlib.md5(string).hexdigest() + '/' + str(timestamp)
        return auth_key

    user_agent = 'myTF1/60010000.15040209 CFNetwork/609 Darwin/13.0.0'
    app_name = 'sdk/Iphone/1.0'
    method = 'getUrl'
    timestamp = get_timestamp()
    version = '1.4.32'
    auth_key = get_auth_key(app_name, media_id, timestamp)
    hosting_application_name = 'com.tf1.applitf1'
    hosting_application_version = '60010000.15040209'

    req = urllib2.Request('http://api.wat.tv/services/Delivery')
    req.add_header('User-Agent', user_agent)
    req.add_data(
        ('appName=%s&method=%s&mediaId=%s&authKey=%s&version=%s'
         '&hostingApplicationName=%s&hostingApplicationVersion=%s')
        % (app_name, method, media_id, auth_key, version,
           hosting_application_name, hosting_application_version))
    print 'Loading ' + req.get_full_url() + ' ' + req.get_data()
    data = json.loads(urllib2.urlopen(req).read())
    print 'Response: ' + repr(data)
    if int(data['code']) != 200:
        # Something is not working, fall back to the simple url scheme.
        return 'http://wat.tv/get/ipad/' + media_id + '.m3u8'

    m3u8_url = data['message']

    if globalvar.ADDON.getSetting('tf1ForceHD') == 'true':
        (scheme,
         netloc,
         path,
         query_string,
         fragment) = urlparse.urlsplit(m3u8_url)
        query_params = urlparse.parse_qs(query_string)
        query_params.pop('bwmax', None)
        new_query_string = urllib.urlencode(query_params, doseq=True)
        m3u8_url = urlparse.urlunsplit((scheme,
                                        netloc,
                                        path,
                                        new_query_string,
                                        fragment))

    # The URL returned by '/services/Delivery' will return a 302 and this seems
    # to confuse the media player. So we first follow and 302 chain and return
    # the final real address.
    req = urllib2.Request(m3u8_url)
    req.add_header('User-Agent', user_agent)
    print 'Loading ' + req.get_full_url()
    response = urllib2.urlopen(req)
    return response.url + '|User-Agent=' + urllib2.quote(user_agent)
