# -*- coding: utf-8 -*-
import urllib2
import re
import CommonFunctions as common
from resources.lib import utils
from resources.lib import globalvar
from bs4 import BeautifulSoup as bs


title = ['Allocine']
img = ['allocine']
readyForUse = True

url_root = 'http://allocine.fr'


categories = [
    ('Cinéma', '/film'),
    ('Séries', '/series'),
    ('Émissions', '/video'),
    ('News', '/news')
]

sub_categories = {
    '/film': [
        ('Bandes-annonces', '/video/bandes-annonces'),  # Fait
        ('Meilleurs films', '/film/meilleurs'),  # Non fait
        ('Films à l\'affiche', '/film/aucinema'),  # Non fait
        ('Prochainement', '/film/attendus'),  # Non fait
        ('Films pour enfants', '/film/enfants/aucinema')  # Non fait
    ]
}

sub_sub_categories = {
    '/video/bandes-annonces': [
        ('Bandes-annonces', '/video/bandes-annonces'),
        ('Extraits', '/video/extraits'),
        ('Vidéos Bonus', '/video/bonus'),
    ],

    '/film/meilleurs': [
        ('Selon les spectateurs', '/film/meilleurs'),
        ('Extraits', '/video/extraits'),
        ('Vidéos Bonus', '/video/bonus'),
    ]
}

sub_sub_sub_categories = {
    '/video/bandes-annonces': [
        ('À ne pas manquer', '/video/bandes-annonces', '0'),
        ('Les plus récentes', '/video/bandes-annonces/plus-recentes', '0'),
        ('Binetôt au cinéma', '/video/bandes-annonces/prochainement', '0'),
    ],

    '/video/extraits': [
        ('Les plus consultés', '/video/extraits', '1'),
        ('Date d\'ajout', '/video/extraits/date-ajout', '1')
    ],

    '/video/bonus': [
        ('Les plus consultées', '/video/bonus', '2'),
        ('Date d\'ajout', '/video/bonus/date-ajout', '2')
    ]

}


def list_shows(channel, param):
    shows = []

    if param == 'none':
        for category in categories:
            shows.append([
                channel,
                'sub|' + category[1] + '|' + 'a',
                category[0],
                '',
                'folder'])
    else:
        param_list = param.split('|')
        print repr(param_list)
        depth = param_list[0]
        param = param_list[1]
        page_type = param_list[2]
        if depth == 'sub':
            sub_category = sub_categories[param]
            for sub_sub_category in sub_category:
                shows.append([
                    channel,
                    'sub_sub|' + sub_sub_category[1] + '|' + ' ',
                    sub_sub_category[0],
                    '',
                    'folder'])
        elif depth == 'sub_sub':
            sub_sub_category = sub_sub_categories[param]
            for sub_sub_sub_category in sub_sub_category:
                shows.append([
                    channel,
                    'sub_sub_sub|' + sub_sub_sub_category[1] + '|' + ' ',
                    sub_sub_sub_category[0],
                    '',
                    'folder'])

        elif depth == 'sub_sub_sub':
            sub_sub_sub_category = sub_sub_sub_categories[param]
            for sub_sub_sub_sub_category in sub_sub_sub_category:
                shows.append([
                    channel,
                    'page|' + sub_sub_sub_sub_category[1] + '|' + sub_sub_sub_sub_category[2],
                    sub_sub_sub_sub_category[0],
                    '',
                    'folder'])

        elif depth == 'page':
            url = url_root + param
            print 'url : ' + url
            url_refer = ''
            if 'page' in url:
                print 'url toto ' + url[:-8]
                url_refer = url[:-8]
            hdr = {
                # 'Referer': url_refer,
                # 'Upgrade-Insecure-Requests': '  1',
                # 'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0'
            }

            req = urllib2.Request(url, headers=hdr)
            html = urllib2.urlopen(req).read()
            # filePath = utils.downloadCatalog(
            #     url,
            #     'titi.html', False, {})
            # html = open(filePath).read()
            soup = bs(html, "html.parser")
            soup_pager = soup.find(
                'div',
                attrs={'class': 'pager'})

            if len(soup_pager) > 0:
                soup_pager_li = soup_pager.find('ul').find_all('li')

                for li in soup_pager_li:
                    url_page = ''
                    current_page = ''

                    if li.find('span'):
                        current_page = li.find('span')
                        current_page = current_page.get_text().encode('utf-8')
                    elif li.find('a'):
                        current_page = li.find('a').get_text().encode('utf-8')

                    url_page = param + '/?page=' + current_page
                    print 'URL : ' + url_page
                    shows.append([
                        channel,
                        'shows|' + url_page + '|' + page_type,
                        'Page ' + current_page,
                        '',
                        'shows'])

    return shows


def list_videos(channel, show_url):
    videos = []

    # url = url_root + show_url.split('|')[1]
    # page_type = param.split('|')[2]
    
    param_list = show_url.split('|')
    print repr(param_list)
    # depth = param_list[0]
    url = url_root + param_list[1]
    page_type = param_list[2]
    print 'Param type = ' + page_type

    print 'URL List videos ' + url
    html = urllib2.urlopen(url).read()
    soup = bs(html, "html.parser")

    page_type_attrs = ''

    if page_type == '0':
        page_type_attrs = {'class': 'media-meta large poster large video'}

    elif page_type == '1':
        page_type_attrs = {'class': 'media-meta small media-meta'}

    elif page_type == '2':
        page_type_attrs = {'class': 'media-meta small'}

    soup_films = soup.find_all(
        'article',
        attrs=page_type_attrs)

    for soup_film in soup_films:
        title = soup_film.find('a').get_text().encode('utf-8')
        img = ''
        if soup_film.find('img').has_attr('data-attr'):
            img = soup_film.find('img')['data-attr'].encode('utf-8')
            img = re.compile(r'{"src":"(.*?)"}', re.DOTALL).findall(img)[0]
        elif soup_film.find('img')['src']:
            img = soup_film.find('img')['src'].encode('utf-8')
        url = soup_film.find('a')['href'].encode('utf-8')

        infoLabels = {
            "Title": title,
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
    html = urllib2.urlopen(url).read()
    soup = bs(html, "html.parser")

    soup_urls = soup.find(
        'form',
        attrs={'class': 'player-export'})['data-model'].encode('utf-8')
    soup_urls = soup_urls.replace('\\', '')

    urls = re.findall(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]' +
        '|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        soup_urls)
    print 'URLS_VIDEOS : ' + repr(urls)
    url_video = ''
    if len(urls) == 1:
        return urls[0]
    elif len(urls) > 1:
        if globalvar.ADDON.getSetting('allocineQuality') == 'sd':
            if 'sd' in urls[0]:
                return urls[0]
            else:
                return urls[1]

        elif globalvar.ADDON.getSetting('allocineQuality') == 'hd':
            if 'hd' in urls[0]:
                return urls[0]
            else:
                return urls[1]
    else:
        return ''



    # soup_pager = soup.find_all(
    #     'div',
    #     attr={'class': 'pager'})

    # if len(soup_pager) > 0:
    #     soup_pager_li = soup_pager.find('ul').find_all('li')
    #     current_page = ''
    #     last_page = li.get_text().encode('utf-8')

    #     for li in soup_pager_li:
    #         if li.has_attr('span'):
    #             current_page = li['span'].get_text().encode('utf-8')

    #     if current_page == '1':
    #         pass


