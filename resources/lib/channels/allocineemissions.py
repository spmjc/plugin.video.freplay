# -*- coding: utf-8 -*-
import re
from resources.lib import globalvar
from bs4 import BeautifulSoup as bs
#import YDStreamExtractor
from resources.lib import utils


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
    'Trier par pertinance': '',
    'Trier par date d\'ajout': '/date-ajout',
    'Trier par ordre alphabétique': '/alpha',
    'Trier par nombre de fans': '/nb-fans'
}


# hdr = {
#     'Upgrade-Insecure-Requests': '  1',
#     'Accept': ' text/html,application/xhtml+xml,'
#     'application/xml;q=0.9,*/*;q=0.8',
#     'User-Agent': ua
# }

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
    '13': '%',
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


def get_obfuscate_url_string(url_string):
    url_string = re.findall('..', url_string)
    url = ''
    for two in url_string:
        try:
            url = url + obf[two]
        except:
            url = url + '?' + two + '?'
            print 'Erreur désobfuscation URL (dict incomplet)'
    return url


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
            print 'URL 1 ' + url
            file_path = utils.download_catalog(
                url,
                url + '.html',
                random_ua=True)
            html = open(file_path).read()
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
            print 'URL 2 : ' + url
            for key, value in sort.iteritems():
                if url_root not in url:
                    next_url = url_root + url + value
                else:
                    next_url = url + value
                shows.append([
                    channel,
                    '3|' + next_url,
                    key,
                    '',
                    'folder'])

        if param == '3':
            print 'URL 3 ' + url

            shows.append([
                channel,
                url,
                'Toutes les vidéos',
                '',
                'shows'])

            url = url.replace('/cat', '/prgcat')

            shows.append([
                channel,
                '4|' + url,
                'Les programmes',
                '',
                'folder'])

        if param == '4':
            print 'URL 4 ' + url
            file_path = utils.download_catalog(
                url,
                url + '.html',
                random_ua=True)
            html = open(file_path).read()
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

            soup_pager = soup.find(
                'div',
                class_='pager')

            if soup_pager:
                soup_pager = soup_pager.find_all('li')
                current_page = ''
                for li in soup_pager:
                    try:
                        span = li.find('span')
                        if not span.has_attr('class'):
                            current_page = li.get_text().encode('utf-8')
                            break
                    except:
                        a = li.find('a')
                        if not a.has_attr('class'):
                            current_page = li.get_text().encode('utf-8')
                            break
                print 'CURRENT PAGE ' + current_page
                current_page = int(current_page)
                last_page = soup_pager[len(soup_pager) - 1]
                last_page = last_page.get_text().encode('utf-8')
                print 'LAST PAGE ' + last_page

                last_page = int(last_page)
                if current_page < last_page:
                    if 'page' in url:
                        next_url = url[:-1] + str(current_page + 1)
                    else:
                        next_url = url + '/?page=' + str(current_page + 1)
                    shows.append([
                        channel,
                        '4|' + next_url,
                        'Page suivante (page ' + str(current_page + 1) + ')',
                        '',
                        'folder'])
                else:
                    print 'Je suis à la dernière page'
            else:
                print 'Une seule page ici'

        if param == '5':
            print 'URL 5 ' + url
            file_path = utils.download_catalog(
                url,
                url + '.html',
                random_ua=True)
            html = open(file_path).read()
            soup = bs(html, "html.parser")
            soup_saisons = soup.find_all(
                ['a', 'span'],
                class_='btn-primary')

            len_saisons = 0

            for saisons in soup_saisons:
                if "button btn-primary btn-large" in repr(saisons):
                    len_saisons += 1
                    title = saisons.get_text().encode('utf-8')
                    title = title.replace('\n', '').replace('\r', '')

                    next_url = get_obfuscate_url(saisons)
                    next_url = url_root + next_url

                    shows.append([
                        channel,
                        next_url,
                        title,
                        '',
                        'shows'])

            if len_saisons == 0:
                print 'Pas de saison ici, seulements des vidéos en vrac'
                shows.append([
                    channel,
                    url,
                    'Toutes les vidéos',
                    '',
                    'shows'])

    return shows


def list_videos(channel, show_url):
    print 'LIST VIDEOS url : ' + show_url
    videos = []
    url = debug_url(show_url)

    file_path = utils.download_catalog(
        url,
        url + '.html',
        random_ua=True)
    html = open(file_path).read()
    soup = bs(html, "html.parser")

    url_page = debug_url(url)
    file_path = utils.download_catalog(
        url_page,
        url_page + '.html',
        random_ua=True)
    html = open(file_path).read()

    soup = bs(html, "html.parser")

    soup_episodes = soup.find_all(
        'article',
        class_="media-meta medium ")

    for soup_episode in soup_episodes:
        try:
            title = soup_episode.find('a').get_text().encode('utf-8')
            title = title.replace('\n', '').replace('\r', '')
            url_soup = soup_episode.find('a')
            url = get_obfuscate_url(url_soup)
        except:
            title_h3 = soup_episode.find('h3')
            title = title_h3.get_text().encode('utf-8')
            title = title.replace('\n', '').replace('\r', '')
            url_soup = title_h3.find('span', attrs={'itemprop': 'url'})
            url = get_obfuscate_url(url_soup)
        img = ''
        if soup_episode.find('img').has_attr('data-attr'):
            img = soup_episode.find('img')['data-attr'].encode('utf-8')
            img = re.compile(r'{"src":"(.*?)"}', re.DOTALL).findall(img)[0]
        elif soup_episode.find('img')['src']:
            img = soup_episode.find('img')['src'].encode('utf-8')

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

    soup_pager = soup.find(
        'div',
        class_='pager')

    if soup_pager:
        soup_pager = soup_pager.find_all('li')
        current_page = ''
        for li in soup_pager:
            try:
                span = li.find('span')
                if not span.has_attr('class'):
                    current_page = li.get_text().encode('utf-8')
                    break
            except:
                a = li.find('a')
                if not a.has_attr('class'):
                    current_page = li.get_text().encode('utf-8')
                    break
        print 'CURRENT PAGE ' + current_page
        current_page = int(current_page)
        last_page = soup_pager[len(soup_pager) - 1]
        last_page = last_page.get_text().encode('utf-8')
        print 'LAST PAGE ' + last_page

        last_page = int(last_page)
        if current_page < last_page:
            if 'page' in url_page:
                next_url = url_page[:-1] + str(current_page + 1)
            else:
                next_url = url_page + '/?page=' + str(current_page + 1)
            videos.append([
                channel,
                next_url,
                'Page suivante (page ' + str(current_page + 1) + ')',
                '',
                {},
                'shows'])
        else:
            print 'Je suis à la dernière page'
    else:
        print 'Une seule page ici'

    return videos


def getVideoURL(channel, url_video):
    url = url_root + url_video
    print 'URL_VIDEO : ' + url

    file_path = utils.download_catalog(
        url,
        url + '.html',
        random_ua=True)
    html = open(file_path).read()

    url_default = ''
    url_sd = ''
    url_hd = ''

    if 'dailymotion' in html:

        id_daily = re.compile(
            r'"entityPartnerID":"(.*?)",', re.DOTALL).findall(html)[0]
        url_daily = 'http://www.dailymotion.com/embed/video/' + id_daily

        #html_daily = urllib2.urlopen(url_daily).read()
        file_path = utils.download_catalog(
                url_daily,
                url_daily + '.html')
        html_daily = open(file_path).read()
        html_daily = html_daily.replace('\\', '')

        urls_mp4 = re.compile(
            r'{"type":"video/mp4","url":"(.*?)"}],"(.*?)":').findall(html_daily)

        for url, quality in urls_mp4:
            print quality
            if quality == '480':
                url_sd = url
            elif quality == '720':
                url_hd = url
            elif quality == '1080':
                url_hd = url
            url_default = url

    elif 'embedCode' in html:
        embed_code = re.compile(
            r'"embedCode":"(.*?)",', re.DOTALL).findall(html)[0]
        embed_code_2 = get_obfuscate_url_string(embed_code)

        url = re.compile(
            r'src="(.*?)"', re.DOTALL).findall(embed_code_2)[0]

        if 'youtube' in url or 'youtu.be' in url:
            YDStreamExtractor.disableDASHVideo(True)
            #  Kodi (XBMC) only plays the video for DASH streams,
            #  so you don't want these normally.
            #  Of course these are the only 1080p streams on YouTube
            vid = YDStreamExtractor.getVideoInfo(url, quality=2)
            # quality is 0=SD, 1=720p, 2=1080p and is a maximum
            url_hd = vid.streamURL()
            #  This is what Kodi (XBMC) will play
            vid = YDStreamExtractor.getVideoInfo(url, quality=0)
            url_sd = vid.streamURL()

            vid = YDStreamExtractor.getVideoInfo(url, quality=1)
            url_default = vid.streamURL()

        elif 'facebook' in url:
            file_path = utils.download_catalog(
                url,
                url + '.html',
                random_ua=True)
            html = open(file_path).read()
            html = html.replace('\\', '')

            url_default = ''
            try:
                url_hd = re.compile(
                    r'"hd_src_no_ratelimit":"(.*?)"', re.DOTALL).findall(html)[0]
                url_default = url_hd
            except:
                url_hd = ''

            try:
                url_sd = re.compile(
                    r'"hs_src_no_ratelimit":"(.*?)"', re.DOTALL).findall(html)[0]
                url_default = url_sd
            except:
                url_sd = ''

        else:
            return ''

    elif 'html5Path' in html:
        if 'html5PathHD' in html:
            html5PathHD = re.compile(
                r'"html5PathHD":"(.*?)",', re.DOTALL).findall(html)[0]
            url_hd = get_obfuscate_url_string(html5PathHD)

        if 'html5PathM' in html:
            html5PathM = re.compile(
                r'"html5PathM":"(.*?)",', re.DOTALL).findall(html)[0]

            url_sd = get_obfuscate_url_string(html5PathM)

        else:
            html5PathL = re.compile(
                r'"html5PathL":"(.*?)",', re.DOTALL).findall(html)[0]

            url_default = get_obfuscate_url_string(html5PathL)

    else:
        print 'Erreur : provider vidéo inconnu'
        return ''

    if globalvar.ADDON.getSetting('allocineQuality') == 'sd':
        if url_sd:
            return url_sd
        else:
            return url_default

    elif globalvar.ADDON.getSetting('allocineQuality') == 'hd':
        if url_hd:
            return url_hd
        else:
            return url_default
    else:
        return url_default
