#-*- coding: utf-8 -*-
import re, json, time, threading
from string import ascii_lowercase
from resources.lib import utils 
from HTMLParser import HTMLParser
from operator import itemgetter

title       = ['INA']
img         = ['ina']
readyForUse = True

cats='{"categories":[{"id":"politique","sub":[{"id":"allocutions+et+discours"},{"id":"elections+et+scrutins"},{"id":"gouvernements"},{"id":"partis+politiques"},{"id":"politique+internationale"},{"id":"presidents+et+chefs+d+etats"}]},{"id":"art+et+culture","sub":[{"id":"architecture"},{"id":"arts+du+spectacle"},{"id":"beaux+arts"},{"id":"cinema"},{"id":"gastronomie"},{"id":"litterature"},{"id":"mode+et+design"},{"id":"musees+et+expositions"},{"id":"musique"}]},{"id":"sport","sub":[{"id":"athletisme"},{"id":"auto+moto"},{"id":"cyclisme"},{"id":"football"},{"id":"sports+d+hiver"},{"id":"tennis"},{"id":"voile"},{"id":"autres+sports"}]},{"id":"divertissement","sub":[{"id":"betisier"},{"id":"chansons"},{"id":"humour"},{"id":"showbiz+et+people"},{"id":"varietes"}]},{"id":"sciences+et+techniques","sub":[{"id":"espace"},{"id":"la+terre"},{"id":"la+vie"},{"id":"maths+physique+chimie"},{"id":"medecine+sante"},{"id":"nouvelles+technologies"},{"id":"sciences+humaines"}]},{"id":"histoire+et+conflits","sub":[{"id":"decolonisation"},{"id":"epoques"},{"id":"grandes+dates"},{"id":"guerre+froide"},{"id":"guerre+d+algerie"},{"id":"indochine+et+vietnam"},{"id":"proche+et+moyen+orient"},{"id":"revolutions+et+coups+d+etat"},{"id":"seconde+guerre+mondiale"},{"id":"autres+conflits"}]},{"id":"economie+et+societe","sub":[{"id":"education+et+enseignement"},{"id":"environnement+et+urbanisme"},{"id":"justice+et+faits+divers"},{"id":"religion"},{"id":"vie+economique"},{"id":"vie+sociale"}]},{"id":"medias","sub":[{"id":"entretiens"},{"id":"petites+phrases"},{"id":"premieres+televisions"},{"id":"presse"},{"id":"publicite"},{"id":"radio"},{"id":"television"}]},{"id":"publicite","sub":[{"id":"alimentation+boisson"},{"id":"automobile+transport"},{"id":"culture+loisirs"},{"id":"divers"},{"id":"finances+assurances"},{"id":"habillement+textile"},{"id":"hygiene+beaute+sante"},{"id":"immobilier+habitat"},{"id":"medias+editions"},{"id":"produits+d+entretien"},{"id":"societes+de+service"},{"id":"telecoms+informatique+audiovisuel"}]},{"id":"fictions+et+animations","sub":[{"id":"adaptations+litteraires"},{"id":"animation"},{"id":"fantastique+et+science+fiction"},{"id":"feuilletons+et+series"},{"id":"fictions+historiques"},{"id":"intrigues+policieres"},{"id":"telefilms+et+dramatiques"},{"id":"theatre"}]},{"id":"ardisson","sub":[{"id":"ardimat"},{"id":"autant+en+emporte+le+temps"},{"id":"bains+de+minuit"},{"id":"descente+de+police"},{"id":"double+jeu"},{"id":"le+bar+de+la+plage"},{"id":"lunettes+noires+pour+nuits+blanches"},{"id":"les+generiques"},{"id":"les+integrales"},{"id":"scoop+a+la+une"},{"id":"les+best+of"},{"id":"autres"},{"id":"tout+le+monde+en+parle"}]},{"id":"cannes","sub":[{"id":"1946+1959"},{"id":"1960+1977"},{"id":"1978+1996"},{"id":"1997+2010"},{"id":"en+marge"}]},{"id":"presidentielles","sub":[{"id":"duels+presidentiels"},{"id":"securite"},{"id":"ecologie"},{"id":"economie"},{"id":"education"},{"id":"emploi"},{"id":"europe"},{"id":"historique"},{"id":"les+candidats"},{"id":"phrases+cultes"},{"id":"retraite"},{"id":"spots+de+campagnes"}]},{"id":"memoires+partagees","sub":[{"id":"operation+languedoc+roussillon"},{"id":"operation+aquitaine"},{"id":"operation+lorraine"},{"id":"operation+tour+de+france"},{"id":"operation+martinique"},{"id":"operation+automobile"},{"id":"la+france+coloniale"},{"id":"loisirs"},{"id":"voyages+a+l+etranger"},{"id":"tourisme+en+france"},{"id":"grandes+villes+de+france"},{"id":"fetes+et+ceremonies"},{"id":"conflits+mondiaux"}]},{"id":"radio+filmee","sub":[{"id":"france+inter"},{"id":"france+info"},{"id":"france+culture"},{"id":"france+bleu"},{"id":"fip"},{"id":"le+mouv"}]}]}'''
def list_shows(channel,folder):
  shows=[]  
  jsonParser = json.loads(cats)
  
  if folder=='none':
    for c in jsonParser['categories']:
      shows.append( [channel,c['id'], utils.formatName(c['id'].replace('+',' ')) ,'' ,'folder'] )
  
  else:                                
    for c in jsonParser['categories']:
      if c['id']==folder:
        for s in c['sub']:
          shows.append( [channel,c['id'] + '|' + s['id'] +'|0', utils.formatName(s['id'].replace('+',' ')) ,'' ,'shows'] )

  return shows


def list_videos(channel,url):
  videos=[]
  cat,sub,id=url.split('|')  
  
  url='https://www.ina.fr/layout/set/ajax/recherche/result?q=tree%3A%28Top%2Fina%2Fogpv3%2Frubrique%2Faudiovideo%2F' + cat + '%2F' + sub + '%29&autopromote=0&c=ina_rubrique&b=' + id + '&type=Video&typeBlock=ina_resultat_exalead&r=Top%2Fina%2Fpremium%2Fnon'
  
  filePath=utils.downloadCatalog(url ,sub + '.html',False,{})
  html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\\n', ' ').replace('\r', '').replace('\\t', '').replace("\\","")
  
  if id!='0':
    videos.append( [channel,cat + '|' + sub + '|' + str(int(id)-24), '<<Page Precedente' ,'',{} ,'shows'] )
    
  match = re.compile(r'href="(.*?)"> <img src="(.*?)" alt="(.*?)">',re.DOTALL).findall(html)
  for url,img,title in match:
    title=title.encode('utf-8')
    infoLabels={ "Title": title}
    idVideo= url[7:url.find('/',7)]
    videos.append( [channel,idVideo, title.encode('utf-8') , img.encode('utf-8'),infoLabels,'play'] )
  videos.append( [channel,cat + '|' + sub + '|' + str(int(id)+24), 'Page Suivante>>' ,'',{} ,'shows'] )
  return videos
 
def getVideoURL(channel,idVideo):
  filePath=utils.downloadCatalog('https://player.ina.fr/notices/%s.mrss' % (idVideo),'ina%s.xml' % (idVideo),False,{}) 
  xml=open(filePath).read()
  
  
  url=re.findall('<media:content url="(.*?)"', xml)[0]
  return url 
  