"""
LineLength.py
@brad_anton

Plots the line lengths to determine if suspicious

"""

import numpy 
from jsbeautifier import beautify

from Utils import graph_lines, find_outliers

class LineLength:
    def __init__(self, data):
        self.data = data

    def count_chars(self):
        """Counts the number of characters in each line
        """
        counts = []
        for line in self.data:
            counts.append(len(line))

        return numpy.array(counts)

    def suspicious(self):
        suspicious = find_outliers(self.count_chars())
        if suspicious.size > 1:
            return True
        else:
            return False

if __name__ == '__main__':
    with open('/var/www/html/js/script.js', 'r') as file:
        n = LineLength(file.readlines())
        if n.suspicious():
            print "Looks suspicious"
        else:
            print "Looks ok"
