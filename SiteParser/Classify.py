"""
Classify.py
@brad_anton

Give a Reduced Dictionary from a HAR, attempt multiple routines 
to classify if a file is good or bad. 
"""

from os import getcwd
from csv import reader 
import re

class Classify:
    def __init__(self, reduced_har):
        self.reduced_har = self.filter_results(reduced_har)

    def filter_results(self, reduced_har):
        """Include only JavaScript, in the future, we probably want to 
        look at everything"""
        filtered = []
        for entry in reduced_har:
            entry = self.check_alexa(entry) # Set if TLD in Alexa Top Ten
            if entry['content_type']:
                is_javascript = re.search('javascript|html', entry['content_type'])
                if (is_javascript and
                        not self.is_minified(entry['url']) and
                        entry['in_alexa'] == False):
                    filtered.append(entry) # We only care about non-Alexa, non-minified Javascript 
        return filtered

    def check_alexa(self, entry, csv_path=None):
        """Checks to see if the site is in the Alexa Top 1000
        
        Keyword Arguments:
        reduced_har -- sites to check
        csv_path -- Path to the Alexa Top 1mil CSV file found here:
            http://s3.amazonaws.com/alexa-static/top-1m.csv.zip

        """
        if entry['tld'] is None:
            return entry
        
        exempted = [ 'maps.googleapis.com' ] # Special Case Exemptions

        if entry['tld'] in exempted:
            entry['in_alexa'] = True
            return entry

        if csv_path is None:
            csv_path = "{0}/SiteParser/utils/top-1m.csv".format(getcwd())


        # TODO: This is not efficient at all
        with open(csv_path, 'rb') as f:
            r = reader(f)
            for row in r:
                if row[1] == entry['tld']:
                    entry['in_alexa'] = True
        return entry
    
    def is_minified(self, url):
        """Determines if a file is a minified version. Right now we 
        just filter on files ending .min.js but in the furture we
        really need to hash known goods. If an attacker obfuscated then
        minifies, we'd miss it."""
        is_minified = re.search('\.min\.js', url)
        if is_minified:
            return True
        return False

    def get_results(self):
        return self.reduced_har

if __name__ == '__main__':
    from ParseHar import ParseHar
    from json import load

    test_json = '{0}/SiteParser/tests/parser_test.json'.format(getcwd())

    with open(test_json, 'r') as file:
        har = load(file)

        parsed = ParseHar(har)
        parsed.process()

        reduced = parsed.get_results()

        classify = Classify(reduced)
        for entry in classify.get_results():
            print entry['url']
