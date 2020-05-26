#!/usr/bin/env python
# coding: utf-8

# # Main library named SocialMediaPresenceCollector
# ## should be saved in separate file named SocialMediaPresenceCollector.py
# To use in your own application - please import this way:
# 
# import SocialMediaPresenceCollector as smpc
# 
# then start the application this way
# 
# smpsk=smpc.SocialMediaPresenceStarterKitt()
# 
# smpsk.start()

# In[ ]:


import requests
import re
import string
import csv
import sys
import json
import os
import os.path
from bs4 import BeautifulSoup 
from collections import OrderedDict
from datetime import datetime



# HTMLParserBS class is used to find all URLs that reference to Social Media
class HTMLParserBS:    
    output_list=[]
    # method extractURLs is to extract all URLs and return them as the urls[] list
    # it goes through the website to find all anchors <a href>
    def extractURLs(self,page):      
        # Capitalization makes a difference for links! So they shouldn't be lowered
        soup = BeautifulSoup(page.text,"html.parser")
        urls = []
        for a in soup.find_all('a', href=True):
            urls.append(a['href'])
        return urls
    # method extractsURLs is to extract all URLs that are not in anchors <a>
    # it uses regular expression that search for any http or https, even not included in anchors
    def extractAllHTTP(self,page):
        URLs=re.findall(r"https?://[\w\-.~/?:#\[\]@!$&'()*+,;=]+", page.text.lower())
        return URLs

# class SocialMediaDeep contains a function responsible to divide the links into:
# (1) internal (used for the second search and external)
# (2) external (not used for the second search of social media)
class SocialMediaDeep:
    website=""    
    # this method is responsible to do the second search on subpages
    # from internal links that are present on the main page of the website
    def goDeeperToFindSocialMedia(self,website,URLs):
        print("Preparing to scrape subpages...")
        for url in URLs:
            try:        
                if url:
                    # the difference between InternalURL_type2 and InternalURL_type1
                    # is that type2 includes the domain name of the website, e.g., http://stat.gov.pl/page2.html
                    # and type1 does not include the domain name, e.g., <a href="./links/page2.html" ...>
                    if website in url and 'javascript' not in url:
                        print("Scraping InternalURL_type2: %s" % url)
                        smp.searchSocialMediaLinks(url,'2')
                    elif url[0]=="/" or url[0:2]=="./" or "http" not in url:
                        if url[0]=="/":
                            print("Scraping InternalURL_type1: {0} {1} ".format(website,url))
                            smp.searchSocialMediaLinks(website+url,'2')
                        elif url[0]==".":
                            print("Scraping InternalURL_type1: {0} {1}".format(website,url.replace('./','/')))
                            smp.searchSocialMediaLinks(website+url.replace('./','/'),'2')
                        else:
                            print("Scraping InternalURL_type1: {0} {1} {2}".format(website,'/',url))
                            smp.searchSocialMediaLinks(website+'/'+url,'2')
                    else:
                        # all external URLs are those who have a domain name different than the main page
                        print("ExternalURL_type1: %s " % url)                    
                else:
                    print("URL was not found in the second search.")
            except:
                print("Exception occured during processing the following URL:"+url)

class FileAccess:
    def jsonListWrite(self,jsonList): 
        currentDate = re.sub('[- :.]', '', str(datetime.now()))
        try:
            with open("wp2_social_"+currentDate+".json", "w") as file:
                file.write(str(jsonList))
                file.close()
        except IOError:
            msg = ("Error writing JSON file.")     
            print(msg)
            return

# class SocialMediaPresence includes one function responsible for finding popular Social Media websites
class SocialMediaPresence:
    website=""
    def __init__(self, 
                 social_media_dict={
                                'Facebook': ['facebook.com'],
                                 'Twitter': ['twitter.com'],
                                 'Youtube': ["youtu.be", "youtube.com"],
                                 'LinkedIn': ["linkedin.com"],
                                 'Instagram': ["instagram.com"],
                                 'Xing':['xing.com'],
                                 'Pinterest': ['pinterest.com']} ):
        # social_media_dict specifies which social media links should be found
        self.social_media_dict = social_media_dict
    # this method finds all social media links on webpage
    def searchSocialMediaLinks(self,website,level='1'):
        if website != '':
            website='http://'+website.lower().strip().replace('http://','').replace('https://','')
        try:
            headers = {'user-agent': 'python-app/0.1 experimental for statistical purposes'}
            r = requests.get(website, headers=headers)            
        except:    
            print("Exception during scraping content of the webpage: "+website)
        else:
            print("The length of the scrapped content: %s characters" % str(len(r.text)))            
            rows=r.text.splitlines()
            # if facebook login button is present on the website - report this on the screen
            # not used now but maybe in the future it can enrich the ICT survey
            #for line in rows:
            #    if "facebookLoginButton" in line:
            #        print ("Facebook login found: %d" % line)
            p = HTMLParserBS()
            p.output_list=p.extractURLs(r)
            URLs=list(p.output_list)
            print("Number of links on website: %d" % len(URLs))
            # sets are used instead of lists to eliminate all duplicates automatically
            # sometimes inside the main page there are several links to Social Media, in this case all duplicates will be removed
            # but all Social Media links will be added to the final list
            # Dictionary to store links for specific social media platforms
            link_dict = {}
            link_dict['URL'] = [website]
            for social_media in self.social_media_dict:
                link_dict[social_media] = set([])
            none='';
            # this loops through through all specified social media domain names
            for url in URLs:
                if url:
                    for social_media in self.social_media_dict:
                        for domain in self.social_media_dict[social_media]:
                            if domain in url:
                                link_dict[social_media].add(url)
                                print(url)

           # Count the number of found links
            n_links = 0
            for social_media in self.social_media_dict:
                n_links += len(link_dict[social_media])

            if n_links==0:
                print('No social media links have been found.')
                none='1';
            else:
                print('Total number of unique social media links found:',
                      n_links)
            # if subpage does not have a social media URL - do not write this in the result file
            if not (none=='1' and level=='2'):            
                try:
                    # name of the file
                    filename='wp2_social.csv'
                    exists=1
                    if not os.path.isfile(filename):
                        exists=0
                    with open (filename,'a') as file:
                        if exists==0:
                            file.write(';'.join(link_dict) + "\n")
                        columnNames= list(link_dict.keys())                    
                        writer=csv.DictWriter(file,delimiter=';',dialect=csv.excel,fieldnames=columnNames)
                        writer.writerow({item: ' ,'.join(link_dict[item]) for item in link_dict})
                except IOError:
                    msg = ("Error writing CSV file.")     
                    print(msg)
                data = {}
                data['URL'] = website
                for social_media in self.social_media_dict:
                    if social_media in link_dict:
                        data[social_media] = list(link_dict[social_media])
                    else:
                        data[social_media] = []
            smd=SocialMediaDeep();
            # if no links have been found on the main page, go one level deeper
            if none=='1' and level=='1' and len(URLs)>1:
                smd.goDeeperToFindSocialMedia(website,URLs)
            return data


# In[ ]:


# class SocialMediaPresenceStarterKitt:
#     smp=SocialMediaPresence()
#     fa=FileAccess()        
#     jsonList=[]
#     def __init__(self):
#         self.smp=SocialMediaPresence()
#         self.fa=FileAccess()
#         self.jsonList=[]
#     def start(self):
#         try:
#             plik=open("url2.txt","r")
#         except IOError:
#             msg = ("Error reading URL file.\n\nPlease create a file named 'url.txt' in the current folder with the list of URLs you want to scrap.")
#             msg += ("\n\nThe file content should be like this (one URL per line):\nmaslankowski.pl\nhttp://www.stat.gov.pl")
#             print(msg)
#         else:
#             for url in plik:
#                 if url!="":
#                     website='http://'+url.lower().strip().replace('http://','').replace('https://','')
#                     print("Website currently being scrapped: "+website)
#                     self.smp.searchSocialMediaLinks(website,'1')
#                     print()
#             fa.jsonListWrite(jsonList)





