# Source code

Part of [Starter Kit](https://github.com/EnterpriseCharacteristicsESSnetBigData/StarterKit "GitHub repositiry of Starter Kit on Enterprise characteristics") of [ESSnet BigData](https://webgate.ec.europa.eu/fpfis/mwikis/essnetbigdata/index.php/ESSnet_Big_Data "ESSnet Big Data is a project within the European statistical system (ESS) jointly undertaken by 28 partners.") on [WPC Enterprise characteristics](https://webgate.ec.europa.eu/fpfis/mwikis/essnetbigdata/index.php/WPC_Enterprise_characteristics "Workpackage C (WPC) of ESSnet Big Data focuses on enterprise characteristics.") 

## Description

The [Python](https://www.python.org/) files are:
- URLsFinder \- defines methods for scraping information for the enterprises' urls from the internet with the help of search engine [Duck Duck Go](https://duckduckgo.com "The best search engine for privacy").
- URLsFinderPrepare \- defines methods for determine the enterprises' urls from the scraped information from the internet by using logistic regersion machine learning technic.
- StarterKitLogging (optional to use) \- defines methods for storing log records for the others modules work.
- SocialMediaPresenceCollector.py \- defines classes and methods for finding social media links on websites.
- DomainScraper.py \- defines the class to scrape domains/websites including internal links.

## Directory structure

- StarterKit
    - **src** \- source code of the modules (this folder)
    - URLsFinder \- an example of how to use the StarterKit for finding enterprises' urls
    - SocialMediaProfiles \- Identifying social media links on enterprise websites.
    - URLScraper \- Scrape a list of URLs and safe the HTML code in a NoSQL database for later analysis.

## How to use

### URLsFinder

Go to the respective folder. There is a Jupyter Notebook file **URLs_Finder_Starter_Kit.ipynb** that describes how to use the software.

### SocialMediaProfiles

Go to the respective folder. The Jupyter Notebook file **Starter-Kit_Social_Media_Profiles.ipynb** describes how to use the software.

### URLScraper
You find the Jupyter Notebook file **URLScraperApplication.ipynb** in the respective folder.

## To do

- URLsFinder \- improve code readability and add comments.
- URLsFinderPrepare \- improve code readability and add comments.
- StarterKitLogging (optional to use) \- improve code readability and add comments.

