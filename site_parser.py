"""
Site Parser 
@brad_anton

"""
import json

from cStringIO import StringIO

from SiteParser.ObfuscatedJs import ObfuscatedJs
from SiteParser.Fetcher import Fetcher
from SiteParser.ParseHar import ParseHar
from SiteParser.Classify import Classify
from SiteParser.Redirects import Redirects

if __name__ == '__main__':
    url = 'http://trk.cp20.com/click?a59xn-1fxwbz-fhblgx2'
    fetch = Fetcher()
    fetch.start_local_server()
    fetch.set_firefox()
    har = fetch.run(url)

    fetch.close()

    parsed = ParseHar(har)
    parsed.process()

    reduced = parsed.get_results()

    print "Found URLs:"
    for e in reduced:
        print "\t{0}".format(e['url'])

    classify = Classify(reduced)
    inspect = classify.get_results()

    print "[+] Inspecting DOM First"
    #print har['dom']
    dom = StringIO(har['dom'].encode('utf-8'))
    o = ObfuscatedJs(dom)
    o.find()

    print "\t[+] Looking for Redirects"
    r = Redirects(dom)
    r.meta()

    if len(inspect) > 0:
        for entry in inspect:
            print "[+] Inspecting:"
            print "\t{0}".format(entry['url'])
            js = StringIO(entry['content'])
            o = ObfuscatedJs(js)
            o.find()
            print "\t[+] Looking for Redirects"
            r = Redirects(js)
            r.meta()

