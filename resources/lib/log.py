# -*- coding: utf-8 -*-
import xbmc
import sys
import os
import globalvar
import uuid
import urllib
import urllib2


def debugInfo():
    if globalvar.LOGLEVEL == 1:
        print 'OS=' + sys.platform
        print 'Build=' + xbmc.getInfoLabel("System.BuildVersion")
        print 'Internet' + xbmc.getInfoLabel("System.InternetState")

    if globalvar.LOGLEVEL <= 2:
        print ('Addon=' +
               globalvar.ADDON.getAddonInfo('name') +
               ' ' + globalvar.ADDON.getAddonInfo('version'))
        print 'Addon Path=' + globalvar.ADDON.getAddonInfo('path')


def logDLFile(url):
    debugInfo()
    print 'Download Catalog=' + url


def logError(args, error):
    debugInfo()
    xbmc.executebuiltin(
        'Notification(%s, %s, %d, %s)' % (
            'FReplay',
            str(error),
            3000,
            os.path.join(globalvar.ADDON_DIR, "icon.png")))
    print '-----------Error' + str(args) + str(error)


def logEvent(args):
    debugInfo()
    print str(args)


def logGA(channel, param, programName):
    url = 'http://www.google-analytics.com/collect'
    cid = str(uuid.uuid1())
    cid = cid[cid.rfind('-') + 1:]
    tid = 'UA-62709903-1'
    build = xbmc.getInfoLabel("System.BuildVersion")
    build = 'Kodi ' + build[:build.find(' ')]
    values = {'v': '1',
              'tid': tid,
              'cid': cid,
              't': 'pageview',
              'dl': 'c=%s&p=%s' % (channel, param),
              'dt': programName[:50],
              'ua': (build + '-' + globalvar.ADDON.getAddonInfo('name') +
                     ' ' + globalvar.ADDON.getAddonInfo('version'))}
    print 'Log', 'c=%s&p=%s' % (channel, param)
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
