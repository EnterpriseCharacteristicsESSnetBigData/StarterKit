# -*- coding: utf-8 -*-
"""
Source code for the URLScraper

TODO: Identify URL synonyms. Right now, the same website is scraped more than once
because http/https addresses are counted as different urls, or because an 
internal link contains a slash in the end, so that even the landing page is scraped more 
than once. (http://mecklenburgische.de vs http://mecklenburgische.de/)
Plus, pages often get hashes appended to their URLs, which is still
just the same page (just different positions). However, if an exclamation mark
comes after the hash, it means that javascript content is loaded at that position
with new content. That kind of URLs should be scraped.
Also, websites with the ending index.html are usually just synonyms for the same
url without that ending


TODO: Implement logging.

TODO: Scrape javascript parts of websites.
"""

# import libraries
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time

class ScrapeDomain():
    ##################
    # init
    ##################
    def __init__(self, domain, index, lang_codes=[], max_pages=1,
                 accept_subdomains=False, protocol='https://'):
        self.protocol = protocol
        self.domain = domain.lower().strip().replace('http://','').replace('https://','').replace('www.','')
        self.domain_link = self.protocol+self.domain
        self.json = {'domain': self.domain,
                      'index': index,
                     'content': {}} # All scraped pages are embedded documents within content dict
        self.max_pages = max_pages
        self.link_set = {self.domain_link}
        self.num_pages = 0
        self.scraped = set()
        self.accept_subdomains = accept_subdomains
        self.lang_codes = lang_codes
        if self.lang_codes:
            lang_idents = []
            for language in self.lang_codes:
                lang_idents.append("\/{}\/".format(language))
                lang_idents.append("\/{}-{}\/".format(language, language))
                lang_idents.append("\?lang={}".format(language))
                lang_idents.append("/{}$".format(language))
            self.lang_patterns = re.compile('|'.join(lang_idents), re.IGNORECASE)

    
    ##################
    # Utility functions
    ##################
    # Exclude downloadable files, pictures, etc from being scraped
    # List taken from ARGUS by datawizard1337 (I added xls and xlsx)
    # https://github.com/datawizard1337/ARGUS --> language prioritising was also inspired by ARGUS
    filetypes = set(['mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif', 'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg',
            'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',
            '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv', 'm4a',
            'css', 'pdf', 'doc', 'exe', 'bin', 'rss', 'zip', 'rar', 'msu', 'flv', 'dmg', 'xls', 'xlsx',
            'mng?download=true', 'pct?download=true', 'bmp?download=true', 'gif?download=true', 'jpg?download=true', 'jpeg?download=true', 'png?download=true', 'pst?download=true', 'psp?download=true', 'tif?download=true', 'tiff?download=true', 'ai?download=true', 'drw?download=true', 'dxf?download=true', 'eps?download=true', 'ps?download=true', 'svg?download=true',
            'mp3?download=true', 'wma?download=true', 'ogg?download=true', 'wav?download=true', 'ra?download=true', 'aac?download=true', 'mid?download=true', 'au?download=true', 'aiff?download=true',
            '3gp?download=true', 'asf?download=true', 'asx?download=true', 'avi?download=true', 'mov?download=true', 'mp4?download=true', 'mpg?download=true', 'qt?download=true', 'rm?download=true', 'swf?download=true', 'wmv?download=true', 'm4a?download=true',
            'css?download=true', 'pdf?download=true', 'doc?download=true', 'exe?download=true', 'bin?download=true', 'rss?download=true', 'zip?download=true', 'rar?download=true', 'msu?download=true', 'flv?download=true', 'dmg?download=true'])
    filetypes_pattern = '|'.join(['\.'+filetype+'$' for filetype in filetypes])
    def det_prio(self):
        '''Determines which URL should be scraped next'''
        not_scraped = list(self.link_set.difference(self.scraped))
        if not self.lang_codes:
            link_stack = sorted(not_scraped, key=len)
        else:
            correct_lang = []
            other_lang = []
            for link in not_scraped:
                if re.search(self.lang_patterns, link):
                    correct_lang.append(link)
                else:
                    other_lang.append(link)
            # Sort urls that were not yet scraped by link length
            link_stack = sorted(correct_lang, key=len) + sorted(other_lang, key=len)
        self.to_scrape = link_stack[0]
    def extractLinks(self):
        '''Parse html code to find links.
        Calls get_internalURL to test whether the link should be scraped.'''
        soup = BeautifulSoup(self.website.text,"html.parser")
        for a in soup.find_all('a', href=True):
           url = self.get_internalURL(a['href'])
           if url:
               self.link_set.add(self.standardize_link(url))
    def get_internalURL(self, url):
        #ignore javascript, mailto and telephone links as well as unwanted file endings
        pattern = re.compile(''.join(["^mailto:|^tel:|^javascript:|",
                                      self.filetypes_pattern]), re.IGNORECASE)
        if url and not re.search(pattern, url):
            if self.domain in url:
                if self.accept_subdomains == False:
                    # Test whether link doesn't contain a subdomain
                    cleaned_url = url.lower().replace('http://','').replace('https://','').replace('www.','')
                    if cleaned_url.split('.')[0]==self.domain.split('.')[0]:
                        return url
                else:
                    return url
            elif url[0:2]=="./":
                return self.domain_link+url.replace('./','/')
            elif url[0]=="/":
                return self.domain_link+url
            elif "http" not in url:
                return self.domain_link+'/'+url
    def standardize_link(self, url):
        '''Standardize the url to exclude duplicates'''
        # Define protocol
        url = url.replace('http://','').replace('https://','').replace('www.','')
        url = self.protocol+url
        # URL endings
        # First removes standalone slashes at the end, then removes # urls
        url = re.sub('#[^!\/]*$', '', re.sub('\/$', '', url))
        # Removes index.html
        url = re.sub('\/index\.html?\/?$', '', url)
        return url

    ##################
    # Scraper
    ##################
    def url_scraping(self, user_agent, collectionName, timeOutConnect=10,
                     timeOutRead=15, timeBetweenRequests=2):
        '''Scrapes link'''
        self.det_prio()
        print('Scraping', self.to_scrape)
        headers = {'user-agent': user_agent}
        self.scraped.add(self.to_scrape)
        try:
            self.website=requests.get(self.to_scrape, headers=headers,
                                      timeout=(timeOutConnect,timeOutRead))
            self.num_pages += 1
            self.scraped.add(self.website.url) # Add scraped url to scraped set (in case of redirect)
            print('Success in scraping page no', self.num_pages, 'of Domain:', self.domain)
            self.json['content'].update({str(self.num_pages): {'url': self.website.url,
                                                          'page': self.website.text,
                                                          'date': str(datetime.now())}})
            # I use website.url to obtain the url that was actually scraped 
            # (different to original url in case of redirects)
            if self.num_pages < self.max_pages:
                self.extractLinks()
            if self.num_pages >= self.max_pages or not self.link_set.difference(self.scraped):
                # Save json to MongoDB when max_pages is reached or no links are left for scraping
                try:
                    result = collectionName.insert_one(self.json)
                    print('Saved scraped pages to database')
                except Exception as e:
                    print('Error while saving into database occurred')
                    print(f'Error message: {type(e)}: {e}')
                    
        except Exception as e:
            print('Error scraping', self.to_scrape)
            print(f'Error message: {type(e)}: {e}')
        finally:
            # Even if the current page produced an error, continue scraping if there are still page links left
            if self.link_set.difference(self.scraped) and self.num_pages<self.max_pages:
                # N second delay on purpose
                time.sleep(timeBetweenRequests)
                self.url_scraping(user_agent, timeOutConnect, timeOutRead, timeBetweenRequests)