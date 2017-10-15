#-*- coding: utf-8 -*-
import urllib2
import CommonFunctions
common = CommonFunctions
from resources.lib import utils
import re
from HTMLParser import HTMLParser

title=['Gulli']
img=['gulli']
readyForUse=True
htmlParser = HTMLParser()

urlBase='http://replay.gulli.fr/'
urlVideo='http://replay.gulli.fr/jwplayer/embed/%s?v=2.7'

def list_shows(channel,folder):
  shows=[]

  if folder=='none':
    shows.append( [channel,'dessins-animes','Dessins Animes','','folder'] )
    shows.append( [channel,'emissions','Emissions','','folder'] )
    shows.append( [channel,'series','Series et films','','folder'] )
  else:
    d=dict()
    cpt=0
    cptStr='/'
    while cpt != -1:
        filePath=utils.downloadCatalog(urlBase + folder + cptStr,'gulli' + folder + str(cpt) +'.html',False,{})
        html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a')
        replays = common.parseDOM(html,"div",attrs={"class":"block_category clearfix"})
        for replay in replays :
          title = (htmlParser.unescape(common.parseDOM(replay,"span",attrs={"class":"title"}) [0])).encode("utf-8")
          if title not in d:
            img = 'http://' +  re.findall('src="http://(.*?)"',replay) [0]
            shows.append( [channel,folder + '$$' + title,title,img.encode("utf-8"),'shows'] )
            d[title]=title
        if len(replays) != 0:
            cpt=cpt+1
            cptStr='/'+str(cpt)
        else:
            cpt=-1
  return shows

def getVideoURL(channel,id):
    html=utils.get_webcontent(urlVideo % id)
    url= re.findall("file:\s?\"(.*\/"+id[3:len(id)]+"\/.*\.mp4)\"",html) [0]
    return url

def list_videos(channel,param):
  folder=param.split('$$')[0]
  category=param.split('$$')[1]

  videos=[]
  cpt=0
  cptStr=''
  while cpt != -1:
    filePath=utils.downloadCatalog(urlBase + folder + cptStr,'gulli' + folder + str(cpt) +'.html',False,{})
    html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace("\n", " ")

    uls = common.parseDOM(html,"ul",attrs={"class":"block_content clearfix"})
    for ul in uls:
        replays = common.parseDOM(ul,"li")
        for replay in replays :
          title = (common.parseDOM(replay,"span",attrs={"class":"title"}) [0]).encode("utf-8")
          if title == category:
            cpt=-1
            title=(htmlParser.unescape(common.parseDOM(replay,"span",attrs={"class":"episode_title"}) [0])).encode("utf-8")
            img = 'http://' + re.findall('src="http://(.*?)"',replay) [0]
            url= re.findall('href="(.*?)"',replay) [0]
            iStart=url.find('VOD')
            vodId= url[iStart:]
            infoLabels={ "Title": title}
            videos.append( [channel, vodId.encode("utf-8") , title , img,infoLabels,'play'] )
    if len(uls) != 0 and cpt != -1:
        cpt=cpt+1
        cptStr='/'+str(cpt)
    else:
        cpt=-1
  return videos
