# -*- coding: utf-8 -*-

from resources.lib import utils
import re
from bs4 import BeautifulSoup as bs


title = ['RTBF Auvio']
img = ['rtbf']
readyForUse = True

url_root = 'http://www.rtbf.be/auvio'

categories = {
    '/categorie/series?id=35': 'Séries',
    '/categorie/sport?id=9': 'Sport',
    '/categorie/divertissement?id=29': 'Divertissement',
    '/categorie/culture?id=18': 'Culture',
    '/categorie/films?id=36': 'Films',
    '/categorie/sport/football?id=11': 'Football',
    '/categorie/vie-quotidienne?id=44': 'Vie quotidienne',
    '/categorie/musique?id=23': 'Musique',
    '/categorie/info?id=1': 'Info',
    '/categorie/humour?id=40': 'Humour',
    '/categorie/documentaires?id=31': 'Documentaires',
    '/categorie/enfants?id=32': 'Enfants'
}


def list_shows(channel, param):
    shows = []
    if param == 'none':
        for url, title in categories.iteritems():
            url = url_root + url
            shows.append([
                channel,
                url + '|' + title,
                title,
                '',
                'folder'])

    else:
        url = param.split('|')[0]
        cat = param.split('|')[1]
        file_path = utils.download_catalog(
            url,
            cat + '.html',
            random_ua=True)
        html = open(file_path).read()
        page_soup = bs(html, "html.parser")
        articles = page_soup.find('section', class_='js-item-container')
        articles = articles.find_all('article')

        for article in articles:
            title_url = article.find(
                'h3').find('a')
            title = title_url['title'].encode('utf-8')
            url_pgm = title_url['href'].encode('utf-8')
            imgs = article.find('img')['data-srcset']
            imgs = re.compile(
                r'http://(.*?).jpg', re.DOTALL).findall(imgs)
            if len(imgs) == 0:
                img = ''
            else:
                img = imgs[len(imgs) - 1]
                img = 'http://' + img + '.jpg'

            shows.append([
                channel,
                url_pgm,
                title,
                img,
                'shows'])

    return shows


def list_videos(channel, show_url):
    videos = []
    html = utils.get_webcontent(show_url)
    page_soup = bs(html, "html.parser")
    page_soup = bs(html, "html.parser")
    articles = page_soup.find('section', class_='js-item-container')
    articles = articles.find_all('article')
    for article in articles:
        title_url = article.find(
            'h3').find('a')
        title = title_url['title'].encode('utf-8')
        url_pgm = title_url['href'].encode('utf-8')
        imgs = article.find('img')['data-srcset']
        imgs = re.compile(
            r'http://(.*?).jpg', re.DOTALL).findall(imgs)
        if len(imgs) == 0:
            img = ''
        else:
            img = imgs[len(imgs) - 1]
            img = 'http://' + img + '.jpg'
        duration_soup = article.find(
            'span',
            class_='www-media-duration').get_text().encode('utf-8')
        duration_soup = re.compile(
            r'(.*?)min(.*?)s', re.DOTALL).findall(duration_soup)[0]
        duration = int(duration_soup[0]) * 60 + int(duration_soup[1])
        time = article.find('time')['datetime'].encode('utf-8')
        time = time[:10]/60

        infoLabels = {
            "Title": title + '  ' + time,
            # "Plot": description,
            'Duration': duration,
            "Aired": time,
            "Year": time[-4:]
        }

        videos.append([
            channel,
            url_pgm,
            title,
            img,
            infoLabels,
            'play'])

    return videos


def getVideoURL(channel, url_video):
    video_id = url_video[-7:]
    url = 'http://www.rtbf.be/auvio/embed/media?id=' + video_id
    html = utils.get_webcontent(url)
    html = html.replace('\\', '')
    html = html.replace('&quot;', '"')
    videos = re.findall(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]' +
        '|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        html)

    for video in videos:
        if '.mp4' in video:
            return video
