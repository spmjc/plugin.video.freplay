import xbmc
import sys
import globalvar

def logEvent(param):
    if globalvar.LOGLEVEL==1:
        print 'OS=' + sys.platform
        print 'Build=' + xbmc.getInfoLabel( "System.BuildVersion" )
        print 'Internet' + xbmc.getInfoLabel( "System.InternetState" )
    
    if globalvar.LOGLEVEL<=2:
        print 'Addon=' + globalvar.ADDON.getAddonInfo('name') + ' ' + globalvar.ADDON.getAddonInfo('version')
        print 'Addon Path=' + globalvar.ADDON.getAddonInfo('path')
        print param
