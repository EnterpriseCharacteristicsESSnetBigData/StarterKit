# Starter Kit: Web Scraping for Enterprise Characteristics

## What is this Starter Kit intended for?

This Starter Kit is a deliverable of the [WPC Enterprise characteristics](https://webgate.ec.europa.eu/fpfis/mwikis/essnetbigdata/index.php/WPC_Enterprise_characteristics "Workpackage C (WPC) focuses on web scraping for enterprise characteristics") which is part of the [ESSnet Big Data II](https://webgate.ec.europa.eu/fpfis/mwikis/essnetbigdata/index.php/ESSnet_Big_Data "ESSnet Big Data II is a project within the European statistical system (ESS) with 28 participating statistical authorities.").

This Starter Kit is intended as an introduction to web scraping for enterprise characteristics. We hope that it will support producers of official statistics with implementing their own web scraping routines to derive enterprise characteristics. However, the methods and functions in this Starter Kit most likely need to be adapted to the individual needs and particularities in the respective countries.

## Contents of the Starter Kit

The Starter Kit has (so far) three parts:
- URLsFinder: A library to identify enterprise URLs with the search engine [Duck Duck Go](https://duckduckgo.com "The best search engine for privacy").
- URLScraper: Functions to scrape a list of URLs and safe the HTML code in a NoSQL database for later analysis.
- SocialMediaProfiles: A library to identify social media links on enterprise websites.


Each part of the Starter Kit has a **Jupyter Notebook** (file with .ipynb extension) that serves as a manual on how to use the functions and methods. These manuals are intended for statisticians with little to no programming background and can be viewed on this website. The source code can be consulted by users with a background in programming.

## Setting up the environment

The Starter Kit is written for **Python 3** (note: on Python 2 the applications will not work). We recommend to install **Python** with the [Anaconda](https://www.anaconda.com/ "Solutions for Data Science Practitioners and Enterprise Machine Learning") distribution. [Anaconda](https://www.anaconda.com/ "Solutions for Data Science Practitioners and Enterprise Machine Learning") comes with several pre-installed libraries that will be used in the Starter Kit. Occasionally, you will need to install additional libraries. Those will be mentioned in the respective part of the Starter Kit. Also, [Anaconda](https://www.anaconda.com/ "Solutions for Data Science Practitioners and Enterprise Machine Learning") distribution comes with pre-installed **Jupyter Notebook** software. For instructions on how to install Anaconda on your system, consult the [Anaconda installation tutorials](https://docs.anaconda.com/anaconda/install/) that are available for many operating systems.

You can install libraries with the following commands in Anaconda Prompt (or the command line tool of your choice):

conda install \<library name\> <br/>
OR<br/>
pip install \<library name\>

Substitute \<library name\> with the name of the library, for example for the library bs4: "pip install bs4".


## Directory structure
The current folder has the following directories:
  - src \- source code of the modules
    - URLsFinder.py \- defines methods for finding enterprise URLs with the help of the search engine [Duck Duck Go](https://duckduckgo.com "The best search engine for privacy").
    - URLsFinderPrepare.py \- defines methods for determining the correct enterprise URLs among all found URLs by using machine learning (logistic regression).
    - StarterKitLogging.py (optional use) \- defines methods for storing log records for the URL finder.
  - URLsFinder
    - URLs_Finder_Starter_Kit.ipynb \- Manual on how to use the library for URL finding
    - scrape_data \- Destination folder for scraped data
    - sbr_data \- Source folder for statistical business register data used for scraping
    - logs \- Location of safed log files
    - black_list_urls \- Location for the blacklist of URLs that should not be ignored by the URL finder
  - SocialMediaProfiles
    - Starter-Kit_Social_Media_Profiles.ipynb \- Manual on how to use the library for finding social media links
    - SocialMediaPresenceCollector.py \- Source code for finding social media links (will be moved into folder src)
    - url.txt \- example data
  - URLScraper
    - URLScraperApplication.ipynb \- Manual on how to scrape URLs
    - URLScraperApplication.py \- Standalone application for scraping URLs to be run in the command line (does the same as the Jupyter Notebook)
    - URLScraperLibrary.py \- URL Scraper as library that can be imported
    - url.txt \- example data


## Additional Resources
Here are some alternative softwares used by the ESS for several years that you may try:
- [urlfinding](https://github.com/SNStatComp/urlfinding "Repository for the CBS URL finder"): Generic software for finding websites of enterprises using [Google Search Engine](https://www.google.com) and Machine Learning by [Statistics Netherlands](https://www.cbs.nl/en-gb). Remark: only a 100 Google search queries per day are free.
- [SummaIstat](https://github.com/SummaIstat "Repositories for Web Scraping for Enterprise Characteristics"): Software tools by [Italian Statistics](https://www.istat.it/en/) for Web Scraping for Enterprise Characteristics in [Java](https://www.java.com/en/) and [Solr](https://lucene.apache.org/solr/). It uses the [Bing Search Engine](https://www.bing.com/) for finding websites of enterprises.
