"""
CharFrequency.py
@brad_anton

Calculates the deviation in the count of characters
"""

from collections import Counter
from string import ascii_uppercase, ascii_lowercase, ascii_letters

class CharFrequency:
    def __init__(self, data):
        self.data = data

    def all(self):
        """Counts the number of occurances of each character"""
        total = Counter(letter for line in self.data 
                        for letter in line)
        return total

    def ascii(self):
        """Counts the number of occurances of just ASCII characters by lowercasing everything"""
        total = Counter(letter.lower() for line in self.data 
                        for letter in line if letter.lower() in ascii_lowercase)
        return total

    def ascii_ul(self):
        """Counts the number of occurances of just ASCII characters, without smashing case"""
        total = Counter(letter for line in self.data 
                        for letter in line if letter in ascii_letters)
        return total

    def ascii_u(self):
        """Counts the number of occurances of just ASCII characters, without smashing case"""
        total = Counter(letter for line in self.data 
                        for letter in line if letter in ascii_uppercase)
        return total

    def ascii_l(self):
        """Counts the number of occurances of just ASCII characters, without smashing case"""
        total = Counter(letter for line in self.data 
                        for letter in line if letter in ascii_lowercase)
        return total

    def total_ascii(self):
        """Returns the total number of ascii characters"""
        t = self.ascii()
        return sum(t.values())

    def total_lower(self):
        """Returns the number of lowercase ASCII characters"""
        t = self.ascii_l()
        return sum(t.values())

    def total_upper(self):
        """Returns the number of uppercase ASCII characters"""
        t = self.ascii_u()
        return sum(t.values())

    def percentage_u(self):
        return 100 * float(self.total_upper())/float(self.total_ascii())

    def percentage_l(self):
        return 100 * float(self.total_lower())/float(self.total_ascii())

    def is_suspicious(self):
        """20 is a Arbitrary value that will need to be backed by
        actual research"""
        threshold = 20

        try: 
            p = self.percentage_u()
        except ZeroDivisionError:
            p = 0
        
        return p > threshold


if __name__ == '__main__':

    from os import getcwd

    test_file = '{0}/SiteParser/tests/testexp.txt'.format(getcwd())
    with open(test_file) as file:
        c = CharFrequency(file.readlines())
        if c.is_suspicious():
            print "Looks Suspicious!"
        else:
            print "Looks ok!"

    with open('/var/www/html/js/script.js') as file:
        c = CharFrequency(file.readlines())
        if c.is_suspicious():
            print "Looks Suspicious!"
        else:
            print "Looks ok!"
