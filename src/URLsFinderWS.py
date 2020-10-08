# -*- coding: utf-8 -*-

"""
Source code for the OBEC Stater Kit URLs Finder Web Scraping class.
TODO: Load black list urls only once.
      Control requests.adapters.HTTPAdapter
"""

import pandas as pd
import glob
from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import time
from urllib.parse import unquote, urlparse
from tqdm import tqdm


# Class URLsFinderWS contains functions responsible for scraping 
# information about the Enterprises.
# These are the variables that this class uses:
# version - identification of the scraped files by date, id or other.
# start_path - directory where a csv file with Enterprises information
#              is located.
# scrape_path - directory where a csv files with scraped Enterprises
#               information are saved.
# log_path - directory where event logging information is saved.
# blacklist_path - directory where a csv file with blacklisted URLs
#                  is located.
# start_file - name of a csv file with Enterprises information.
# scrape_file - name of a csv file with scraped information from
#               websites.
# sapi_file - name of a csv file with scraped information from search
#             engine Duck Duck Go.
# to_scrape_file - name of a csv file with URLs from websites that will
#                  be scraped.
# log_file - name of a events log file.
# black_list_file - name of a csv file with blacklisted URLs.
# csv_delimiter - delimiter of the csv file, eg.: ";".
# csv_encoding - encoding of the csv file, eg.: "utf-8".
# csv_ext - files extension, eg.: ".csv".
# headers - HTTP request header information.
# slices - The number of portions to divide the information in files.
#          For all information use 0.
# obec_words_file - Words to be serched in the contents of the pages,
#              eg.: e-mail, address, phone, etc. in case of finding
#              urls or key words in case of OBEC.
#from datetime import datetime
#variables = {
#    'version': datetime.now().strftime('%Y-%m-%d'),
#    'version': 'v.2020.2',
#    'start_path': '.\\sbr_data\\',
#    'scrape_path': '.\\scrape_data\\',
#    'log_path': '.\\logs\\',
#    'black_list_path': '.\\black_list_urls\\',
#    'start_file': 'SBR_Data_ESSnet.csv',
#    'scrape_file': 'OBEC_Starter_Kit_Scrape_Data',
#    'sapi_file': 'OBEC_Starter_Kit_SAPI_Data',
#    'to_scrape_file': 'OBEC_Starter_Kit_to_Scrape_Data',
#    'log_file': 'OBEC_Starter_Kit_Log_Data.log',
#    'black_list_file': 'black_list_urls.csv',
#    'csv_delimiter': ';',
#    'csv_encoding': 'utf-8',
#    'csv_ext': '.csv',
#    'headers': {
#        'user-agent': 'ESSnet BigData WPC OBEC Starter Kit - \
#                       https://webgate.ec.europa.eu/fpfis/mwikis\
#                       /essnetbigdata/index.php/ESSnet_Big_Data\
#                      '.encode('utf-8'),
#        'Accept-Charset': 'utf-8',
#        'Accept-Encoding': 'identity',
#        'Accept': 'text/html'
#    },
#    'slices': 2,
#    'obec_words_file': 'URLs_words.txt' # 'OBEC_words_*.txt'
#}

class URLsFinderWS:

    def __init__(self, iterable=(), **kwargs):
        self.__dict__.update(iterable, **kwargs)
        print(" ".join('URLs Finder web scraping module is ready \
		      to work for vesion {0}'.format(self.version).split()))

			  
    # load_files method loads csv files

    def load_files(self, *args, **kwargs):
        if kwargs.get('file', None) == 'black_list':
            path = r'{0}{1}'.format(self.black_list_path,
                                     self.black_list_file,
                                     )
        elif kwargs.get('file', None) == 'obec_words_file':
            path = r'{0}{1}'.format(self.start_path,
                                     self.obec_words_file
                                     )
        else:
            path = r'{0}{1}'.format(self.start_path,
                                    self.start_file
                                    )
        all_files = glob.glob(path, recursive=True)
        li = []
        for fn in all_files:
            df = pd.read_csv(fn, delimiter=self.csv_delimiter, 
                             encoding=self.csv_encoding, dtype=str)
            df.replace(regex={r'\n': '', '\t': '', r'\s+': ' '},
                       inplace=True
                       )
            print(" ".join('Load file {0} \
                           with {1} rows \
                           and {2} coloumns'.format(fn,
                                                    df.shape[0],
                                                    df.shape[1]
                                                    ).split()
                           )
                 )
            li.append(df)
        df = pd.concat(li, axis=0, ignore_index=True, sort=False)
        df = df.fillna('').astype(str)
        df = df.applymap(
            lambda x: x.strip() if isinstance(x, str) else x)
        return df


    # start_ws method starts web scraping routines and uses the following
    # parameters:
    # print_errors - parameter whether to print errors or not 
    #                (optional, default False)
    # what - parameter to pass a routine for the method (mandatory,
    #        values: 'search', 
    #                'word_count',
    #                'find_urls_to_scrape_from_url',
    #                'find_urls_to_scrape_from_suggested_url',
    #                'find_enterprise_information')
    # search_engine - parameter with search engine api to query
    #        (optional, default 'https://html.duckduckgo.com/html/?q=')
    # sleep - parameter with number of seconds between each query
    #         request to the Search Engine (optional, default 1)
    # timeout - parameter with number of seconds for keep the request
    #           open (optional, default 5)
    # urlsatstart - parameter with number of URLs to be taken from the
    #               beginning of the web page code
    #               (optional, default 10)
    # urlsatend - parameter with number of URLs to be taken from the
    #             end of the web page code (optional, default 10)
    # url - parameter to indicate the column with the urls to scrape'
    #       (optional, default 'URL')
    # slice - parameter with number of portion of information to start
    #         scraping from again in case of interuption
    #         (optional, default 0)

    def start_ws(self, *args, **kwargs):
        print_errors = kwargs.get('print_errors', False)
        what = kwargs.get('what', '')
        search_engine = kwargs.get(
            'search_engine', 
            'https://html.duckduckgo.com/html/?q='
            )
        sleep = kwargs.get('sleep', 1)
        timeout = kwargs.get('timeout', 5)
        urlsatstart = kwargs.get('urlsatstart', 10)
        urlsatend = kwargs.get('urlsatend', 10)
        url = kwargs.get('url', 'URL')
        slice = kwargs.get('slice', 0)
        for x in range(slice, self.slices):
            print('Slice: {0}'.format(x))
            if what == 'word_count':
                frame = pd.read_csv(
                    r'{0}{1}_{2}_{3}{4}'.format(self.scrape_path,
                                                self.to_scrape_file,
                                                self.version,
                                                x,
                                                self.csv_ext), 
                    delimiter = self.csv_delimiter,
                    encoding = self.csv_encoding, 
                    dtype = str)
                print('DataFrame columns: {0}'.format(list(frame.columns)))
                dfnt = self.scrape_urls(frame,
                                        timeout=timeout,
                                        sleep=sleep,
                                        slice=x,
                                        what='word_count')
                self.save_errors(dfnt[1],
                                 who='word_count',
                                 print_errors=print_errors)
            elif what == 'search':
                frame = self.load_files()
                frame = frame.iloc[x::self.slices, :]
                print('DataFrame columns: {0}'.format(list(frame.columns)))
                dfnt = self.query_search_engine(frame,
                                                search_engine,
                                                timeout=timeout,
                                                sleep=sleep,
                                                slice=x)
                self.save_errors(dfnt[1],
                                 who=self.sapi_file,
                                 print_errors=print_errors)
            elif what == 'find_urls_to_scrape_from_url':
                frame = self.load_files()
                frame = frame.iloc[x::self.slices, :]
                print('DataFrame columns: {0}'.format(list(frame.columns)))
                dfnt = self.get_urls_to_scrape(frame,
                                               timeout=timeout,
                                               sleep=sleep,
                                               urlsatstart=urlsatstart,
                                               urlsatend=urlsatend,
                                               url=url,
                                               slice=x)
                self.save_errors(dfnt[1], 
                                 who='find_urls_to_scrape_from_url',
                                 print_errors=print_errors)
            elif what == 'find_urls_to_scrape_from_suggested_url':
                frame = self.load_files()
                frame = frame.iloc[x::self.slices, :]
                print('DataFrame columns: {0}'.format(list(frame.columns)))
                dfns = self.black_list_urls(self.load_files(file='black_list'),
                                            slice=x)			
                dfnt = self.get_urls_to_scrape(dfns,
                                               timeout=timeout,
                                               sleep=sleep,
                                               urlsatstart=urlsatstart,
                                               urlsatend=urlsatend,
                                               url=url,
                                               slice=x)
                self.save_errors(dfnt[1],
                                 who=self.to_scrape_file,
                                 print_errors=print_errors)
            elif what == 'find_enterprise_information':
                self.get_obec_words()
                frame = self.load_files()
                frame = frame.iloc[x::self.slices, :]
                print('DataFrame columns: {0}'.format(list(frame.columns)))
                dfnt = pd.read_csv(
                    r'{0}{1}_{2}_{3}{4}'.format(self.scrape_path,
                                                self.to_scrape_file,
                                                self.version,
                                                x,
                                                self.csv_ext),
                    delimiter=self.csv_delimiter,
                    encoding=self.csv_encoding,
                    dtype=str)
                dfnt = dfnt[
                    ~dfnt['Suggested URL'].str.contains(
                        '|'.join(self.load_files(file='black_list'))
                    )
                ]
                dfnt = self.scrape_urls(dfnt,
                                        timeout=timeout,
                                        sleep=sleep,
                                        slice=x,
                                        what='find_enterprise_information',
                                        dflook=frame)
                self.save_errors(dfnt[1], 
                                 who=self.scrape_file, 
                                 print_errors=print_errors)
            else:
                self.save_errors(dfnt[1], who='', print_errors=print_errors)
        return dfnt

		
    def save_errors(self, dfnt, *args, **kwargs):
        print_errors = kwargs.get('print_errors', False)
        who	= kwargs.get('who', '')
        if who:
            if len(dfnt) != 0:
                dfnt.to_csv(
                    r'{0}{1}_{2}_{3}{4}'.format(self.log_path, 
                                                who, 
                                                'errors', 
                                                self.version, 
                                                self.csv_ext),
                    mode = 'a',					
                    sep = self.csv_delimiter, 
                    encoding = self.csv_encoding, 
                    index = None, 
                    header=True)
            if print_errors:			
                print('Errors:\n{0}\n'.format(dfnt[1]))
        else:
            print('The method needs routine. Use key word \'search\', \
                  \'find_urls_to_scrape_from_suggested_url\', \
                  \'find_enterprise_information\', \
                  \'find_urls_to_scrape_from_url\' or \'word_count\' \
                  like that what=\'<key word>\'')


    def black_list_urls(self, black_listurls, *args, **kwargs):
        slice = kwargs.get('slice', 0)
        dfns = pd.read_csv(
            r'{0}{1}_{2}_{3}{4}'.format(self.scrape_path, 
                                        self.sapi_file, 
                                        self.version, 
                                        slice, 
                                        self.csv_ext), 
            delimiter = self.csv_delimiter, 
            encoding = self.csv_encoding, 
            dtype = str)
        dfns = dfns[
            ~dfns['Suggested URL'].str.contains(
                '|'.join(black_listurls['Black list URLs'].unique().tolist())
            )
        ]
        dfns['Suggested URL'] = dfns['Suggested URL'].apply(
            lambda x:unquote(x)
        )
        dfns['Has Simple Suggested URL'] = dfns['Suggested URL'].apply(
            lambda x: 1 \
            if urlparse(x).path in ['','/','/en','/en/'] \
                and urlparse(x).query=='' \
                and urlparse(x).fragment=='' \
            else 0
        )
        return dfns
		

    def query_search_engine(self, df, search_engine, *args, **kwargs):
        sleep = kwargs.get('sleep', 6)
        timeout = kwargs.get('timeout', 3)
        slice = kwargs.get('slice', 0)
        dfn = pd.DataFrame()
        dfe = pd.DataFrame()
        with tqdm(total=len(list(df.iterrows()))) as pbar:
            for index, row in df.iterrows():
                pbar.set_description(
                    'processed: %s %s ' % (
                        row['ID'], 
                        row['Name']
                        )
                    )
                pbar.update(1)
                search_string = re.sub(
                    '\s',
                    '+', 
                    re.sub(
                        '\s+', 
                        ' ', 
                        re.sub(
                            '\r', 
                            ' ', 
                            re.sub(
                                '\n', 
                                ' ', 
                                row['Name']
                                )
                            ).strip()
                        )
                    )
                url = '{0}{1}'.format(search_engine, search_string)
                s = requests.Session()
                a = requests.adapters.HTTPAdapter(
                                pool_connections=100, 
                                pool_maxsize=100, 
                                max_retries=20, 
                                pool_block=False)
                s.mount('https://', a)
                s.mount('http://', a)
                try:
#                    page = requests.get(
                    page = s.get(
                        url, 
                        headers=self.headers, 
                        timeout=timeout
                        )
                except requests.ConnectionError:
                    dfe = self.df_append(df, row, dfe, 'Connection problems')
                except requests.HTTPError:
                    dfe = self.df_append(df, row, dfe, 'HTTP error')
                except requests.Timeout:
                    dfe = self.df_append(df, row, dfe, 'Timeout occurred')
                except requests.TooManyRedirects:
                    dfe = self.df_append(df, row, dfe, 'Too many redirects')
                except requests.RequestException:
                    dfe = self.df_append(df, row, dfe, 'Request exception')
                except:
                    dfe = self.df_append(dfns, row, dfe, 'General exception')				
                else:
                    if page.status_code == 200:
                        getmax = 10
                        i = 0
                        try:
                            bs = BeautifulSoup(page.content,'lxml')
                        except:
                            dfe = self.df_append(
                                df, row, dfe, 
                                'Read page content with BeautifulSoup')
                        else:
                            topurls = bs.findAll('a',
                                                 {'class': ['result__a']})
                            for topurl in topurls:
                                geturl = re.search('uddg=(.+)', 
                                                   topurl.get('href'))
                                vURL = 0
                                try:
                                    u1 = urlparse(
                                            unquote(geturl.group(1)))
                                    u2 = urlparse(row['URL'])
                                except:
                                    dfe = self.df_append(
                                            df, row, dfe, 'URL parse')
                                else:
                                    if (unquote(geturl.group(1))[-4:].lower()
                                        not in [
                                            '.exe', 
                                            '.pdf', 
                                            '.xml', 
                                            '.jpg', 
                                            '.png', 
                                            '.gif', 
                                            '.zip', 
                                            '.rar', 
                                            '.mp4',
                                            'webm',											
                                            '.ogg',											
                                            '.avi', 
                                            '.doc', 
                                            'docx'
                                            ]
                                        and geturl 
                                        and i < getmax 
                                    ):
                                        if u1.netloc == u2.netloc:
                                            vURL = 1
                                        dfn=dfn.append(
                                            {
                                                'ID': row['ID'],
                                                'Name': row['Name'],
                                                'URL': row['URL'],
                                                'Suggested URL': (
                                                    unquote(geturl.group(1))),
                                                'Link position': i,
                                                'Has equal domain': vURL
                                            }, 
                                            ignore_index=True
                                        )
                                i = i + 1
                finally:
                    time.sleep(sleep)
        if len(dfe) != 0:
            dfe = dfe[list(df.columns)+['Error']]
        dfn = dfn[['ID', 'Name', 'URL', 'Suggested URL', 
                   'Link position', 'Has equal domain']]
        dfn.to_csv(
            r'{0}{1}_{2}_{3}{4}'.format(self.scrape_path, 
                                        self.sapi_file, 
                                        self.version, 
                                        slice, 
                                        self.csv_ext), 
            sep=self.csv_delimiter, 
            encoding = self.csv_encoding, 
            index = None, 
            header=True)
        return [dfn, dfe]

		
    def get_urls_to_scrape(self, dfns, *args, **kwargs):
        sleep = kwargs.get('sleep', 1)
        timeout = kwargs.get('timeout', 5)
        urlsatstart = kwargs.get('urlsatstart', 10)
        urlsatend = kwargs.get('urlsatend', 10)
        url = kwargs.get('url', 'URL')
        slice = kwargs.get('slice', 0)
        dfne = pd.DataFrame()
        dfe = pd.DataFrame()
        with tqdm(total = len(list(dfns.iterrows()))) as pbar:
            for index, row in dfns.iterrows():
                pbar.set_description(
                    'processed: %s %s ' % (row['ID'], 
                                           row[url])
                    )
                pbar.update(1)
                s = requests.Session()
                a = requests.adapters.HTTPAdapter(
                                pool_connections=100, 
                                pool_maxsize=100, 
                                max_retries=20, 
                                pool_block=False)
                s.mount('https://', a)
                s.mount('http://', a)
                try:
#                    page = requests.get(row[url].encode("utf-8"), 
                    page = s.get(row[url].encode("utf-8"), 
                                        headers=self.headers, 
                                        timeout=timeout, 
                                        verify=True)
                except requests.ConnectionError:
                    dfe = self.df_append(dfns, row, dfe, 
                                         'Connection problems')
                except requests.HTTPError:
                    dfe = self.df_append(dfns, row, dfe, 
                                         'HTTP error')
                except requests.Timeout:
                    dfe = self.df_append(dfns, row, dfe, 
                                         'Timeout occurred')
                except requests.TooManyRedirects:
                    dfe = self.df_append(dfns, row, dfe, 
                                         'Too many redirects')
                except requests.RequestException:
                    dfe = self.df_append(dfns, row, dfe, 'Request exception')
                except requests.SSLError:
                    dfe = self.df_append(dfns, row, dfe, 
                                         'Certificate verification error')
                except:
                    dfe = self.df_append(dfns, row, dfe, 'General exception')
                else:
                    if page.status_code == 200:
                        try:
                            bs = BeautifulSoup(page.content, 'lxml')
                        except:
                            dfe = self.df_append(
                                dfns, row, dfe, 
                                'Read page content with BeautifulSoup')
                        else:
                            topurls = bs.findAll('a')
                            dft = self.add_url(topurls, dfns, row, dfe, 
                                               urlsatstart, dfne, url)
                            dfne = dft[0]
                            dfe = dft[1]
                            dft = self.add_url(reversed(topurls), dfns, 
                                               row, dfe, urlsatend, 
                                               dfne, url)
                            dfne = dft[0]
                            dfe = dft[1]
                finally:
                    time.sleep(sleep)
        if len(dfe) != 0:
            dfe = dfe[list(dfns.columns) + ['Error']]
        dfne.drop_duplicates(inplace=True)
        dfne.drop_duplicates(subset=['ID', 'URL to scrape'], inplace=True)
        dfne.reset_index(drop=True, inplace=True)
        dfne = dfne[list(dfns.columns)+['URL to scrape']]
        dfne.to_csv(
            r'{0}{1}_{2}_{3}{4}'.format(self.scrape_path, 
                                        self.to_scrape_file, 
                                        self.version, 
                                        slice, 
                                        self.csv_ext), 
            sep = self.csv_delimiter, 
            encoding = self.csv_encoding, 
            index = None, 
            header=True)
        dfnt = pd.read_csv(
            r'{0}{1}_{2}_{3}{4}'.format(self.scrape_path, 
                                        self.to_scrape_file, 
                                        self.version, 
                                        slice, 
                                        self.csv_ext), 
            delimiter = self.csv_delimiter,
            encoding = self.csv_encoding, 
            dtype = str)
        return [dfnt, dfe]


    def scrape_urls(self, dfnt, *args, **kwargs):
        what = kwargs.get('what', '')
        sleep = kwargs.get('sleep', 1)
        timeout = kwargs.get('timeout', 5)
        slice = kwargs.get('slice', 0)
        dfl = kwargs.get('dflook', None)
        dfnes = pd.DataFrame()
        dfe = pd.DataFrame()
        with tqdm(total=len(list(dfnt.iterrows()))) as pbar:
            for index, row in dfnt.iterrows():
                pbar.set_description(
                    'processed: %s %s ' % (row['ID'], 
                                           row['URL to scrape'])
                    )
                pbar.update(1)
                s = requests.Session()
                a = requests.adapters.HTTPAdapter(
                                pool_connections=100, 
                                pool_maxsize=100, 
                                max_retries=20, 
                                pool_block=False)
                s.mount('https://', a)
                s.mount('http://', a)
                try:
#                    page = requests.get(row['URL to scrape'], 
                    page = s.get(row['URL to scrape'], 
                                        headers=self.headers, 
                                        timeout=timeout, 
                                        verify=True)
                except requests.ConnectionError:
                    dfe = self.df_append(dfnt, row, dfe, 
                                         'Connection problems')
                    if what == 'word_count':
                        dfnes = self.df_append(dfnt, row, dfnes, '', 
                                               what='word_count')
                except requests.HTTPError:
                    dfe = self.df_append(dfnt, row, dfe, 'HTTP error')
                    if what == 'word_count':
                        dfnes = self.df_append(dfnt, row, dfnes, '', 
                                               what='word_count')
                except requests.Timeout:
                    dfe = self.df_append(dfnt, row, dfe, 
                                         'Timeout occurred')
                    if what == 'word_count':
                        dfnes = self.df_append(dfnt, row, dfnes, '', 
                                               what='word_count')
                except requests.TooManyRedirects:
                    dfe = self.df_append(dfnt, row, dfe, 
                                         'Too many redirects')
                    if what == 'word_count':
                        dfnes = self.df_append(dfnt, row, dfnes, '', 
                                               what='word_count')
                except requests.RequestException:
                    dfe = self.df_append(dfnt, row, dfe, 
                                         'Request exception')
                    if what == 'word_count':
                        dfnes = self.df_append(dfnt, row, dfnes, '', 
                                               what='word_count')
                except requests.SSLError:
                    dfe = self.df_append(dfnt, row, dfe, 
                                         'Certificate verification error')
                    if what == 'word_count':
                        dfnes = self.df_append(dfnt, row, dfnes, '', 
                                               what='word_count')
                except:
                    dfe = self.df_append(dfnt, row, dfe, 'General exception')
                    if what == 'word_count':						
                        dfnes = self.df_append(dfnt, row, dfnes, '', 
                                               what='word_count')
                else:
                    if page.status_code == 200:
                        try:
                            bs = BeautifulSoup(page.content,'lxml')
                        except:
                            dfe = self.df_append(
                                dfnt, row, dfe, 
                                'Read page content with BeautifulSoup')
                            if what == 'word_count':						
                                dfnes = self.df_append(dfnt, row, dfnes, '', 
                                                       what='word_count')
                        else:
                            [
                                s.decompose() for s in bs(
                                    ['iframe', 'script', 'style'])
                            ]
                            texts = bs.getText()
                            texts = re.sub(
                                ' +', 
                                ' ',
                                texts.replace(
                                    '\n', 
                                    ' ').replace(
                                        '\t', 
                                        ' ').replace(
                                            '\r', 
                                            ' ').strip()
                            )
                            texts = texts.lower()
                            dfnes = self.df_append(
                                dfnt, row, dfnes, texts, what=what, dfl=dfl)
                    else:
                        if what == 'word_count':						
                            dfnes = self.df_append(dfnt, row, dfnes, '', 
                                                   what='word_count')
                finally:
                    time.sleep(sleep)
        if len(dfe) != 0:
            dfe = dfe[list(dfnt.columns)+['Error']]
        dfnes = dfnes[list(dfnt.columns)+self.words]
        dfnes.to_csv( 
            r'{0}{1}_{2}_{3}{4}'.format(self.scrape_path, 
                                        self.scrape_file, 
                                        self.version, 
                                        slice, 
                                        self.csv_ext), 
            sep=self.csv_delimiter, 
            encoding = self.csv_encoding, 
            index = None, 
            header=True)
        return [dfnes, dfe]

		
    def df_append(self, dfc, row, dfe, str, *args, **kwargs):
        dfl = kwargs.get('dfl', None)
        what = kwargs.get('what', '')
        lst = list(dfc.columns)
        if what == 'word_count':
            for word in self.words:
                lst.append(word)
                row[word] = str.lower().count(word.lower())            		
        elif what == 'find_enterprise_information': 
            dfl=dfl.loc[dfl['ID'] == row['ID']]		
            for word in self.words:
                lst.append(word)
                row[word] = 1 if re.search(
                                    re.escape(dfl[word[4:]].iloc[0]), 
                                    str, 
                                    re.IGNORECASE) \
                                and re.escape(dfl[word[4:]].iloc[0]) \
                              else 0
        elif str[:7].lower() in ['http://', 'https:/']:
            lst.append('URL to scrape')
            row['URL to scrape'] = str
        else:
            lst.append('Error')
            row['Error'] = str		
        dfe=dfe.append(
            {
                lst[i]: row[lst[i]] for i in range(0, len(lst), 1)
            }, 
            ignore_index=True
        )
        return dfe


    def add_url(self, topurls, dfns, row, dfe, urlsat, dfne, url):
        lst = [
            '.exe', 
            '.pdf', 
            '.xml', 
            '.jpg', 
            '.png', 
            '.gif', 
            '.zip', 
            '.rar', 
            '.mp4', 
            'webm',											
            '.ogg',											
            '.avi', 
            '.doc', 
            'docx',
            'javascript'
            ]
        i = 0
        for topurl in topurls:
            geturl = topurl.get('href')
            if geturl is None:
                geturl = row[url]
            if geturl:
                prefix, success, geturl = geturl.partition("#")
                if not success: 
                    geturl = prefix
            try:
                u1 = urlparse(geturl)
                u2 = urlparse(row[url])
            except:
                dfe = self.df_append(dfns, row, dfe, 'URL parse')				
            else:
                if geturl and geturl[0:2] == '//':
                    geturl = (u2.scheme
                              + ':'
                              + geturl)
                elif geturl and geturl[0:1] == '/':
                    geturl = (u2.scheme
                              + '://'
                              + u2.netloc
                              + geturl)
                elif (geturl 
                        and geturl[0:4] != 'http' 
                        and geturl[0:6] != 'mailto'
                        ):
                    geturl = (u2.scheme
                              + '://'
                              + u2.netloc
                              + '/'
                              + geturl)
                if (not any(ext in geturl for ext in lst)
                        and geturl 
                        and i < urlsat 
                        and (u1.netloc in u2.netloc 
                             or u2.netloc in u1.netloc 
                             or u1.netloc=='')
                        and geturl[:7].lower() in ['http://', 'https:/']
                        ):
                    geturl = unquote(geturl)
                    dfne = self.df_append(dfns, row, dfne, geturl)
                    i = i + 1
            if i == urlsat:
                break
        return [dfne, dfe]


    def get_obec_words(self):
        ow = self.load_files(file='obec_words_file')
        ow = ow.iloc[:,0]
        ow = ow.drop_duplicates(keep = 'first')
        self.words = ow.tolist()
        print('OBEC term matrix key words:\n{0}'.format(self.words))
		
		
