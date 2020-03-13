# import libraries
from pymongo import MongoClient
import requests
from datetime import datetime
import string, sys
import time
class URLScraper:
    # define the client connection
    client=MongoClient('mongodb://localhost:27017')
    database=client['wpc']
    # host - default localhost
    # port - default 27017
    # dbname - default wpc
    def __init__(self,dbname,host,port):
        try:
            self.client=MongoClient('mongodb://'+host+':'+str(port))
            # define the database
            database  = client[dbname]
        except:
            print('Error connecting the database', sys.exc_info()[0])
    # filename - a text file with URL in each line
    def scrap(self,filename):
        try:
            with open(filename,'r') as file:
                for url in file:
                    print('Scrapping ',url.strip())
                    website=requests.get(url.strip())
                    data = database.websites
                    json = {
                        'url': str(url.strip()),
                        'content': website.text,
                        'date': str(datetime.now())
                    }
                    result = data.insert_one(json)
                    print('Scrapped ',url.strip())
                    # 5 second delay on purpose
                    time.sleep(5)
        except:
            print('Error during accessing the file with input URLs', sys.exc_info()[0])   
