#!/usr/bin/env python
# coding: utf-8

# # URL Scraper Starter Kitt
# ## Structure of this Starter Kitt
# 
# 1. Source code (in Python) - library and application
# 2. Jupyter Notebook files (ipynb) including manuals inside
# 3. Example files - data with urls - url.txt
# 
# ### Data processing schema
# URL list in files -> URLScraper -> Websites in NoSQL collections for further processing
# 
# ### Prerequisites
# Create a file url.txt with the following structure (one row for one url):
# 
# http://stat.gov.pl
# 
# http://destatis.de
# 
# http://www.nsi.bg
# 
# Five steps to run this application.
# 
# 1. Import libraries
# 2. Create a connection to mongodb server
# 3. Set the database name
# 4. Set the file name of URLs to import
# 5. Start the web scraping

# # 1. Import libraries.
# If they do not exist please update your Python environment with pip, pip3, conda or easy_install. Look into manual.

# In[1]:


# import libraries
from pymongo import MongoClient
import requests
from datetime import datetime
import string, sys
import time


# # 2. Create a connection to mongodb server. 
# 
# Replace the values below with your own.
# 
# ### Variables to set:
# 
# servername - change with IP address or name of the server, e.g. 192.168.1.1 or serverdb.domain.com
# 
# port - change the port number - for MongoDB default is 27017

# In[2]:


host='localhost'
port=27017
# define the client connection
# host - default localhost
# port - default 27017
client=MongoClient('mongodb://'+str(host)+":"+str(port))


# # 3. Set the database name.
# 
# ### Variable to set:
# 
# dbname - if the database does not exist it will be created.

# In[3]:


dbname='wpc'
try:
    database=client[dbname]
except:
    print('Error connecting the database', sys.exc_info()[0])


# # 4. Set the file name of URLs to import. 
# 
# The file should be structured like this:
# 
# http://stat.gov.pl
# 
# http://destatis.de
# 
# http://www.nsi.bg
# 
# ### Variable to set:
# 
# filename - the name of the file, e.g. url.txt

# In[4]:


filename='url.txt'
file=open(filename,'r') 


# # 5. Start the web scraping.
# 
# ### Variables to set:
# 
# timeBetweenRequests - set the time between requests - in seconds (suggested 3-5 seconds).
# 
# collectionName - default database.websites - value after dot can be changed, e.g. database.myfirstcollection, database.wpc_20200301

# In[6]:


timeBetweenRequests=5
collectionName = database.websites
for url in file:
    print('Scrapping ',url.strip())
    website=requests.get(url.strip())    
    json = {
        'url': str(url.strip()),
        'content':  website.text,
        'date': str(datetime.now())
    }
    result = collectionName.insert_one(json)
    print('Scrapped ',url.strip())
    # N second delay on purpose
    time.sleep(timeBetweenRequests)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




