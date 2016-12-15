# -*- coding: utf-8 -*-
import urllib2
import re
import CommonFunctions as common
from resources.lib import utils
from resources.lib import globalvar
from bs4 import BeautifulSoup as bs
from random import randint


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
            ('Au box-office', '/film/meilleurs/boxoffice', '99', 'root', '4'),
            ('Les pires films', '/film/meilleurs/dupire', '99', 'root', '3')
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

url_refer = 'http://www.allocine.fr'

user_agents = [
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
]


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

    #url_refer = 'http://www.allocine.fr'

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
        url_refer = 'http://www.allocine.fr/video/bandes-annonces/'
        print 'REFER : ' + url_refer
        ua = user_agents[randint(0, len(user_agents) - 1)]
        hdr = {
            #'Referer': url_refer,
            'DNT': '1',
            'Upgrade-Insecure-Requests': '  1',
            'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': user_agents
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
            last_page = soup_pager_li[len(soup_pager_li) - 1]
            if last_page.find('span'):
                last_page = last_page.find('span')
                last_page = current_page.get_text().encode('utf-8')
            elif last_page.find('a'):
                last_page = last_page.find('a').get_text().encode('utf-8')

            for k in range(0, int(last_page)):
                url_page = url + '/?page=' + str(k + 1)
                print 'URL : ' + url_page
                shows.append([
                    channel,
                    'shows|' + url_page + '|' + page_type,
                    'Page ' + str(k + 1),
                    '',
                    'shows'])

    return shows


def list_videos(channel, show_url):
    videos = []
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

            description = ''
            sortie = soup_film.find(
                'span',
                attrs={'itemprop': 'datePublished'}).get_text().encode('utf-8')
            description += 'Date de sortie : ' + sortie

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

    elif page_type == '3' or page_type == '4':
        added_films = []
        soup_films = soup.find_all(
            'div',
            attrs={'class': 'data_box'})
        for soup_film in soup_films:
            poster = soup_film.find('div', attrs={'class': 'poster'})
            title = poster.find('img')['title'].encode('utf-8')
            if title in added_films:
                continue
            else:
                added_films.append(title)
            img = poster.find('img')['src'].encode('utf-8')

            try:
                url = soup_film.find('a', attrs={'class': 'btn-primary'})['href'].encode('utf-8')
            except:
                url = ''

            description = ''

            if page_type == '4':
                box_office = soup_film.find(
                    'div',
                    attrs={'class': 'entries_inner'}).get_text().encode('utf-8')
                description += box_office

            try:
                sortie = soup_film.find(
                    'span',
                    attrs={'itemprop': 'datePublished'}).get_text().encode('utf-8')
                description += 'Date de sortie : ' + sortie
            except:
                pass

            lighten = soup_film.find_all(
                'span',
                attrs={'class': 'lighten'})

            tr_real = ''
            tr_acteur = ''
            for item in lighten:
                if 'Réalisateur' in item.get_text().encode('utf-8'):
                    tr_real = item.parent.parent
                elif 'Avec' in item.get_text().encode('utf-8'):
                    tr_acteur = item.parent.parent

            if tr_real:
                description += '\nRéalisateur(s) :'
                tr_real2 = tr_real.find('td').find_all(
                    'span')
                tr_real2.extend(tr_real.find('td').find_all(
                    'a'))
                for real in tr_real2:
                    description += ' ' + real.get_text().encode('utf-8') + ','
                description = description[:-1]

            if tr_acteur:
                description += '\nActeur(s) :'
                tr_acteur2 = tr_acteur.find('td').find_all(
                    'a')
                tr_acteur2.extend(tr_acteur.find('td').find_all(
                    'span'))
                for act in tr_acteur2:
                    description += ' ' + real.get_text().encode('utf-8') + ','
                description = description[:-1]

            description += '\nGenre : '
            genre = soup_film.find(
                'span',
                attrs={'itemprop': 'genre'}).get_text().encode('utf-8')
            description += genre

            stars = soup_film.find_all(
                'span',
                attrs={'class': 'stareval'})

            try:
                starts_press = stars[0].find(
                    'span',
                    attrs={'class': 'note'}).get_text().encode('utf-8')
                description += '\nNote presse : ' + starts_press + '/5'
            except:
                pass

            try:
                starts_spact = stars[1].find(
                    'span',
                    attrs={'class': 'note'}).get_text().encode('utf-8')
                description += '\nNote spectateurs : ' + starts_spact + '/5'
            except:
                pass

            try:
                syn = soup_film.find(
                    'p',
                    attrs={'class': 'margin_5t'}).get_text().encode('utf-8')

                description += '\n' + syn
            except:
                pass


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

