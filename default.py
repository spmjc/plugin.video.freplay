# -*- coding: utf-8 -*-
import sys
import os
import os.path
import urllib
import urlparse

import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon

import resources.lib.globalvar as globalvar
import resources.lib.utils as utils
import resources.lib.channels.favourites as favourites
import resources.lib.commondownloader as commondownloader 
import resources.lib.log as log

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)


def add_Channel(idChannel, nameChannel, order):
    url = build_url({'mode': 'folder', 'channel': idChannel, 'param': 'none'})
    li = xbmcgui.ListItem(
        nameChannel,
        iconImage=os.path.join(globalvar.MEDIA, idChannel + ".png"))
    commands = []
    if order != 0:
        commands.append((
            globalvar.LANGUAGE(30101).encode('utf-8'),
            'XBMC.RunPlugin(%s?mode=up&channel=%s&param=none&name=none)' %
            (sys.argv[0], order)))
    if order != len(globalvar.ordered_channels) - 1:
        commands.append((
            globalvar.LANGUAGE(30102).encode('utf-8'),
            'XBMC.RunPlugin(%s?mode=down&channel=%s&param=none&name=none)' %
            (sys.argv[0], order)))
    commands.append((
        globalvar.LANGUAGE(30103).encode('utf-8'),
        'XBMC.RunPlugin(%s?mode=hide&channel=%s&param=none&name=none)' %
        (sys.argv[0], order)))
    if len(globalvar.hidden_channels) > 0:
        commands.append((
            globalvar.LANGUAGE(30104).encode('utf-8') + ' (%s)' %
            len(globalvar.hidden_channels),
            'XBMC.RunPlugin(%s?mode=unhide&channel=%s&param=none&name=none)' %
            (sys.argv[0], order)))
    li.addContextMenuItems(commands)

    xbmcplugin.addDirectoryItem(
        handle=addon_handle,
        url=url,
        listitem=li,
        isFolder=True)


def buildShowsList(videos):
    for chan, video_url, video_title, video_icon, infoLabels, video_mode in videos:
        li = xbmcgui.ListItem(
            video_title,
            iconImage=video_icon,
            thumbnailImage=video_icon,
            path=video_url)
        url = build_url({
            'mode': video_mode,
            'channel': chan,
            'param': video_url,
            'name': video_title})
        if video_mode == 'play':
            li.setInfo( type='Video', infoLabels=infoLabels)
            li.setProperty('IsPlayable', 'true')
            li.addContextMenuItems([(globalvar.LANGUAGE(33020).encode('utf-8'), 'XBMC.RunPlugin(%s?mode=dl&channel=%s&param=%s&name=%s)' % (sys.argv[0],chan,urllib.quote_plus(video_url),urllib.quote_plus(video_title)))])
            xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_NONE)
            xbmcplugin.setPluginCategory(addon_handle, 'episodes')
            xbmcplugin.setContent(addon_handle, 'episodes')
        xbmcplugin.addDirectoryItem(
            handle=addon_handle,
            url=url,
            listitem=li,
            isFolder=video_mode != 'play')
    if channel == 'favourites' and param == 'unseen':
        notify(globalvar.LANGUAGE(33026).encode('utf-8'), 0)


def notify(text, channel):
    time = 3000  # in miliseconds
    xbmc.executebuiltin(
        'Notification(%s, %s, %d, %s)' %
        ('FReplay', text, time, os.path.join(globalvar.ADDON_DIR, "icon.png")))


log.logEvent(args)
mode = args.get('mode', None)

utils.init()

if mode is None:
    for item in globalvar.ordered_channels:
        add_Channel(item[0], globalvar.channels[item[0]][0], item[1])
    xbmcplugin.endOfDirectory(addon_handle)

else:
    channel = args['channel'][0]
    param = args['param'][0]
    if mode[0] == 'folder':
        for chan, folder_param, folder_title, folder_icon, mode in globalvar.channels[channel][1].list_shows(channel, param):
            url = build_url({
                'mode': mode,
                'channel': chan,
                'param': folder_param,
                'name': folder_title})
            li = xbmcgui.ListItem(folder_title, iconImage=folder_icon)
            # Contextual Menu
            if mode == 'shows' and channel != 'favourites':
                li.addContextMenuItems([(globalvar.LANGUAGE(33021).encode('utf-8'), 'XBMC.RunPlugin(%s?mode=bkm&action=add&channel=%s&param=%s&display=%s)' % 
                                          (sys.argv[0],chan, urllib.quote_plus(folder_param), urllib.quote_plus(folder_title))),
                                          ])
            if mode == 'shows' and channel == 'favourites':
                li.addContextMenuItems([ (globalvar.LANGUAGE(33022).encode('utf-8'), 'XBMC.RunPlugin(%s?mode=bkm&action=rem&channel=%s&param=%s&display=%s)' % 
                                        (sys.argv[0],chan,urllib.quote_plus(folder_param),urllib.quote_plus(folder_title))),
                                        ])

            if mode == 'play':
                print 'play', folder_title
                li.setInfo(type='Video', infoLabels={"Title": folder_title})
                li.setProperty('IsPlayable', 'true')
                li.addContextMenuItems([(globalvar.LANGUAGE(33020).encode('utf-8'), 'XBMC.RunPlugin(%s?mode=dl&channel=%s&param=%s&name=%s)' % (sys.argv[0],chan,urllib.quote_plus(folder_param),urllib.quote_plus(folder_title)))])
            xbmcplugin.addDirectoryItem(
                handle=addon_handle,
                url=url,
                listitem=li,
                isFolder=mode != 'play')

    elif mode[0] == 'shows':
        buildShowsList(
            globalvar.channels[channel][1].list_videos(channel, param))

    elif mode[0] == 'play':
        url = globalvar.channels[channel][1].getVideoURL(channel, param)
        programName = args['name'][0]
        log.logGA(channel, param, programName)
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(addon_handle, True, item)

    elif mode[0] == 'Search':
        keyboard = xbmc.Keyboard('', globalvar.LANGUAGE(33023).encode('utf-8'))
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            buildShowsList(
                globalvar.channels[channel][1].list_videos(
                    channel, keyboard.getText()))

    elif mode[0] == 'bkm':
        if args['action'][0] == 'add':  # Add to Favourites
            display = args['display'][0]
            result = favourites.add_favourite(channel, param, display)
        else:
            result = favourites.rem_favourite(channel, param)
            xbmc.executebuiltin("XBMC.Container.Refresh")
        notify(result, channel)

    elif mode[0] == 'dl':
        if globalvar.dlfolder == '':
            notify(globalvar.LANGUAGE(33024).encode('utf-8'), channel)
        else:
            url = globalvar.channels[channel][1].getVideoURL(channel, param)
            extensionStart = url.rfind('.')
            extension = url[extensionStart:len(url)].upper()
            if extension == '.MP4':
                fileName = utils.format_filename(args['name'][0] + '.mp4')
                commondownloader.download(
                    url, os.path.join(globalvar.dlfolder, fileName))
            else:
                notify(
                    extension + globalvar.LANGUAGE(33025).encode('utf-8'),
                    channel)

    elif mode[0] == 'up':
        utils.move_up(int(channel))
        xbmc.executebuiltin("XBMC.Container.Refresh")
    elif mode[0] == 'down':
        utils.move_down(int(channel))
        xbmc.executebuiltin("XBMC.Container.Refresh")
    elif mode[0] == 'hide':
        utils.hide(int(channel))
        xbmc.executebuiltin("XBMC.Container.Refresh")
    elif mode[0] == 'unhide':
        dialog = xbmcgui.Dialog()
        ret = dialog.select(
            globalvar.LANGUAGE(30104).encode('utf-8'),
            globalvar.hidden_channels)
        if ret >= 0:
            utils.unhide(ret)
            xbmc.executebuiltin("XBMC.Container.Refresh")
    xbmcplugin.endOfDirectory(
        handle=int(addon_handle),
        succeeded=True,
        updateListing=False)
