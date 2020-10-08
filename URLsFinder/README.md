# URLs Finder Example

Part of [Starter Kit](https://github.com/EnterpriseCharacteristicsESSnetBigData/StarterKit "GitHub repositiry of Starter Kit on Enterprise characteristics") of [ESSnet BigData](https://webgate.ec.europa.eu/fpfis/mwikis/essnetbigdata/index.php/ESSnet_Big_Data "ESSnet Big Data is a project within the European statistical system (ESS) jointly undertaken by 28 partners.") on [WPC Enterprise characteristics](https://webgate.ec.europa.eu/fpfis/mwikis/essnetbigdata/index.php/WPC_Enterprise_characteristics "Workpackage C (WPC) of ESSnet Big Data focuses on enterprise characteristics.") 

## Description

URLs Finder is a [Python](https://www.python.org/) software for finding enterprises' urls from information in Statistical Business Registers by using web scraping and machine learning. It uses four modules:
    - obec.py \- Initialization code for the URLs Finder Stater Kit classes to be used with Jupyter Notebook.
    - URLsFinderWS.py \- defines methods for scraping information for the enterprises' urls from the internet with the help of search engine [Duck Duck   Go](https://duckduckgo.com "The best search engine for privacy").
    - URLsFinderMLLR.py \- defines methods for determine the enterprises' urls from the scraped information from the internet by using logistic regersion machine  learning technic.
    - StarterKitLogging.py (optional to use) \- defines methods for storing log records for the others modules work.

## Directory structure

- StarterKit
    - src \- source code
    - **URLsFinder** \- an example of how to use the Starter Kit for finding enterprises' urls (**this folder**)
        - scrape_data \- Destination folder for scraped data
        - sbr_data \- Source folder for statistical business register data used for scraping
        - logs \- Location of saved log files
        - black_list_urls \- Location for the blacklist of URLs that should be ignored by the URLs finder
        - machine_learning \- Results from machine learning predictions for URLs of enterprises
    - SocialMediaProfiles \- an example of how to use the Starter Kit for finding enterprises' social media presence
    - URLScraper \- an example of how to use the Starter Kit for scraping enterprises' websites
        

## How to use

The Jupyter Notebook file **OBEC_Starter_Kit_URLs_Finder.ipynb** in this directory describes how to use the software.
