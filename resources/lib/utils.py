# -*- coding: utf-8 -*-
import globalvar

import os
import imp
import time
import urllib
import urllib2
import string
import log
import logging


def getOrderChannel(chanName):
    if globalvar.ADDON.getSetting('disp' + chanName):
        return int(globalvar.ADDON.getSetting('disp' + chanName))
    else:
        print chanName
        return 20


def init():
    for subdir, dirs, files in os.walk(globalvar.CHANNELS_DIR):
        for file in files:
            filename, extension = os.path.splitext(file)
            extension = extension.upper()
            if extension == '.PY' and file != '__init__.py':
                f, filepath, description = imp.find_module(
                    filename, [globalvar.CHANNELS_DIR])
                try:
                    channelModule = imp.load_module(
                        filename, f, filepath, description)
                except Exception:
                    logging.exception(
                        "Error loading channel module " + filepath)

                if channelModule.readyForUse:
                    for i in range(0, len(channelModule.title)):
                        order = getOrderChannel(channelModule.img[i])
                        if order != 99:
                            globalvar.channels[channelModule.img[i]] = [channelModule.title[i], channelModule, order]
                            globalvar.ordered_channels.append((
                                channelModule.img[i],
                                order))
                        else:
                            globalvar.hidden_channels.append(
                                channelModule.title[i])
                            globalvar.hidden_channelsName.append(
                                channelModule.img[i])

    globalvar.ordered_channels.sort(key=lambda channel: channel[0])
    globalvar.ordered_channels.sort(key=lambda channel: channel[1])

    for i in range(len(globalvar.ordered_channels)):
        if globalvar.ordered_channels[i][1] != i:
            globalvar.ordered_channels[i] = (
                globalvar.ordered_channels[i][0],
                i)
            globalvar.ADDON.setSetting(
                'disp' + globalvar.ordered_channels[i][0],
                str(i))
    globalvar.dlfolder = globalvar.ADDON.getSetting('dlFolder')


def downloadCatalog(url, fileName, force, dicPost):
    bDLFile = True
    fileName = format_filename(fileName)
    iCtlgRefresh = int(globalvar.ADDON.getSetting('ctlgRefresh')) * 60
    if not os.path.exists(globalvar.CACHE_DIR):
        os.makedirs(globalvar.CACHE_DIR, mode=0777)
    filePath = os.path.join(globalvar.CACHE_DIR, fileName)
    if os.path.exists(filePath):
        mtime = os.stat(filePath).st_mtime
        bDLFile = (time.time() - mtime > iCtlgRefresh)
    else:
        bDLFile = True
    if bDLFile:
        if dicPost:
            data = urllib.urlencode(dicPost)
            print data
            urllib.urlretrieve(url, filePath, None, data)
        else:
            urllib.urlretrieve(url, filePath)
        log.logDLFile(url)
    return filePath


def format_filename(s):
    """Take a string and return a valid filename constructed from the string.
    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores.
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    return filename


def get_webcontent(url):
    req = urllib2.Request(url)
    req.add_header(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0.1')
    req.add_header('Referer', url)
    webcontent = urllib2.urlopen(req).read()
    return webcontent


def move_up(order):
    globalvar.ADDON.setSetting(
        'disp' + globalvar.ordered_channels[order][0],
        str(order - 1))
    globalvar.ADDON.setSetting(
        'disp' + globalvar.ordered_channels[order - 1][0],
        str(order))


def move_down(order):
    globalvar.ADDON.setSetting(
        'disp' + globalvar.ordered_channels[order][0],
        str(order + 1))
    globalvar.ADDON.setSetting(
        'disp' + globalvar.ordered_channels[order + 1][0],
        str(order))


def hide(order):
    globalvar.ADDON.setSetting(
        'disp' + globalvar.ordered_channels[order][0],
        '99')


def unhide(order):
    globalvar.ADDON.setSetting(
        'disp' + globalvar.hidden_channelsName[order],
        str(len(globalvar.ordered_channels)))
