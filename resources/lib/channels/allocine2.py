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

url_root = 'http://www.allocine.fr'


categories = [
    ('Cinéma', '/film', '1'),
    ('Séries', '/series', '1'),
    ('Émissions', '/video', '1'),
    ('News', '/news', '1')
]

# Construction du paramètre shows :
# 'root or sub or page | depth | cond (short_url) | root or add | long_url

# Construction du paramètre videos :
# long_url | page_type


subcategories = {
    '1': {
        '/film': [
            ('Bandes-annonces', '/video/bandes-annonces', '2', 'root'),  # Fait
            ('Meilleurs films', '/film/meilleurs', '2', 'root'),  # Non fait
            ('Films à l\'affiche', '/film/aucinema', '2', 'root'),  # Non fait
            ('Prochainement', '/film/attendus', '2', 'root'),  # Non fait
            ('Films pour enfants', '/film/enfants/aucinema', '2', 'root')  # Non fait
        ]
    },

    '2': {
        '/video/bandes-annonces': [
            ('Bandes-annonces', '/video/bandes-annonces', '3', 'root'),
            ('Extraits', '/video/extraits', '3', 'root'),
            ('Vidéos Bonus', '/video/bonus', '3', 'root')
        ],

        '/film/meilleurs': [
            ('Selon les spectateurs', '/film/meilleurs', '3', 'root'),
            ('Selon la presse', '/film/meilleurs/presse', '3', 'root'),
            ('Au box-office', '/film/meilleurs/boxoffice', '3', 'root'),
            ('Les pires films', '/film/meilleurs/dupire', '3', 'root')
        ]
    },

    '3': {
        '/video/bandes-annonces': [
            ('À ne pas manquer', '', '99', 'add', '0'),
            ('Les plus récentes', '/plus-recentes', '99', 'add', '0'),
            ('Binetôt au cinéma', '/prochainement', '99', 'add', '0')
        ],

        '/video/extraits': [
            ('Les plus consultés', '', '99', 'add', '1'),
            ('Date d\'ajout', '/date-ajout', '99', 'add', '1')
        ],

        '/video/bonus': [
            ('Les plus consultées', '', '99', 'add', '2'),
            ('Date d\'ajout', '/date-ajout', '99', 'add', '2')
        ],

        '/film/meilleurs|/film/meilleurs/presse': [
            ('Tous les genres', '/genre-13000', '4', 'add', 'root'),
            ('Action', '/genre-13025', '4', 'add', 'root'),
            ('Animation', '/genre-13026', '4', 'add', 'root'),
            ('Aventure', '/genre-13001', '4', 'add', 'root'),
            ('Comédie', '/genre-13005', '4', 'add', 'root'),
            ('Comédie dramatique', '/genre-13002', '4', 'add', 'root'),
            ('Documentaire', '/genre-13007', '4', 'add', 'root'),
            ('Drame', '/genre-13008', '4', 'add', 'root'),
            ('Fantastique', '/genre-13012', '4', 'add', 'root'),
            ('Policier', '/genre-13018', '4', 'add', 'root'),
            ('Romance', '/genre-13024', '4', 'add', 'root'),
            ('Thriller', '/genre-13023', '4', 'add', 'root')
        ]
    },

    '4': {
        '/genre': [
            ('Toutes les années', '/decennie-0000', '5', 'add', 'root'),
            ('2010 - 2019', '/decennie-2010', '5', 'add', 'root'),
            ('2000 - 2009', '/decennie-2000', '5', 'add', 'root'),
            ('1990 - 1999', '/decennie-1990', '5', 'add', 'root'),
            ('1980 - 1989', '/decennie-1980', '5', 'add', 'root')
        ]
    },

    '5': {
        '/decennie': [
            ('Tous les pays', '/pays-5000', '99', 'add', '3'),
            ('France', '/pays-5001', '99', 'add', '3'),
            ('U.S.A', '/pays-5002', '99', 'add', '3'),
            ('Allemagne', '/pays-5129', '99', 'add', '3'),
            ('Grande-Bretagne', '/pays-5004', '99', 'add', '3'),
            ('Italie', '/pays-5020', '99', 'add', '3')
        ]
    }

}

hdr = {
    # 'Referer': url_refer,
    # 'Upgrade-Insecure-Requests': '  1',
    # 'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0'
}

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

    if param == 'none':
        for category in categories:
            url_long = url_root + category[1]
            depth = category[2]
            cond = category[1]
            shows.append([
                channel,
                'sub|' + depth + '|' + cond + '|root' + '|' + url_long,
                category[0],
                '',
                'folder'])
    elif 'sub' in param:
        param_list = param.split('|')
        print repr(param_list)
        depth = param_list[1]
        cond = param_list[2]
        root_or_add = param_list[3]
        long_url = param_list[4]
        depth_dict = subcategories[depth]
        sub_categories = ''
        for key, value in depth_dict.iteritems():
            print 'COND : ' + cond + ' KEY : ' + key
            if cond in key or key in cond:
                sub_categories = depth_dict[key]
                break

        for sub_category in sub_categories:
            title = sub_category[0]
            cond = sub_category[1]
            next_type = 'sub'
            long_url = param_list[4]
            if sub_category[3] == 'root':
                long_url = url_root + cond
            else:  # add
                long_url = long_url + cond

            if sub_category[2] == '99':
                next_type = 'page'
                cond = sub_category[4]
            print 'LONG_URL ' + long_url
            shows.append([
                channel,
                next_type + '|' + sub_category[2] + '|' + cond + '|' + sub_category[3] + '|' + long_url,
                title,
                '',
                'folder'])

    elif 'page' in param:
        param_list = param.split('|')
        print 'PARAM_LIST PAGE : ' + repr(param_list)
        #depth = param_list[1]
        page_type = param_list[2]
        #root_or_add = param_list[3]
        url = param_list[4]
        url = debug_url(url)

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

                url_page = url + '/?page=' + current_page
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
    url = param_list[1]
    url = debug_url(url)
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

    if page_type == '0' or page_type == '1' or page_type == '2':
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

    elif page_type == '3':
        soup_films = soup.find_all(
            'div',
            attrs={'class': 'data_box'})
        for soup_film in soup_films:
            poster = soup_film.find('div', attrs={'class': 'poster'})
            title = poster.find('img')['title'].encode('utf-8')
            img = poster.find('img')['src'].encode('utf-8')
            url = soup_film.find('a', attrs={'class': 'btn-primary'})['href'].encode('utf-8')

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
    print 'URL_VIDEO : '+url
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





# sub_sub_categories = {
#     '/video/bandes-annonces': [
#         ('Bandes-annonces', '/video/bandes-annonces', '99'),
#         ('Extraits', '/video/extraits', '99'),
#         ('Vidéos Bonus', '/video/bonus', '99')
#     ],

#     '/film/meilleurs': [
#         ('Selon les spectateurs', '/film/meilleurs', '1'),
#         ('Selon la presse', '/film/meilleurs/presse', '1'),
#         ('Au box-office', '/film/meilleurs/boxoffice', '1'),
#         ('Les pires films', '/film/meilleurs/dupire', '1')
#     ]
# }




# sub_sub_sub_categories = {
#     '/video/bandes-annonces': [
#         ('À ne pas manquer', '/video/bandes-annonces', '0'),
#         ('Les plus récentes', '/video/bandes-annonces/plus-recentes', '0'),
#         ('Binetôt au cinéma', '/video/bandes-annonces/prochainement', '0')
#     ],

#     '/video/extraits': [
#         ('Les plus consultés', '/video/extraits', '1'),
#         ('Date d\'ajout', '/video/extraits/date-ajout', '1')
#     ],

#     '/video/bonus': [
#         ('Les plus consultées', '/video/bonus', '2'),
#         ('Date d\'ajout', '/video/bonus/date-ajout', '2')
#     ]

# }

