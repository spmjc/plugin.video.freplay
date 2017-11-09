# -*- coding: utf-8 -*-
import json
import resources.lib.utils as utils
from resources.lib import globalvar

title = ['La 1ère', 'France 2', 'France 3', 'France 4', 'France 5', 'France Ô']
img = ['la_1ere', 'france2', 'france3', 'france4', 'france5', 'franceo']
readyForUse = True

channelCatalog = 'http://pluzz.webservices.francetelevisions.fr/' \
                 'pluzz/liste/type/replay/nb/10000/chaine/%s'

showInfo = 'http://webservices.francetelevisions.fr/tools/getInfosOeuvre/v2/' \
           '?idDiffusion=%s&catalogue=Pluzz'

imgURL = 'http://refonte.webservices.francetelevisions.fr%s'

categories = {"france2": "France 2",
              "france3": "France 3",
              "france4": "France 4",
              "france5": "France 5",
              "franceo": "France Ô",
              "guadeloupe": "Guadeloupe 1ère",
              "guyane": "Guyane 1ère",
              "martinique": "Martinique 1ère",
              "mayotte": "Mayotte 1ère",
              "nouvellecaledonie": "Nouvelle Calédonie 1ère",
              "polynesie": "Polynésie 1ère",
              "reunion": "Réunion 1ère",
              "saintpierreetmiquelon": "St-Pierre et Miquelon 1ère",
              "wallisetfutuna": "Wallis et Futuna 1ère",
              "sport": "Sport",
              "info": "Info",
              "documentaire": "Documentaire",
              "seriefiction": "Série & fiction",
              "magazine": "Magazine",
              "jeunesse": "Jeunesse",
              "divertissement": "Divertissement",
              "jeu": "Jeu",
              "culture": "Culture"}


def list_shows(channel, folder):
    shows = []
    uniqueItem = dict()

    realChannel = channel
    if channel == 'la_1ere':
        realChannel = 'la_1ere_reunion%2C' \
                      'la_1ere_guyane%2C' \
                      'la_1ere_polynesie%2C' \
                      'la_1ere_martinique%2C' \
                      'la_1ere_mayotte%2C' \
                      'la_1ere_nouvellecaledonie%2C' \
                      'la_1ere_guadeloupe%2C' \
                      'la_1ere_wallisetfutuna%2C' \
                      'la_1ere_saintpierreetmiquelon'

    url_json = channelCatalog % (realChannel)
    filePath = utils.downloadCatalog(url_json,
                                     '%s.json' % (channel),
                                     False,
                                     {})
    filPrgm = open(filePath).read()
    jsonParser = json.loads(filPrgm)
    emissions = jsonParser['reponse']['emissions']

    if folder == 'none':
        for emission in emissions:
            rubrique = emission['rubrique'].encode('utf-8')
            if rubrique not in uniqueItem:
                uniqueItem[rubrique] = rubrique
                shows.append([
                    channel,
                    rubrique,
                    change_to_nicer_name(rubrique),
                    '',
                    'folder'])

    else:
        for emission in emissions:
            rubrique = emission['rubrique'].encode('utf-8')
            if rubrique == folder:
                titre = emission['titre_programme'].encode('utf-8')
                if titre != '':
                    id = emission['id_programme'].encode('utf-8')
                    if id == '':
                        id = emission['id_emission'].encode('utf-8')
                    if id not in uniqueItem:
                        uniqueItem[id] = id
                        shows.append([
                            channel,
                            id,
                            titre,
                            imgURL % (emission['image_large']),
                            'shows'])
    return shows


def change_to_nicer_name(original_name):
    if original_name in categories:
        return categories[original_name]
    return original_name


def list_videos(channel, folder):
    videos = []
    filePath = utils.downloadCatalog(
        channelCatalog % (channel),
        '%s.json' % (channel),
        False,
        {})
    filPrgm = open(filePath).read()
    jsonParser = json.loads(filPrgm)
    emissions = jsonParser['reponse']['emissions']
    for emission in emissions:
        id = emission['id_programme'].encode('utf-8')
        if id == '':
            id = emission['id_emission'].encode('utf-8')
        if id == folder:
            titre = ''
            plot = ''
            duration = 0
            date = ''
            id_diffusion = emission['id_diffusion']
            if 'accroche' in emission:
                plot = emission['accroche'].encode('utf-8')
            if 'real_duration' in emission:
                duration = int(emission['real_duration'])
            if 'titre' in emission:
                titre = emission['titre'].encode('utf-8')
            if 'soustitre' in emission:
                titre += ' - ' + emission['soustitre'].encode('utf-8')
            if 'date_diffusion' in emission:
                year = emission['date_diffusion'][:4]            
                titre += ' - ' + emission['date_diffusion'][:10].encode('utf-8')
            if 'image_medium' in emission:
                image = imgURL % emission['image_medium']                              
            
            infoLabels = {
                "Title": titre,
                "Plot": plot,
                "Duration": duration,
                "Year": year}

            videos.append([
                channel,
                id_diffusion,
                titre,
                image,
                infoLabels,
                'play'])
    return videos


def getVideoURL(channel, id):
        filPrgm = utils.get_webcontent(showInfo % (id))
        jsonParser = json.loads(filPrgm)
        for video in jsonParser['videos']:
            if video['format'] == globalvar.ADDON.getSetting(
               '%sQuality' % (channel)):
                url = video['url']
        return url
