"""
ParseHarEntry.py
@brad_anton

HTTP Archive (HAR) entry parser with reduces the set and adds 
in data.
"""
import json
import re 

from hashlib import sha512,sha256
from geoip import geolite2
from IPy import IP
from base64 import b64decode
#from os import getcwd
from tld import get_tld
from tld.exceptions import TldDomainNotFound
#from csv import reader

class ParseHarEntry:
    def __init__(self, entry, site_hash=None ):
        self.request = entry['request']
        self.response = entry['response']

        self.result = { 'url': None, 
                'url_sha512': None,
                'ip': None, 
                'vhost': None, 
                'tld': None, 
                'ip_country': None, 
                'content_sha512': None, 
                'content_sha256': None, 
                'content_type': None , 
                'content_encoding': None,
                'content': None,
                'in_alexa': False,
                'http_status': None,
                'redirect_url': None
                }

        self.result['url'] = self.request['url']
        self.result['url_sha512'] = sha512(self.result['url']).hexdigest()

        try:
            self.result['tld'] = get_tld(self.result['url'])
        except TldDomainNotFound:
            pass

        if 'serverIPAddress' in entry: 
            self.result['ip'] = entry['serverIPAddress']

        for header in self.request['headers']:
            if header['name'] == 'Host':
                self.result['vhost'] = header['value']

    def get_url(self):
        """Returns the URL for the entry"""
        return self.result['url']

    def get_content_hash(self):
        """Gets the hash of the content data, base64 decodes it if needed"""

        if ('text' in self.response['content']
                and self.response['content']['text'] != ""):
            content = self.response['content']['text']
            self.result['content'] = content.encode('utf-8')
        else:
            return 

        if 'mimeType' in self.response['content']:
            self.result['content_type'] = self.response['content']['mimeType']

        if 'encoding' in self.response['content']:
            self.result['content_encoding'] = self.response['content']['encoding']
            content = b64decode(content)

        try:
            """Rather then trying to detect MimeType, which is problematic,
            we just catch UnicodeEncodeError and then encode it as utf-8"""
            self.result['content_sha512'] = sha512(content).hexdigest()
            self.result['content_sha256'] = sha256(content).hexdigest()
        except UnicodeEncodeError: 
            self.result['content_sha512'] = sha512(content.encode('utf-8')).hexdigest()
            self.result['content_sha256'] = sha256(content.encode('utf-8')).hexdigest()

    def get_status(self):
        pass

    def get_country(self):
        if self.result['ip'] and IP(self.result['ip']).iptype() == 'PUBLIC':
            match = geolite2.lookup(self.result['ip'])
            if match:
                self.result['ip_country'] = match.country
    
    def process(self):
        self.get_content_hash()
        self.get_country()

    def get_results(self):
        return self.result

if __name__ == '__main__':
    with open('tests/parser_test.json', 'r') as f:
        har = json.load(f)

        for entry in har['log']['entries']:
            p = ParseHarEntry(entry)
            p.process()
            print p.get_results()
