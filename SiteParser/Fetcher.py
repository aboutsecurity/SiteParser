"""
Fetcher.py
@brad_anton

Uses Selenium and BrowserMob to get all includes for a 
website. 

Selenium provides the framework for running the Browser and
BrowswerMob allows us to get all the includes and their content.

"""

from browsermobproxy import RemoteServer, Server
from selenium import webdriver
from os import getcwd

class Fetcher:
    def __init__(self):
        self.server = None
        self.proxy = None
        self.browser = None
        self.driver = None

    def set_remote_server(self, host, port):
        """Defines an already running proxy server for gathering
        includes and content
        """
        self.server = RemoteServer(host, port)
        self.proxy = self.server.create_proxy()

    def start_local_server(self, binpath=None):
        """Starts a local instance of BrowserMob.
        
        Keyword Arguments:
        binpath -- The full path, including the binary name to the 
        browsermob-proxy binary.
        """
        if binpath is None:
            binpath="{0}/browsermob-proxy-2.1.0-beta-4/bin/browsermob-proxy".format(getcwd())

        self.server = Server(binpath)
        self.server.start()
        self.proxy = self.server.create_proxy()

    def set_firefox(self):
        """Sets the Webdriver for Firefox"""
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_proxy(self.proxy.selenium_proxy())
        self.driver = webdriver.Firefox(firefox_profile=self.profile)

    def run(self, site, name='fetch'):
        """Runs an instance of the Fetcher. Requires that either
        set_remote_server() or start_local_server() has been previously  
        called.

        Keyword Arguments:
        site -- The URL of the site to load.
        name -- Name of the resulting HAR.
        """
        try:
            self.proxy.headers({'Via': None}) # TODO: Need to override BrowserMob to remove the Via Header - https://github.com/lightbody/browsermob-proxy/issues/213 
            self.proxy.new_har(name, options={ 'captureHeaders': True, 
                'captureContent': True, 
                'captureBinaryContent': True })
            self.driver.get(site)

            har = self.proxy.har
            har['dom'] = self.driver.page_source
            return har 
        except AttributeError:
            print "[!] FAILED: Ensure you have set a Webdriver"

    def close(self):
        try:
            self.proxy.stop() # The proxy won't need to be stopped if using remote_server()
        except AttributeError:
            pass

        try:
            self.driver.close()
        except AttributeError:
            print '[!] Driver not found'

if __name__ == '__main__':
    fetch = Fetcher()
    #fetch.set_remote_server('localhost',9090)
    fetch.start_local_server()
    fetch.set_firefox()
    har = fetch.run('http://trk.cp20.com/click?a59xn-1fxwbz-fhblgx2')

    fetch.close()

    from json import dumps
    print dumps(har, sort_keys=True, indent=4, separators=(',', ': '))
