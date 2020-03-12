# URLs Finder Example

Part of [Starter Kit](https://github.com/EnterpriseCharacteristicsESSnetBigData/StarterKit "GitHub repositiry of Starter Kit on Enterprise characteristics") of [ESSnet BigData](https://webgate.ec.europa.eu/fpfis/mwikis/essnetbigdata/index.php/ESSnet_Big_Data "ESSnet Big Data is a project within the European statistical system (ESS) jointly undertaken by 28 partners.") on [WPC Enterprise characteristics](https://webgate.ec.europa.eu/fpfis/mwikis/essnetbigdata/index.php/WPC_Enterprise_characteristics "Workpackage C (WPC) of ESSnet Big Data focuses on enterprise characteristics.") 

## 1. Description

URLs Finder is a [Python](https://www.python.org/) software for finding enterprises' urls from information in Statistical Business Registers by using web scraping and machine learning. It has tree modules:
- URLsFinder \- defines methods for scraping information for the enterprises' urls from the internet with the help of search engine [Duck Duck Go](https://duckduckgo.com "The best search engine for privacy").
- URLsFinderPrepare \- defines methods for determine the enterprises' urls from the scraped information from the internet by using logistic regersion machine learning technic.
- StarterKitLogging (optional to use) \- defines methods for storing log records for the others modules work.

These are the [Pythons'](https://www.python.org/) libraries and components that URLs Finder modules need:
- [pandas](https://pandas.pydata.org/) is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool.
- [glob](https://docs.python.org/3/library/glob.html) is an Unix style pathname pattern expansion.
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.
- [requests](https://pypi.org/project/requests/) allows you to send HTTP/1.1 requests extremely easily.
- [re](https://docs.python.org/3/library/re.html) provides regular expression matching operations similar to those found in Perl.
- [numpy](https://numpy.org/) is the fundamental package for scientific computing with Python.
- [time](https://docs.python.org/3/library/time.html) provides various time-related functions.
- [unquote](https://docs.python.org/3/library/urllib.parse.html) replace %xx escapes by their single-character equivalent.
- [urlparse](https://docs.python.org/3/library/urllib.parse.html) parse a URL into six components, returning a 6-item named tuple. This corresponds to the general structure of a URL: scheme://netloc/path;parameters?query#fragment.
- [tqdm](https://pypi.org/project/tqdm/) provides a progress bar.
- [datetime](https://docs.python.org/3/library/datetime.html) module supplies classes for manipulating dates and times.
- [logging](https://docs.python.org/3/library/logging.html) defines functions and classes which implement a flexible event logging system for applications and libraries.

These are the variables that URLs Finder modules uses:
- **version** \- identification of the scraped files by date, id or other.
- **title** \- name of the project, also used for scraped files names.
- **startpath** \- directory where a csv file with Enterprises information is located.
- **scrapepath** \- directory where a csv files with scraped Enterprises information are saved.
- **logpath** \- directory where event logging information is saved. 
- **blacklistpath** \- directory where a csv file with blacklisted URLs is located.
- **startfile** \- name of a csv file with Enterprises information.
- **scrapefile** \- name of a csv file with scraped information from websites.
- **sapifile** \- name of a csv file with scraped information from search engine [Duck Duck Go](https://duckduckgo.com "The best search engine for privacy").
- **toscrapefile** \- name of a csv file with URLs from websites that will be scraped.
- **logfile** \- name of a events log file.
- **blacklistfile** \- name of a csv file with blacklisted URLs.
- **csv_delimiter** \- delimiter of the csv file, eg.: ";".
- **csv_encoding** \- encoding of the csv file, eg.: "utf-8".
- **headers** \- HTTP request header information.

## Structure

Directory structure:
- Starter Kit
    - src \- source code
    - URLsFinder \- example use (this folder)
        - black_list_urls \- directory where a csv file with blacklisted URLs is located
        - logs \- directory where event logging information is saved
        - sbr_data \- directory where a csv file with Enterprises information is located
        - scrape_data \- directory where a csv files with scraped Enterprises information are saved

## How to use
