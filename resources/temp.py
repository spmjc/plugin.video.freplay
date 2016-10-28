'''
Created on Oct 27, 2016

@author: greg
'''
import urllib, json
from bs4 import BeautifulSoup as Soup

url = "http://m.ina.fr/layout/set/ajax/listes/emissions?letter=b&classObject=ina_emission"
response = urllib.urlopen(url)
data = json.loads(response.read())
htmlcontent = data["content"]
print htmlcontent
soup = Soup(htmlcontent)
allDivs = soup.find_all("div", attrs={'class' : 'six columns alpha omega'})
print allDivs
#<div class="six columns alpha omega"><a href="/emissions/babar/"><img alt="Babar" height="77" src="/var/ogpv3/storage/images/accueil/menu-principal/emissions/babar/93219-1-fre-FR/babar_102x77.jpg" width="102"/></a></div>
for div in allDivs:
    print "link: " + div.select("a[href]")[0]["href"]
    imageTag = div.select("img")[0]
    print "image: " + imageTag["src"]
    print "titre: " + imageTag["alt"]
