"""
Redirects.py
@brad_anton

We

"""

import re

from lxml.html import parse, tostring

class Redirects:
    def __init__(self, data):
        data.seek(0) 
        self.html = parse(data)

    def meta(self):
        for redirect_url in self.html.xpath('//meta[@http-equiv="refresh"]/@content'):
            match = re.search(r'URL=(.*)', redirect_url)
            if match:
                print "\t\t{0}".format(match.group(1))

if __name__ == '__main__':
    with open('/var/www/html/index.html', 'r') as file:
        n = Redirects(file)
        n.meta()

