# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon

import os

ADDON_NAME = 'plugin.video.freplay'
ADDON = xbmcaddon.Addon(ADDON_NAME)
SETTINGS = ADDON
LANGUAGE = ADDON.getLocalizedString
ADDON_DIR = ADDON.getAddonInfo("path")
ADDON_DATA = xbmc.translatePath(ADDON.getAddonInfo('profile'))
VERSION = ADDON.getAddonInfo("version")
RESOURCES = os.path.join(ADDON_DIR, "resources")
CHANNELS_DIR = os.path.join(RESOURCES, "lib", "channels")
MEDIA = os.path.join(RESOURCES, "media")
ADDON_DATA = xbmc.translatePath(
    "special://profile/addon_data/%s/" % ADDON_NAME)
CACHE_DIR = os.path.join(ADDON_DATA, "catalog_cache")
FAVOURITES_FILE = os.path.join(ADDON_DATA, "favourites.json")

LOGLEVEL = 1  # From to 3
DEVMODE = True

VIEWID = '503'

LANG = 'fr'
QLTY = 'hd'

dirCheckList = (CACHE_DIR,)
channels = dict()
ordered_channels = []
hidden_channels = []
hidden_channelsName = []
