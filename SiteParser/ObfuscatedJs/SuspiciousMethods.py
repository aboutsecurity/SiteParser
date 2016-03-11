"""

SuspiciousMethods.py
@brad_anton

Takes counts of the occurance of "Suspicious" Methods within JavaScript. These 
were originally from:
    https://www.blackhat.com/presentations/bh-usa-07/Feinstein_and_Peck/Whitepaper/bh-usa-07-feinstein_and_peck-WP.pdf

"""
import re

class SuspiciousMethods:
    def __init__(self, data):
        self.data = data
        self.patterns = { "document_write" : re.compile(r'document\.write'),
            "string_instance" : re.compile(r"newstring"),
            "eval" : re.compile(r"eval"),
            "location" : re.compile(r"location"),  
            "escape" : re.compile(r"escape"),
            "encode" : re.compile(r"encode"),
            "decode" : re.compile(r"decode"),
            "element_instance" : re.compile(r"newelement"),
            "object_instance" : re.compile(r"object_created") }

        self.results = {}
        for key in self.patterns.iterkeys():
            self.results[key] = 0 


    def find(self):
        for line in self.data:
            for key, regex in self.patterns.iteritems():
                if regex.search(line):
                    self.results[key] += 1
        return self.results

if __name__ == '__main__':
    with open('test.js', 'r') as file:
        n = SuspiciousMethods(file.readlines())
        print n.find()

