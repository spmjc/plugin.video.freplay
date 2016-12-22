# -*- coding: utf-8 -*-
import urllib2
import re
from resources.lib import globalvar
from bs4 import BeautifulSoup as bs
from random import randint
import YDStreamExtractor


title = ['Allocine Émissions']
img = ['allocineemissions']
readyForUse = True

url_root = 'http://www.allocine.fr'

categories = [
    (
        'Webséries',
        '/video/cat-158001'
    ),
    (
        'Mangas',
        '/video/cat-158002'
    ),
    (
        'Parodies',
        '/video/cat-158003'
    ),
    (
        'Émissions d\'actu',
        '/video/cat-158004'
    ),
    (
        'Émissions Bonus',
        '/video/cat-158005'
    ),
    (
        'Stars',
        '/video/cat-158006'
    ),
    (
        'Films et séries en intégralité',
        '/video/cat-158007'
    )
]

sort = {
    'Pertinance': '',
    'Date d\'ajout': 'date-ajout',
    'Ordre alphabétique': 'alpha',
    'Nombre de fans': 'nb-fans'
}



user_agents = [
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36'
    ' (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14'
    ' (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14'
    ' (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
]


def get_random_headers():
    ua = user_agents[randint(0, len(user_agents) - 1)]
    hdr = {
        'DNT': '1',
        'Upgrade-Insecure-Requests': '  1',
        'Accept': ' text/html,application/xhtml+xml,'
        'application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': ua
    }
    return hdr


obf = {
    'BA': 'A',  #
    'B1': 'B',  #
    'B2': 'C',
    'BB': 'D',  #
    'B3': 'E',  #
    'B4': 'F',  #
    'BC': 'G',  #
    'B5': 'H',  #
    'B6': 'I',  #
    'BD': 'J',  #
    'B7': 'K',
    'B8': 'L',  #
    'BE': 'M',  #
    'B9': 'N',
    'BF': 'O',  #
    '30': 'P',  #
    '3A': 'Q',
    '31': 'R',  #
    '32': 'S',  #
    '3B': 'T',  #
    '33': 'U',
    '34': 'V',
    '3C': 'W',  #
    '35': 'X',
    '36': 'Y',  #
    '3D': 'Z',  #
    '4A': 'a',
    '41': 'b',
    '42': 'c',
    '4B': 'd',
    '43': 'e',
    '44': 'f',
    '4C': 'g',  #
    '45': 'h',
    '46': 'i',
    '4D': 'j',  #
    '47': 'k',  #
    '48': 'l',
    '4E': 'm',
    '49': 'n',
    '4F': 'o',
    'C0': 'p',
    'CA': 'q',  #
    'C1': 'r',
    'C2': 's',
    'CB': 't',
    'C3': 'u',
    'C4': 'v',
    'CC': 'w',  #
    'C5': 'x',  #
    'C6': 'y',
    'CD': 'z',  #
    '10': ' ',
    '11': '\"',
    '1F': '/',
    '1E': '-',
    '3F': '_',
    '19': '.',
    '28': '<',
    '29': '>',
    '2D': ':',
    '2E': '=',
    '2F': '?',
    '14': '&',
    '20': '0',
    '2A': '1',
    '21': '2',
    '22': '3',  #
    '2B': '4',  #
    '23': '5',
    '24': '6',
    '2C': '7',
    '25': '8',
    '26': '9'
}


def get_obfuscate_url(url_soup):
    if not url_soup:
        print 'Erreur : typeof(url_soup) = None'
        return ''
    elif url_soup.has_attr('href'):
        return url_soup['href'].encode('utf-8')
    elif 'ACr' in url_soup['class'][0].encode('utf-8'):
        url = url_soup['class'][0].encode('utf-8')
        url = url.replace('ACr', '')
        url = url.decode('base64')
        return url
    elif 'acLnk' in url_soup['class'] and 'link_more' not in url_soup['class']:
        url_obf = url_soup['class'][1].encode('utf-8')
        url_obf = re.findall('..', url_obf)
        url = ''
        for two in url_obf:
            try:
                url = url + obf[two]
            except:
                print 'Erreur désobfuscation URL (dict incomplet)'
        return url
    else:
        print 'Erreur get_obfuscate_url'
        return ''


def debug_url(url):
    elts = ['/pays-5000', '/decennie-0000', '/genre-13000']
    for elt in elts:
        if elt in url:
            url = url.replace(elt, '')
    if url.endswith('/?page=1'):
        url = url.replace('/?page=1', '')
    return url


def list_shows(channel, param):
    shows = []
    global categories

    if param == 'none':
        for category in categories:
            title = category[0]
            url_short = category[1]
            url_long = url_root + url_short
            shows.append([
                channel,
                '1|' + url_long,
                title,
                '',
                'folder'])

    else:
        param_list = param.split('|')
        param = param_list[0]
        url_long = param_list[1]
        url = debug_url(url_long)

        if param == '1':
            req = urllib2.Request(url, headers=get_random_headers())
            html = urllib2.urlopen(req).read()
            soup = bs(html, "html.parser")
            soup_subsub = soup.find(
                'div',
                class_='nav-button-filter')

            soup_subsub = soup_subsub.find_all('a')
            if len(soup_subsub) > 0:
                for subsub in soup_subsub:
                    title = subsub.find('span', class_='label')
                    title = title.get_text().encode('utf-8')

                    next_url = subsub['href'].encode('utf-8')
                    print 'NEXTURL ' + next_url
                    shows.append([
                        channel,
                        '2|' + next_url,
                        title,
                        '',
                        'folder'])
            else:
                print 'Pas de sous catégories ici'
                param = '2'

        if param == '2':
            url = url.replace('/cat', '/prgcat')

            for key, value in sort.iteritems():
                next_url = url_root + url + value
                shows.append([
                    channel,
                    '3|' + next_url,
                    key,
                    '',
                    'folder'])

        if param == '3':
            print 'URL 3 ' + url
            req = urllib2.Request(url, headers=get_random_headers())
            html = urllib2.urlopen(req).read()
            soup = bs(html, "html.parser")
            soup_pager = soup.find(
                'div',
                class_='pager')

            if soup_pager:
                soup_pager = soup_pager.find_all('li')
                last_page = soup_pager[len(soup_pager) - 1]
                last_page = last_page.get_text().encode('utf-8')
                last_page = int(last_page)
                for k in range(0, last_page):
                    next_url = url + '/?page=' + str(k + 1)
                    title = 'Page ' + str(k + 1)
                    shows.append([
                        channel,
                        '4|' + next_url,
                        title,
                        '',
                        'folder'])
            else:
                print 'Une seule page ici'
                param = '4'

        if param == '4':
            print 'URL 4 ' + url
            req = urllib2.Request(url, headers=get_random_headers())
            html = urllib2.urlopen(req).read()
            soup = bs(html, "html.parser")
            soup_prg = soup.find_all(
                'article',
                class_='media-meta medium poster')

            for prg in soup_prg:
                title = prg.find('h2', class_='title')
                title = title.get_text().encode('utf-8')
                title = title.replace('\n', '').replace('\r', '')

                next_url = prg.find('h2', class_='title')
                next_url = next_url.find('a')
                next_url = get_obfuscate_url(next_url)
                next_url = url_root + next_url

                img = ''
                if prg.find('img').has_attr('data-attr'):
                    img = prg.find('img')['data-attr'].encode('utf-8')
                    img = re.compile(
                        r'{"src":"(.*?)"}', re.DOTALL).findall(img)[0]
                elif prg.find('img')['src']:
                    img = prg.find('img')['src'].encode('utf-8')

                shows.append([
                    channel,
                    '5|' + next_url,
                    title,
                    img,
                    'folder'])

        if param == '5':
            print 'URL 5 ' + url
            req = urllib2.Request(url, headers=get_random_headers())
            html = urllib2.urlopen(req).read()
            soup = bs(html, "html.parser")
            soup_saisons = soup.find_all(
                ['a', 'span'],
                class_='btn-primary')

            for saisons in soup_saisons:
                if "button btn-primary btn-large" in repr(saisons):
                    title = saisons.get_text().encode('utf-8')
                    title = title.replace('\n', '').replace('\r', '')

                    next_url = get_obfuscate_url(saisons)
                    next_url = url_root + next_url

                    print 'NEXT URL : ' + next_url

                    shows.append([
                        channel,
                        next_url,
                        title,
                        '',
                        'shows'])

    return shows


def list_videos(channel, show_url):
    videos = []
    url = debug_url(show_url)

    req = urllib2.Request(url, headers=get_random_headers())
    html = urllib2.urlopen(req).read()
    soup = bs(html, "html.parser")

    pages_url = []

    soup_pager = soup.find(
        'div',
        class_='pager')

    if soup_pager:
        soup_pager = soup_pager.find_all('li')
        last_page = soup_pager[len(soup_pager) - 1]
        last_page = last_page.get_text().encode('utf-8')
        last_page = int(last_page)
        for k in range(0, last_page):
            next_url = url + '/?page=' + str(k + 1)
            pages_url.append(next_url)
    else:
        pages_url.append(url)

    for url in pages_url:
        url = debug_url(url)
        req = urllib2.Request(url, headers=get_random_headers())
        html = urllib2.urlopen(req).read()
        soup = bs(html, "html.parser")

        soup_episodes = soup.find_all(
            'article',
            class_="media-meta medium ")

        for soup_episode in soup_episodes:
            title = soup_episode.find('a').get_text().encode('utf-8')
            title = title.replace('\n', '').replace('\r', '')
            img = ''
            if soup_episode.find('img').has_attr('data-attr'):
                img = soup_episode.find('img')['data-attr'].encode('utf-8')
                img = re.compile(r'{"src":"(.*?)"}', re.DOTALL).findall(img)[0]
            elif soup_episode.find('img')['src']:
                img = soup_episode.find('img')['src'].encode('utf-8')
            url_soup = soup_episode.find('a')
            url = get_obfuscate_url(url_soup)

            try:
                description = soup_episode.find(
                    'p',
                    attrs={'itemprop': 'description'}).get_text().encode('utf-8')
            except:
                description = ''

            infoLabels = {
                "Title": title,
                "Plot": description
            }

            videos.append([
                channel,
                url,
                title,
                img,
                infoLabels,
                'play'])

    return videos


def getVideoURL(channel, url_video):
    url = url_root + url_video
    print 'URL_VIDEO : ' + url
    html = urllib2.urlopen(url).read()

    if 'dailymotion' in html:

        id_daily = re.compile(
            r'"entityPartnerID":"(.*?)",', re.DOTALL).findall(html)[0]

        url_daily = 'http://www.dailymotion.com/embed/video/' + id_daily

        print 'url_daily : ' + url_daily

        html_daily = urllib2.urlopen(url_daily).read()
        html_daily = html_daily.replace('\\', '')

        urls_mp4 = re.compile(
            r'{"type":"video/mp4","url":"(.*?)"}],"(.*?)":').findall(html_daily)

        url_sd = ''
        url_hd = ''
        url_default = ''
        for url, quality in urls_mp4:
            print quality
            if quality == '480':
                url_sd = url
            elif quality == '720':
                url_hd = url
            elif quality == '1080':
                url_hd = url
            url_default = url

        if globalvar.ADDON.getSetting('allocineQuality') == 'sd':
            if url_sd != '':
                return url_sd
            else:
                return url_default

        elif globalvar.ADDON.getSetting('allocineQuality') == 'hd':
            if url_hd != '':
                return url_hd
            else:
                return url_default
        else:
            return url_default

    else:
        embed_code = re.compile(
            r'"embedCode":"(.*?)",', re.DOTALL).findall(html)[0]

        embed_code = re.findall('..', embed_code)
        embed_code_2 = ''
        for two in embed_code:
            try:
                embed_code_2 = embed_code_2 + obf[two]
            except:
                print 'Erreur désobfuscation URL (dict incomplet)'

        url = re.compile(
            r'src="(.*?)"', re.DOTALL).findall(embed_code_2)[0]

        if 'youtube' in url or 'youtu.be' in url:
            YDStreamExtractor.disableDASHVideo(True)
            #  Kodi (XBMC) only plays the video for DASH streams,
            #  so you don't want these normally.
            #  Of course these are the only 1080p streams on YouTube
            quality = 1
            if globalvar.ADDON.getSetting('allocineQuality') == 'sd':
                quality = 0

            elif globalvar.ADDON.getSetting('allocineQuality') == 'hd':
                quality = 2
            vid = YDStreamExtractor.getVideoInfo(url, quality=quality)
            # quality is 0=SD, 1=720p, 2=1080p and is a maximum
            return vid.streamURL()
            #  This is what Kodi (XBMC) will play
        return ''
