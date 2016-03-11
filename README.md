# Site Parser
This is a proof-of-concept project which uses Selenium and BrowserMob Proxy to inspect websites for malicious JavaScript.

## Setup

First clone the project: 

```
git clone https://github.com/brad-anton/SiteParser.git
```

The set up a virutal environment

```
pip install virtualenv
cd SiteParser
virtualenv venv
source venv/bin/activate
```

Install dependancies (these need to be cleaned up)

```
pip install -r requirements.txt
```

### Java
You'll also need Java for Selenium and BrowserMob

## Using
To get started modify `site_parser.py` and set the `url` variable appropriately. Then run

```
python site_parser.py
```




