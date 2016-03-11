"""
Entropy.py
@brad_anton

Checks various components of a reduced HAR for entropy
"""
from scipy.stats import entropy

class Entropy:
    def __init__(self, data):
        self.data = data
    
    def string(self):
        pass

    def line(self):
        """Calculate entropy of a line of text
        """
        pass

if __name__ == '__main__':
    from json import load

    with open('/var/www/html/js/script.js', 'r') as file:
        for line in file:
            e = Entropy(line)
            e.line()
