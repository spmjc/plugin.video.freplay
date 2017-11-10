# -*- coding: utf-8 -*-
import re
from resources.lib import utils
from bs4 import BeautifulSoup as bs

title = ['Canal U']
img = ['canalu']
readyForUse = True

url_root = 'http://www.canal-u.tv'


def list_shows(channel, param):
    shows = []

    if param == 'none':
        filePath = utils.download_catalog(
            url_root + '/themes',
            channel + '.html')
        root_html = open(filePath).read()
        root_soup = bs(root_html, "html.parser")

        themes_soup = root_soup.find(
            'div',
            attrs={'class': 'fright'})
        themes_soup = themes_soup.find(
            'ul',
            attrs={'id': 'themes'})

        for theme in themes_soup.findAll('li'):
            name_theme = theme.find('a')['title'].encode('utf-8')
            url_theme = theme.find('a')['href'].encode('utf-8')
            img_theme = theme.find('img')['src'].encode('utf-8')
            depth = url_theme.count('/')

            shows.append([
                channel,
                url_theme + '|' + str(depth),
                name_theme,
                url_root + img_theme,
                'folder'])
    else:
        current_url = param.split('|')[0]
        current_url_depth = int(param.split('|')[1])
        file_path = utils.download_catalog(
            current_url,
            current_url + '.html')
        theme_html = open(file_path).read()
        theme_soup = bs(theme_html, "html.parser")

        categories = theme_soup.find(
            'ul',
            attrs={'id': 'racine'})

        categories = categories.find_all('a')

        for category in categories:
            url = category['href'].encode('utf-8')
            url_depth = url.count('/')
            if url_depth == current_url_depth + 1:
                if current_url in url:
                    title = category.find('span').get_text().encode('utf-8')
                    next_type = 'folder'
                    if category.find('span')['class'] == 'file':
                        next_type = 'shows'

                    shows.append([
                        channel,
                        url + '|' + str(url_depth),
                        title,
                        '',
                        next_type])

        shows.append([
            channel,
            current_url + '|none',
            'Dernières vidéos de cette cétégorie',
            '',
            'shows'])

    return shows


def list_videos(channel, param):
    videos = []
    url = param.split('|')[0]
    # print 'URL : ' + url
    file_path = utils.download_catalog(
        url,
        url + '.html')
    theme_html = open(file_path).read()
    theme_soup = bs(theme_html, "html.parser")

    videos_soup = theme_soup.find_all(
        'li',
        class_='fleft lasts-online-even')

    videos2_soup = theme_soup.find_all(
        'li',
        class_='fleft lasts-online-odd')

    for video in videos_soup:

        url = video.find('a')['href'].encode('utf-8')
        img = video.find('div', class_='visible')
        img = img.find('img')['src'].encode('utf-8')
        img = url_root + img
        title = video.find('h4').get_text().encode('utf-8')
        title = title.replace('\n', '').replace('\r', '')
        duration = 0

        infoLabels = {
            "Title": title,
            'Duration': duration}

        videos.append([
            channel,
            url,
            title,
            img,
            infoLabels,
            'play'])

    for video in videos2_soup:

        url = video.find('a')['href'].encode('utf-8')
        img = video.find('div', class_='visible')
        img = img.find('img')['src'].encode('utf-8')
        img = url_root + img
        title = video.find('h4').get_text().encode('utf-8')
        title = title.replace('\n', '').replace('\r', '')
        duration = 0

        infoLabels = {
            "Title": title,
            'Duration': duration}

        videos.append([
            channel,
            url,
            title,
            img,
            infoLabels,
            'play'])

    page_soup = theme_soup.find(
        'div',
        class_='pagination')
    if page_soup is not None:
        page_soup = page_soup.find_all('a')

        current_page = 0
        for page in page_soup:
            if page.has_attr('class'):
                if page['class'][0].encode('utf-8') == 'selected':
                    current_page = page.get_text().encode('utf-8')
                    current_page = int(current_page)

        if current_page < len(page_soup):
            next_url = page_soup[current_page]['href'].encode('utf-8')
            videos.append([
                channel,
                next_url,
                'Page suivante (page ' + str(current_page + 1) + ')',
                '',
                {},
                'shows'])

    return videos


def getVideoURL(channel, url):
    html = utils.get_webcontent(url).replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
    
    urls = re.compile(r'"file": "(.*?)"', re.DOTALL).findall(html)
    for url in urls:
      if '.hd.mp4' in url:
        url_video=url
        
    return url_video
