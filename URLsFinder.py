# class URLsFinder contains functions responsible to find URLs of Enterprises
class URLsFinder:
    def __init__(self,startpath,startfile,csv_delimiter,csv_encoding,scrapepath,sapifile,toscrapefile,scrapefile,headers,blacklistpath,blacklistfile):
        self.startpath=startpath
        self.startfile=startfile
        self.csv_delimiter=csv_delimiter
        self.csv_encoding=csv_encoding
        self.scrapepath=scrapepath
        self.sapifile=sapifile
        self.toscrapefile=toscrapefile
        self.scrapefile=scrapefile
        self.headers=headers
        self.blacklistpath=blacklistpath
        self.blacklistfile=blacklistfile
    # this method loads csv files with Enterprises ...
    # pd: pandas dataframe object
    # glob: glob object
    # startpath: path to the files with Enterprises information
    # startfile: csv files with Enterprises information
    # csv_delimiter: delimiter of the csv file, eg.: ;
    # csv_encoding: encoding of the csv file, eg.: utf-8
    def loadFiles(self, *args, **kwargs):
        if kwargs.get('file', None)=='blacklist':
            path1 = r'{0}{1}'.format(self.blacklistpath,self.blacklistfile) # use your path            
        else:
            path1 = r'{0}{1}'.format(self.startpath,self.startfile) # use your path
        all_files = glob.glob(path1, recursive=True)
        li = []
        for fn in all_files:
            print(fn)
            df = pd.read_csv(fn,delimiter=self.csv_delimiter,encoding = self.csv_encoding, dtype=str)
            df.replace(regex={r'\n': '', '\t': '', r'\s+': ' '}, inplace=True)
            print('All records {}'.format(df.shape))
            #dfe=df.loc[~(df[SBR_ID].str.contains('\d\d\d\d\d\d\d\d\d', na=False))]
            #print('Records with errors {}'.format(dfe.shape))
            li.append(df)
        df=pd.concat(li, axis=0, ignore_index=True, sort=False)
        df=df.fillna('').astype(str)
        df.columns = df.columns.str.strip()
        return df
    # this method search ...
    def querySearchEngine(self,df, *args, **kwargs):
        sleep=kwargs.get('sleep', 6)
        timeout=kwargs.get('timeout', 3)
        dfn=pd.DataFrame()
        dfe=pd.DataFrame()
        with tqdm(total=len(list(df.iterrows()))) as pbar:
            for index, row in df.iterrows():
                pbar.set_description('processed: %s %s ' % (row['ID'], row['Name']))
                pbar.update(1)
                search_string=re.sub('\s', '+',re.sub('\s+', ' ',re.sub('\r', ' ',re.sub('\n', ' ',row['Name'])).strip()))
                url='https://duckduckgo.com/html/?q={0}'.format(search_string)
                try:
                    page = requests.get(url, headers=self.headers, timeout=timeout)
                except requests.ConnectionError:
                    dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Error':"Connection problems"
                    }, ignore_index=True)
                except requests.HTTPError:
                    dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Error':"HTTP error"
                    }, ignore_index=True)
                except requests.Timeout:
                    dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Error':"Timeout occurred"
                    }, ignore_index=True)
                except requests.TooManyRedirects:
                    dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Error':"Too many redirects"
                    }, ignore_index=True)
                except requests.RequestException:
                    dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Error':"Generic exception"
                    }, ignore_index=True)
                else:
                    if page.status_code == 200:
                        getmax=10
                        i=0
                        try:
                            bs = BeautifulSoup(page.content,'lxml')
                        except:
                            dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Suggested URL':row['Suggested URL'],
                                'Link position':row['Link position'],'URL to scrape':row['URL to scrape'],'Error':"Read page content with BeautifulSoup"
                            }, ignore_index=True)    
                        else:
                            topurls=bs.findAll('a',{'class':['result__a']})
                            for topurl in topurls:
                                geturl=re.search('uddg=(.+)', topurl.get('href'))
                                if geturl and i<getmax and unquote(geturl.group(1))[-4:].lower() not in ['.pdf','.xml','.jpg','.png','.gif','.zip','.rar','.mp4','.avi','.doc','.docx']:
                                    vURL=0
                                    try:
                                        u1=urlparse(unquote(geturl.group(1)))
                                        u2=urlparse(row['URL'])
                                    except:
                                        dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Suggested URL':row['Suggested URL'],
                                            'Link position':row['Link position'],'Error':"URL parse"
                                        }, ignore_index=True)
                                    else:
                                        if urlparse(unquote(geturl.group(1))).netloc==urlparse(row['URL']).netloc:
                                            vURL=1
                                        dfn=dfn.append({
                                            'ID':row['ID'],
                                            'Name':row['Name'],
                                            'URL':row['URL'],
                                            'Suggested URL':unquote(geturl.group(1)),
                                            'Link position':i,
                                            'Has equal domain':vURL
                                        }, ignore_index=True)
                                i=i+1
                finally:
                    time.sleep(sleep)
        dfn.to_csv(r'{0}{1}'.format(self.scrapepath,self.sapifile), sep=self.csv_delimiter, encoding = self.csv_encoding, index = None, header=True)
        return [dfn,dfe]
    def blacklistURLs(self,blacklisturls):
        dfns = pd.read_csv(r'{0}{1}'.format(self.scrapepath,self.sapifile),delimiter=self.csv_delimiter,encoding = self.csv_encoding, dtype=str)
        dfns = dfns[~dfns['Suggested URL'].str.contains('|'.join(blacklisturls))]
        dfns['Suggested URL']= dfns['Suggested URL'].apply(lambda x:unquote(x))
        dfns['Has Simple Suggested URL']=dfns['Suggested URL'].apply(lambda x: 1 if urlparse(x).path in ['','/','/en','/en/'] and urlparse(x).query=='' and urlparse(x).fragment=='' else 0)
        return dfns
    # this method search ...
    def getURLsToScrape(self,dfns, *args, **kwargs):
        sleep=kwargs.get('sleep', 1)
        timeout=kwargs.get('timeout', 5)
        urlsatstart=kwargs.get('urlsatstart', 10)
        urlsatend=kwargs.get('urlsatend', 10)
        dfne=pd.DataFrame()
        dfe=pd.DataFrame()
        with tqdm(total=len(list(dfns.iterrows()))) as pbar:
            for index, row in dfns.iterrows():
                pbar.set_description('processed: %s %s ' % (row['ID'], row['Suggested URL']))
                pbar.update(1)
                try:
                    page = requests.get(row['Suggested URL'], headers=self.headers, timeout=timeout)
                except requests.ConnectionError:
                    dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Suggested URL':row['Suggested URL'],
                        'Link position':row['Link position'],'Error':"Connection problems"
                    }, ignore_index=True)
                except requests.HTTPError:
                    dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Suggested URL':row['Suggested URL'],
                        'Link position':row['Link position'],'Error':"HTTP error"
                    }, ignore_index=True)
                except requests.Timeout:
                    dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Suggested URL':row['Suggested URL'],
                        'Link position':row['Link position'],'Error':"Timeout occurred"
                    }, ignore_index=True)
                except requests.TooManyRedirects:
                    dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Suggested URL':row['Suggested URL'],
                        'Link position':row['Link position'],'Error':"Too many redirects"
                    }, ignore_index=True)
                except requests.RequestException:
                    dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Suggested URL':row['Suggested URL'],
                        'Link position':row['Link position'],'Error':"Generic exception"
                    }, ignore_index=True)
                else:
                    if page.status_code == 200:
                        try:
                            bs = BeautifulSoup(page.content,'lxml')
                        except:
                            dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Suggested URL':row['Suggested URL'],
                                'Link position':row['Link position'],'URL to scrape':row['URL to scrape'],'Error':"Read page content with BeautifulSoup"
                            }, ignore_index=True)    
                        else:
                            topurls=bs.findAll('a')
                            i=0
                            for topurl in topurls:
                                geturl=topurl.get('href')
                                if geturl:
                                    prefix, success, geturl=geturl.partition("#")
                                    if not success: geturl = prefix
                                try:
                                    u1=urlparse(geturl)
                                    u2=urlparse(row['Suggested URL'])
                                except:
                                    dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Suggested URL':row['Suggested URL'],
                                        'Link position':row['Link position'],'Error':"URL parse"
                                    }, ignore_index=True)
                                else:
                                    if geturl and geturl[0:2]=='//':
                                        geturl=urlparse(row['Suggested URL']).scheme+':'+geturl
                                    elif geturl and geturl[0:1]=='/':
                                        geturl=urlparse(row['Suggested URL']).scheme+'://'+urlparse(row['Suggested URL']).netloc+geturl
                                    elif geturl and geturl[0:4]!='http' and geturl[0:6]!='mailto':
                                        geturl=urlparse(row['Suggested URL']).scheme+'://'+urlparse(row['Suggested URL']).netloc+'/'+geturl.partition("@")[-1]
                                    if geturl and i<urlsatstart and urlparse(geturl).netloc==urlparse(row['Suggested URL']).netloc and geturl[-4:].lower() not in ['.pdf','.xml','.jpg','.png','gif','.zip']:
                                        dfne=dfne.append({
                                            'ID':row['ID'],
                                            'Name':row['Name'],
                                            'URL':row['URL'],
                                            'Suggested URL':row['Suggested URL'],
                                            'Link position':row['Link position'],
                                            'Has Simple Suggested URL':row['Has Simple Suggested URL'],
                                            'Has equal domain':row['Has equal domain'],
                                            'URL to scrape':unquote(geturl)
                                        }, ignore_index=True)
                                        i=i+1
                                if i==urlsatstart:
                                    break
                            i=0
                            for topurl in reversed(topurls):
                                geturl=topurl.get('href')
                                if geturl:
                                    prefix, success, geturl=geturl.partition("#")
                                    if not success: geturl = prefix
                                try:
                                    u1=urlparse(geturl)
                                    u2=urlparse(row['Suggested URL'])
                                except:
                                    dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Suggested URL':row['Suggested URL'],
                                        'Link position':row['Link position'],'Error':"URL parse"
                                    }, ignore_index=True)
                                else:
                                    if geturl and geturl[0:2]=='//':
                                        geturl=urlparse(row['Suggested URL']).scheme+':'+geturl
                                    elif geturl and geturl[0:1]=='/':
                                        geturl=urlparse(row['Suggested URL']).scheme+'://'+urlparse(row['Suggested URL']).netloc+geturl
                                    elif geturl and geturl[0:4]!='http' and geturl[0:6]!='mailto':
                                        geturl=urlparse(row['Suggested URL']).scheme+'://'+urlparse(row['Suggested URL']).netloc+'/'+geturl.partition("@")[-1]
                                    if geturl and i<urlsatend and urlparse(geturl).netloc==urlparse(row['Suggested URL']).netloc and geturl[-4:].lower() not in ['.pdf','.xml','.jpg','.png','gif','.zip']:
                                        dfne=dfne.append({
                                            'ID':row['ID'],
                                            'Name':row['Name'],
                                            'URL':row['URL'],
                                            'Suggested URL':row['Suggested URL'],
                                            'Link position':row['Link position'],
                                            'Has Simple Suggested URL':row['Has Simple Suggested URL'],
                                            'Has equal domain':row['Has equal domain'],
                                            'URL to scrape':unquote(geturl)
                                        }, ignore_index=True)
                                        i=i+1
                                if i==urlsatend:
                                    break
                finally:
                    time.sleep(sleep)
        dfne.drop_duplicates(inplace=True)
        dfne.drop_duplicates(subset=['ID', 'URL to scrape'], inplace=True)
        dfne.reset_index(drop=True, inplace=True)
        dfne.to_csv(r'{0}{1}'.format(self.scrapepath,self.toscrapefile), sep=self.csv_delimiter, encoding = self.csv_encoding, index = None, header=True)
        dfnt = pd.read_csv(r'{0}{1}'.format(self.scrapepath,self.toscrapefile),delimiter=self.csv_delimiter,encoding = self.csv_encoding, dtype=str)
        return [dfnt,dfe]
    # this method search ...
    def scrapeURLs(self,frame,dfnt, *args, **kwargs):
        sleep=kwargs.get('sleep', 1)
        timeout=kwargs.get('timeout', 5)
        dfnes=pd.DataFrame()
        dfe=pd.DataFrame()
        with tqdm(total=len(list(dfnt.iterrows()))) as pbar:
            for index, row in dfnt.iterrows():
                pbar.set_description('processed: %s %s ' % (row['ID'], row['URL to scrape']))
                pbar.update(1)
                try:
                    page = requests.get(row['URL to scrape'], headers=self.headers, timeout=timeout)
                except requests.ConnectionError:
                    dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Suggested URL':row['Suggested URL'],
                        'Link position':row['Link position'],'URL to scrape':row['URL to scrape'],'Error':"Connection problems"
                    }, ignore_index=True)
                except requests.HTTPError:
                    dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Suggested URL':row['Suggested URL'],
                        'Link position':row['Link position'],'URL to scrape':row['URL to scrape'],'Error':"HTTP error"
                    }, ignore_index=True)
                except requests.Timeout:
                    dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Suggested URL':row['Suggested URL'],
                        'Link position':row['Link position'],'URL to scrape':row['URL to scrape'],'Error':"Timeout occurred"
                    }, ignore_index=True)
                except requests.TooManyRedirects:
                    dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Suggested URL':row['Suggested URL'],
                        'Link position':row['Link position'],'URL to scrape':row['URL to scrape'],'Error':"Too many redirects"
                    }, ignore_index=True)
                except requests.RequestException:
                    dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Suggested URL':row['Suggested URL'],
                        'Link position':row['Link position'],'URL to scrape':row['URL to scrape'],'Error':"Generic exception"
                    }, ignore_index=True)
                else:
                    vID=0
                    vName=0
                    vPhone=0
                    vEmail=0
                    vAddress=0
                    vPopulatedplace=0
                    vDomain=0
                    if page.status_code == 200:
                        try:
                            bs = BeautifulSoup(page.content,'lxml')
                        except:
                            dfe=dfe.append({'ID':row['ID'],'Name':row['Name'],'URL':row['URL'],'Suggested URL':row['Suggested URL'],
                                'Link position':row['Link position'],'URL to scrape':row['URL to scrape'],'Error':"Read page content with BeautifulSoup"
                            }, ignore_index=True)    
                        else:
                            [s.extract() for s in bs('script')]
                            texts=bs.getText()
                            texts=re.sub(' +', ' ',texts.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').strip())
                            dfl=frame
                            dfs=dfl.loc[dfl['ID'] == row['ID']]
                            if re.search(re.escape(dfs['ID'].iloc[0]), texts, re.IGNORECASE):
                                vID=1
                            if re.search(re.escape(dfs['Name'].iloc[0]), texts, re.IGNORECASE):
                                vName=1
                            if re.search(re.escape(dfs['Phone'].iloc[0]), texts, re.IGNORECASE):
                                vPhone=1
                            if re.search(re.escape(dfs['Email'].iloc[0]), texts, re.IGNORECASE):
                                vEmail=1
                            if re.search(re.escape(dfs['Address'].iloc[0]), texts, re.IGNORECASE):
                                vAddress=1
                            if re.search(re.escape(dfs['Populated place'].iloc[0]), texts, re.IGNORECASE):
                                vPopulatedplace=1
                            if re.search('@',dfs['Email'].iloc[0], re.IGNORECASE):
                                if re.search(dfs['Email'].iloc[0].split("@",1)[1], row['Suggested URL'], re.IGNORECASE):
                                    vDomain=1
                    dfnes=dfnes.append({
                        'ID':row['ID'],
                        'Name':row['Name'],
                        'URL':row['URL'],
                        'Suggested URL':row['Suggested URL'],
                        'Link position':row['Link position'],
                        'URL to scrape':row['URL to scrape'],
                        'Status code': page.status_code,
                        'Has Simple Suggested URL':row['Has Simple Suggested URL'],
                        'Has equal domain':row['Has equal domain'],
                        'Has ID':vID,
                        'Has Name':vName,
                        'Has Phone':vPhone,
                        'Has Email':vEmail,
                        'Has equal Email and URL Domains':vDomain,
                        'Has Address':vAddress,
                        'Has Populated place':vPopulatedplace
#                        'Has Simple Suggested URL':vSimpleURL
                    }, ignore_index=True)
                finally:
                    time.sleep(sleep)
        dfnes.to_csv(r'{0}{1}'.format(self.scrapepath,self.scrapefile), sep=self.csv_delimiter, encoding = self.csv_encoding, index = None, header=True)
        return [dfnes,dfe]