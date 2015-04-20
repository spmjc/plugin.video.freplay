from HTMLParser import HTMLParser
import urllib2

class HomeParse(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for name,value in attrs:
            if name=='class' and value=='revivre-artiste':
                print 'hi'


def list_shows(channel,folder):
    shows=[]
    
    if folder=='none':
        shows.append( [channel,'toptrailer$$1', 'BA A ne pas manquer','','shows'] )
        
        parser = HomeParse()
        print urllib2.urlopen('http://live.mytaratata.com/artistes').read()
        parser.feed(urllib2.urlopen('http://live.mytaratata.com/artistes').read())
    return shows