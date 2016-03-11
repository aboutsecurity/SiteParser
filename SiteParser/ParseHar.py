"""
ParseHar.py
@brad_anton

Parses a HTTP archive (HAR) for bad things
"""
from ParseHarEntry import ParseHarEntry

import json
import gevent

from hashlib import sha512

class ParseHar: 
    def __init__(self, har):
        self.har = har
        self.entries = har['log']['entries']

        """Parent sites are hashed and stored which
        allows each HAR entry to maintain a relationship to where it was called
        """
        self.site_hash = sha512(self.entries[0]['request']['url'])
        self.parsed_entries = []
    
    def process_entry(self, entry):
        """Multi-threaded entry to speed up processing
        """
        p = ParseHarEntry(entry, self.site_hash)
        p.process()
        self.parsed_entries.append(p.get_results())

    def process(self):
        """Spawns an thread for each entry to process"""
        threads = []

        for entry in self.entries:
            #p = ParseHarEntry(entry, self.site_hash)
            #p.process()
            #self.parsed_entries.append(p.get_results())

            job = gevent.spawn(self.process_entry, entry)
            threads.append(job)
            gevent.joinall(threads)

    def get_results(self):
        return self.parsed_entries

if __name__ == '__main__':
    with open('tests/parser_test.json', 'r') as file:
        har = json.load(file)
        parsed = ParseHar(har)
        parsed.process()
        print parsed.get_results()

