"""
ObfuscatedJs.py
@brad_anton

Determines if Javascript is Obfuscated

"""
from LineLength import LineLength
from SuspiciousMethods import SuspiciousMethods
from CharFrequency import CharFrequency

class ObfuscatedJs:
    def __init__(self, javascript):
        """
        Keyword Arguments:

        javascript -- file-like object (StringIO or file) for iterating over. 
        """
        javascript.seek(0)
        self.javascript = javascript.readlines()

    def find(self):
        l = LineLength(self.javascript)
        if l.suspicious():
            print "\t[+] Line Length Analysis Looks Suspicious!"
        else: 
            print "\t[+] Line Length Analysis Looks Clean!"

        s = SuspiciousMethods(self.javascript)
        r = s.find()
        print "\t[+] Suspicious Method Analysis:"

        for key, value in r.iteritems():
            print "\t\t{0}:{1}".format(key, value)

        c = CharFrequency(self.javascript)
        if c.is_suspicious():
            print "\t[+] Character Frequency Analysis Looks Suspicious"
        else:
            print "\t[+] Character Frequency Analysis Looks Clean"
