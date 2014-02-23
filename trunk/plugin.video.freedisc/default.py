__scriptname__ = "Freedisc.pl"
__author__ = "Pillager"
__url__ = ""
__scriptid__ = "plugin.video.freedisc"
__credits__ = "detoyy"
__version__ = "0.0.1"

import urllib,urllib2,re
import xbmc,xbmcplugin,xbmcgui,sys
import cookielib

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'


def _get_keyboard(default="", heading="", hidden=False):
        """ shows a keyboard and returns a value """
        keyboard = xbmc.Keyboard(default, heading, hidden)
        keyboard.doModal()
        if (keyboard.isConfirmed()):
                return unicode(keyboard.getText(), "utf-8")
        return default


def CATEGORIES():
        INDEX('http://freedisc.pl/files,movies,0','')
        #INDEX2('http://freedisc.pl/files,movies,0')


def INDEX(url,query):
        addDir('Search','blabla',3,'')
        cj = cookielib.CookieJar()

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

        # Add our headers
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')]
        
        urllib2.install_opener(opener)

        data = 'ajaxPage=search&type=0&pageno=Movies&actualGenreName='+query  # nic bo nic nie ma do wyslania narazie

        # Build our Request object (dodanie do url ",data" makes it a POST)
        req = urllib2.Request(url,data)
      
        # Make the request and read the response
        resp = urllib2.urlopen(req)
        link = resp.read()
        #print contents
        #link = getHtml(url)
        #print link
        #regex = "' title='(.+?)'><b><u>"+query+"</u></b>"
        #matchname = re.compile(regex).findall(link)
                              
        matchurl = re.compile("<a class='link'   href='(.+?)'  title=").findall(link)
        #print str(matchurl)+'matchurl'
        matchthumb = re.compile("<img width='77' height='58' src='/(.+?)'></img>").findall(link)
        for url,thumb in zip( matchurl, matchthumb):
                #print url
                                           
                x,y,name = url.split(',')    
                url = 'http://freedisc.pl/' + url
                #print url
                uzytkownik,fileid,filename = url.split(',')
                fileid = fileid.replace('f-','')
                thumb = 'http://freedisc.pl/'+thumb
                thumb = 'http://freedisc.pl/photo/'+fileid+'/7/3'
                #addDownLink(name + ' ' , url,2, thumb,fileid)
                addDir(name,url,2,thumb)

def INDEX2(url):
        #print url+' index2url'  #http://freedisc.pl/rum,f-302357,cfnm-on-sofa.mp4  http://freedisc.pl/marcin,f-649061,donatan-cleo-my-slowianie.mp4?ref=deman
        ref = url+'?ref=deman'
        #print 'INDEX2 ref ' +ref
        getHtml(ref)
        #print data
        x,fileid,name = url.split(',')
        fileid = fileid.replace('f-','')
        thumb = 'http://freedisc.pl/photo/'+fileid+'/7/3'
        addDownLink(name,url,5,thumb,fileid)


def SEARCHVIDEOS(url):
        searchUrl = 'http://freedisc.pl/ajaxRequest.php'
        vq = _get_keyboard(heading="Enter the query")
        # if blank or the user cancelled the keyboard, return
        if (not vq): return False, 0
        # we need to set the title to our query
        title = urllib.quote_plus(vq)
        #searchUrl += title
        #print "Searching URL: " + searchUrl
        INDEX(searchUrl,title)


def getHtml(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        data = response.read()
        response.close()
        return data



def getParams():
        param = []
        paramstring = sys.argv[2]
        if len(paramstring) >= 2:
                params = sys.argv[2]
                cleanedparams = params.replace('?','')
                if (params[len(params)-1] == '/'):
                        params = params[0:len(params)-2]
                pairsofparams = cleanedparams.split('&')
                param = {}
                for i in range(len(pairsofparams)):
                        splitparams = {}
                        splitparams = pairsofparams[i].split('=')
                        if (len(splitparams)) == 2:
                                param[splitparams[0]] = splitparams[1]

        return param


def addDownLink(name,url,mode,iconimage,fileid):
        u = 'http://freedisc.pl/streaming/video.mp4?fileID='+fileid
        ok = True
        liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png",
                               thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name })
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                         url=u, listitem=liz, isFolder=False)
        return ok


def addDir(name,url,mode,iconimage):
        u = (sys.argv[0] +
             "?url=" + urllib.quote_plus(url) +
             "&mode=" + str(mode) +
             "&name=" + urllib.quote_plus(name))
        ok = True
        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png",
                               thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name })
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                         url=u, listitem=liz, isFolder=True)
        return ok


params = getParams()
url = None
name = None
mode = None

try:
        url = urllib.unquote_plus(params["url"])
except:
        pass
try:
        name = urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode = int(params["mode"])
except:
        pass

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)

if mode == None or url == None or len(url)<1:
        print ""
        CATEGORIES()

elif mode == 1:
        print "" + url
        INDEX(url)

elif mode == 3:
        print mode
        SEARCHVIDEOS(url)
elif mode == 2:
        print mode
        INDEX2(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
