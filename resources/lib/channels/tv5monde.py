#-*- coding: utf-8 -*-
from xml.dom import minidom  
from resources.lib import utils           

title=['TV5 Monde']
img=['tv5monde']
readyForUse=False

def list_shows(channel,folder):
  shows=[]
  d=dict()
    
  dom = xml.dom.minidom.parseString(utils.get_webcontent('http://www.tv5monde.com/data/momac/getAllThemesShowsVideos-7.xml'))
  if folder=='none':
    themes=dom.getElementsByTagName("theme")
    for theme in themes:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
        
  return shows