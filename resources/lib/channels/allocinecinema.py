# -*- coding: utf-8 -*-
import urllib2
import re
from resources.lib import globalvar
from bs4 import BeautifulSoup as bs
from random import randint


title = ['Allocine Cinéma']
img = ['allocinecinema']
readyForUse = True

url_root = 'http://www.allocine.fr'

categories = [
    (
        'Bandes-annonces',
        '/video/bandes-annonces',
        'root',
        'sub_bandes_annonces',
        'page_type_none'
    ),  # Un truc a finir
    (
        'Meilleurs films',
        '/film/meilleurs',
        'root',
        'sub_meilleurs_films',
        'page_type_none'
    ),  # Fait
    (
        'Films à l\'affiche',
        '/film/aucinema',
        'root',
        'sub_films_affiche',
        'page_type_none'
    ),
    (
        'Prochainement',
        '/film/attendus',
        'root',
        'sub_prochainement',
        'page_type_none'
    ),
    (
        'Films pour enfants',
        '/film/enfants',
        'root',
        'ages',
        'page_type_3'
    ),
    (
        'Tous les films',
        '/films',
        'root',
        'sub_tous_les_films',
        'page_type_5'
    )
]

sub_categories = {
    # Bandes annonces ##########################################
    'sub_bandes_annonces': [
        (
            'Bandes-annonces',
            '/video/bandes-annonces',
            'root',
            'sub_bandes_annonces_2',
            'page_type_non'
        ),  # Fait
        (
            'Extraits',
            '/video/extraits',
            'root',
            'sub_extraits',
            'page_type_none'
        ),  # Fait
        (
            'Vidéos Bonus',
            '/video/bonus',
            'root',
            'sub_videos_bonus',
            'page_type_none'
        ),  # Fait
        (
            'Toutes les vidéos de films',
            '/video/films',
            'root',
            'types',
            'page_type_6'
        )  # A faire
    ],

    'sub_bandes_annonces_2': [
        (
            'À ne pas manquer',
            '',
            'add',
            'shows',
            'page_type_0'
        ),
        (
            'Les plus récentes',
            '/plus-recentes',
            'add',
            'shows',
            'page_type_0'
        ),
        (
            'Binetôt au cinéma',
            '/prochainement',
            'add',
            'shows',
            'page_type_0'
        )
    ],

    'sub_extraits': [
        (
            'Les plus consultés',
            '',
            'add',
            'shows',
            'page_type_1'),
        (
            'Date d\'ajout',
            '/date-ajout',
            'add',
            'shows',
            'page_type_1')
    ],

    'sub_videos_bonus': [
        (
            'Les plus consultées',
            '',
            'add',
            'shows',
            'page_type_2'
        ),
        (
            'Date d\'ajout',
            '/date-ajout',
            'add',
            'shows',
            'page_type_2'
        )
    ],

    # Meilleurs films ##########################################
    'sub_meilleurs_films': [
        (
            'Selon les spectateurs',
            '',
            'add',
            'genres',
            'page_type_3'
        ),
        (
            'Selon la presse',
            '/presse',
            'add',
            'genres',
            'page_type_3'
        ),
        (
            'Au box-office',
            '/boxoffice',
            'add',
            'shows',
            'page_type_4'
        ),
        (
            'Les pires films',
            '/dupire',
            'add',
            'shows',
            'page_type_3'
        )
    ],

    # Films à l'affiche ##########################################
    'sub_films_affiche': [
        (
            'Tous les films à l\'affiche',
            '',
            'add',
            'sub_films_affiche_2',
            'page_type_none'
        ),
        (
            'Meilleurs films à l\'affiche',
            '/top',
            'add',
            'shows',
            'page_type_5'
        ),
        (
            'Sorties de la semaine',
            '/film/sorties-semaine',
            'root',
            'shows',
            'page_type_5'
        ),
        (
            'Avant-premières',
            '/film/avantpremieres',
            'root',
            'shows',
            'page_type_3'
        )
    ],

    'sub_films_affiche_2': [
        (
            'Nombre de copies',
            '',
            'add',
            'shows',
            'page_type_5'
        ),
        (
            'Date de sortie',
            '/date-sortie',
            'add',
            'shows',
            'page_type_5'
        )
    ],

    # Prochainement ##########################################
    'sub_prochainement': [
        (
            'Films à venir les plus consultés',
            '',
            'add',
            'shows',
            'page_type_5'
        ),
        (
            'Calendrier des sorties',
            '/film/agenda',
            'root',
            'shows',
            'page_type_5'
        ),
        (
            'Sorties ciné US, Bientôt en France ?',
            '/film/agenda/usa/',
            'root',
            'sub_sorties_usa',
            'page_type_none'
        )
    ],

    'sub_sorties_usa': [
        (
            'Films déjà sortis aux USA',
            '',
            'add',
            'shows',
            'page_type_3'
        ),
        (
            'Films prochainement aux USA',
            '/bientot',
            'add',
            'shows',
            'page_type_3'
        )
    ],

    # Tous les films ##########################################
    'sub_tous_les_films': [
        (
            'Popularité',
            '',
            'add',
            'genres',
            'page_type_5'
        ),
        (
            'Notes spectateurs',
            '/notes',
            'add',
            'genres',
            'page_type_5'
        ),
        (
            'Notes presse',
            '/presse',
            'add',
            'genres',
            'page_type_5'
        ),
        (
            'Ordre alphabétique',
            '/alphabetique',
            'add',
            'genres',
            'page_type_5'
        )
    ],

    'sub_sorties_usa': [
        (
            'Films déjà sortis aux USA',
            '',
            'add',
            'shows',
            'page_type_3'
        ),
        (
            'Films prochainement aux USA',
            '/bientot',
            'add',
            'shows',
            'page_type_3'
        )
    ]
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
            next_categories = category[3]
            page_type = category[4]
            shows.append([
                channel,
                'sub|' + next_categories + '|' + url_long + '|' + page_type,
                title,
                '',
                'folder'])

    elif 'sub' in param:
        param_list = param.split('|')
        categories_name = param_list[1]
        if categories_name == 'other':
            categories_name = param_list[4]
        url_long = param_list[2]

        # Si on a un filtrage
        if categories_name == 'ages' \
                or categories_name == 'genres' \
                or categories_name == 'years' \
                or categories_name == 'genres_2' \
                or categories_name == 'types' \
                or categories_name == 'versions' \
                or categories_name == 'pays':
            # print 'FILTRAGE'
            key = ''
            next_filt = 'shows'
            if categories_name == 'ages':
                key = 'âge'
                next_filt = 'genres'

            elif categories_name == 'genres':
                key = 'genres'
                next_filt = 'years'

            elif categories_name == 'years':
                key = 'années'
                next_filt = 'pays'

            elif categories_name == 'pays':
                key = 'pays'
                next_filt = 'shows'

            elif categories_name == 'types':
                key = 'types'
                next_filt = 'genres_2'

            elif categories_name == 'genres_2':
                key = 'genres'
                next_filt = 'versions'

            elif categories_name == 'versions':
                key = 'versions'
                next_filt = 'shows'

            page_type = param_list[3]
            url = debug_url(url_long)
            req = urllib2.Request(url, headers=get_random_headers())
            html = urllib2.urlopen(req).read()
            soup = bs(html, "html.parser")

            soup_filtres = soup.find_all(
                'div',
                attrs={'class': 'left_col_menu_item'})

            if len(soup_filtres) == 0:
                soup_filtres = soup.find_all(
                    'div',
                    attrs={'class': 'filter-entity-section'})

            soup_args = ''
            for filtre in soup_filtres:
                if key in filtre.get_text().encode('utf-8'):
                    soup_args = filtre
                    break

            args = soup_args.find_all(['span', 'a'])
            if len(args) > 0:
                for arg in args:
                    title = arg.get_text().encode('utf-8')
                    if title.startswith('(') and title.endswith(')'):
                        continue
                    url = get_obfuscate_url(arg)
                    if not url:
                        url = url_long
                    else:
                        url = url_root + url

                    if key == 'show' or next_filt == 'shows':
                        next_param = url + '|' + page_type
                        next_func = 'shows'
                    else:
                        next_param = 'sub|other|' + url + '|' + page_type + \
                                     '|' + next_filt
                        next_func = 'folder'

                    shows.append([
                        channel,
                        next_param,
                        title,
                        '',
                        next_func])

        #  Sinon on a encore des catégories à parcourir
        else:
            # print 'ENCORE DES CATEGORIES A PARCOURIR'
            categories = sub_categories[categories_name]
            for category in categories:
                title = category[0]
                url_short = category[1]
                root_or_add = category[2]
                page_type = category[4]
                if root_or_add == 'root':
                    url = url_root + url_short
                else:
                    url = url_long + url_short

                next_categories = category[3]

                if next_categories == 'shows':
                    shows.append([
                        channel,
                        url + '|' + page_type,
                        title,
                        '',
                        'shows'])
                else:
                    shows.append([
                        channel,
                        'sub|' + next_categories + '|' + url + '|' + page_type,
                        title,
                        '',
                        'folder'])
    return shows


def list_videos(channel, show_url):
    videos = []
    param_list = show_url.split('|')
    page_url = param_list[0]
    page_url = debug_url(page_url)
    page_type = param_list[1]

    req = urllib2.Request(page_url, headers=get_random_headers())
    html = urllib2.urlopen(req).read()
    soup = bs(html, "html.parser")

    page_type_attrs = ''

    if page_type == 'page_type_0':
        page_type_attrs = {'class': 'media-meta large poster large video'}

    elif page_type == 'page_type_1':
        page_type_attrs = {'class': 'media-meta small media-meta'}

    elif page_type == 'page_type_2':
        page_type_attrs = {'class': 'media-meta small'}

    elif page_type == 'page_type_6':
        page_type_attrs = {'class': 'media-meta sidecontent small'}

    if page_type == 'page_type_0' \
       or page_type == 'page_type_1'\
       or page_type == 'page_type_6'\
       or page_type == 'page_type_2':

        soup_films = soup.find_all(
            'article',
            attrs=page_type_attrs)

        for soup_film in soup_films:
            try:
                title = soup_film.find('a').get_text().encode('utf-8')
            except:
                title = soup_film.find(
                    'h2', class_='title').get_text().encode('utf-8')
            title = title.replace('\n', '').replace('\r', '')
            img = ''
            if soup_film.find('img').has_attr('data-attr'):
                img = soup_film.find('img')['data-attr'].encode('utf-8')
                img = re.compile(r'{"src":"(.*?)"}', re.DOTALL).findall(img)[0]
            elif soup_film.find('img')['src']:
                img = soup_film.find('img')['src'].encode('utf-8')
            url_soup = soup_film.find('a')
            url = get_obfuscate_url(url_soup)

            description = ''
            try:
                sortie = soup_film.find(
                    'span',
                    attrs={'itemprop': 'datePublished'})
                sortie = sortie.get_text().encode('utf-8')
                description += 'Date de sortie : ' + sortie
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

    elif page_type == 'page_type_3' or page_type == 'page_type_4':
        added_films = []
        soup_films = soup.find_all(
            'div',
            attrs={'class': 'data_box'})
        for soup_film in soup_films:
            poster = soup_film.find('div', attrs={'class': 'poster'})
            title = poster.find('img')['title'].encode('utf-8')
            title = title.replace('\n', '').replace('\r', '')
            if title in added_films:
                continue
            else:
                added_films.append(title)
            img = poster.find('img')['src'].encode('utf-8')

            try:
                url_soup = soup_film.find('a', attrs={'class': 'btn-primary'})

            except:
                url_soup = soup_film.find(
                    'span',
                    attrs={'class': 'btn-primary'})
            url = get_obfuscate_url(url_soup)

            description = ''

            if page_type == 'page_type_4':
                box_office = soup_film.find(
                    'div',
                    attrs={'class': 'entries_inner'}
                ).get_text().encode('utf-8')
                description += box_office

            try:
                sortie = soup_film.find(
                    'span',
                    attrs={'itemprop': 'datePublished'}
                ).get_text().encode('utf-8')
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

    elif page_type == 'page_type_5':
        soup_films = soup.find_all(
            'div',
            attrs={'class': 'card card-entity card-entity-list cf hred'})
        for soup_film in soup_films:
            try:
                title = soup_film.find(
                    'a',
                    attrs={'class': 'meta-title-link'}
                ).get_text().encode('utf-8')
            except:
                title = soup_film.find(
                    'span',
                    attrs={'class': 'meta-title-link'}
                ).get_text().encode('utf-8')
            title = title.replace('\n', '').replace('\r', '')
            img = soup_film.find(
                'img',
                attrs={'class': 'thumbnail-img'})['data-src'].encode('utf-8')

            url_soup = soup_film.find(
                'a',
                attrs={'class': 'button button-primary'})
            if not url_soup:
                url_soup = soup_film.find(
                    'span',
                    class_='button-primary')

            url = get_obfuscate_url(url_soup)

            description = ''

            main_infos = soup_film.find(
                'div',
                attrs={'class': 'meta-body-info'}).get_text().encode('utf-8')
            main_infos = " ".join(main_infos.split())
            description += main_infos

            reals = soup_film.find(
                'div',
                attrs={'class': 'meta-body-direction'}
            ).get_text().encode('utf-8')
            reals = " ".join(reals.split())
            reals = '\n\n' + reals
            description += reals

            acteurs = soup_film.find(
                'div',
                attrs={'class': 'meta-body-actor'}).get_text().encode('utf-8')
            acteurs = " ".join(acteurs.split())

            acteurs = '\n\n' + acteurs
            description += acteurs

            synopsis = soup_film.find(
                'div',
                attrs={'class': 'synopsis'})
            if synopsis:
                synopsis = synopsis.get_text().encode('utf-8')
                synopsis = " ".join(synopsis.split())
                synopsis = '\n\n' + synopsis
                description += synopsis

            lighten = soup_film.find_all(
                'span',
                attrs={'class': 'lighten'})

            stars = soup_film.find_all(
                'div',
                attrs={'class': 'rating'})

            try:
                starts_press = stars[0].find(
                    'span',
                    attrs={'class': 'stareval-note'}
                ).get_text().encode('utf-8')
                description += '\n\nNote presse : ' + " ".join(starts_press.split()) + '/5'
            except:
                pass

            try:
                starts_spact = stars[1].find(
                    'span',
                    attrs={'class': 'stareval-note'}
                ).get_text().encode('utf-8')
                description += '\nNote spectateurs : ' + " ".join(starts_spact.split()) + '/5'
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

    last_page = 0
    current_page = 1
    soup_pager = soup.find(
        'div',
        attrs={'class': 'pager'})
    if soup_pager is not None and len(soup_pager) > 0:
        soup_pager_li = soup_pager.find('ul').find_all('li')
        last_page = soup_pager_li[len(soup_pager_li) - 1]
        if last_page.find('span'):
            last_page = last_page.find(
                'span').get_text().encode('utf-8')
        elif last_page.find('a'):
            last_page = last_page.find(
                'a').get_text().encode('utf-8')

        for page in soup_pager_li:
            if page.find('span') and not page.find('span').has_attr('class'):
                current_page = page.find(
                    'span').get_text().encode('utf-8')

        current_page = int(current_page)
        last_page = int(last_page)
    soup_pager = soup.find(
        'div',
        attrs={'class': 'pagination-item-holder'})
    if soup_pager is not None and len(soup_pager) > 0:
        soup_pager_a = soup_pager.find_all('a')
        if len(soup_pager_a) == 0:
            soup_pager_a = soup_pager.find_all('span')

        last_page = soup_pager_a[len(soup_pager_a) - 1]
        last_page = last_page.get_text().encode('utf-8')
        last_page = int(last_page)

        for page in soup_pager_a:
            if 'current-item' in page['class']:
                current_page = page.get_text().encode('utf-8')
                current_page = int(current_page)

    # print 'CURRENT_PAGE : ' + str(current_page)
    # print 'LAST-PAGE : ' + str(last_page)
    if current_page < last_page:
        if 'page' in page_url:
            next_url = page_url[:-1] + str(current_page + 1)
        else:
            next_url = page_url + '/?page=' + str(current_page + 1)
        title = 'Page suivante (page ' + str(current_page + 1) + ')'
        # print 'NEXT URL PAGE '+ next_url
        videos.append([
            channel,
            next_url + '|' + page_type,
            title,
            '',
            {},
            'shows'])

    return videos


def getVideoURL(channel, url_video):
    url = url_root + url_video
    # print 'URL_VIDEO : ' + url
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
    # print 'URLS_VIDEOS : ' + repr(urls)
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
