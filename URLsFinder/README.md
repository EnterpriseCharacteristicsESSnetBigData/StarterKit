# URLs Finder Example

Part of [Starter Kit](https://github.com/EnterpriseCharacteristicsESSnetBigData/StarterKit "GitHub repositiry of Starter Kit on Enterprise characteristics") of [ESSnet BigData](https://webgate.ec.europa.eu/fpfis/mwikis/essnetbigdata/index.php/ESSnet_Big_Data "ESSnet Big Data is a project within the European statistical system (ESS) jointly undertaken by 28 partners.") on [WPC Enterprise characteristics](https://webgate.ec.europa.eu/fpfis/mwikis/essnetbigdata/index.php/WPC_Enterprise_characteristics "Workpackage C (WPC) of ESSnet Big Data focuses on enterprise characteristics.") 

## Description

URLs Finder is a [Python](https://www.python.org/) software for finding enterprises' urls from information in Statistical Business Registers by using web scraping and machine learning. It uses tree modules:
- URLsFinder \- defines methods for scraping information for the enterprises' urls from the internet with the help of search engine [Duck Duck Go](https://duckduckgo.com "The best search engine for privacy").
- URLsFinderPrepare \- defines methods for determine the enterprises' urls from the scraped information from the internet by using logistic regersion machine learning technic.
- StarterKitLogging (optional to use) \- defines methods for storing log records for the others modules work.

## Directory structure

- StarterKit
    - src \- source code
    - **URLsFinder** \- an example of how to use the StarterKit for finding enterprises' urls (this folder)
        - black_list_urls \- directory where an example CSV file with blacklisted URLs is located (input for processing the data)
        - logs \- directory where event logging information is saved
        - sbr_data \- directory where an example CSV file with Enterprises information is located (input data)
        - scrape_data \- directory where example CSV files with scraped Enterprises information are saved (output data)
    - URLsFinder \- an example of how to use the StarterKit for finding enterprises' urls
    - SocialMediaProfiles \- ...
    - ...
        

## How to use

The Jupyter Notebook file **URLs_Finder_Starte_Kit.ipynb** in this directory describes how to use the software.
