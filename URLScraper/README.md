<h1>URL Scraper Starter Kitt</h1>
<h2>Structure of this Starter Kitt</h2>
    <ol>
<li>Source code (in Python):
    <ol>
        <li>library</li>
        <li>standalone application</li>
        <li>self-tutorial of application</li>
    </ol>
<li>Jupyter Notebook files (ipynb) including manuals inside</li>
<li>Example files - data with urls - url.txt</li>
</ol>
<h3>Data processing schema</h3>
    <p>URL list in files -&gt; URLScraper -&gt; Websites in NoSQL collections for further processing</p>
<h3>Prerequisites</h3><p>Create a file url.txt with the following structure (one row for one url):</p>
<p><a href="http://stat.gov.pl">http://stat.gov.pl</a></p>
<p><a href="http://destatis.de">http://destatis.de</a></p>
<p><a href="http://www.nsi.bg">http://www.nsi.bg</a></p>
<p>Five steps to run this application.</p>
<ol>
<li>Import libraries</li>
<li>Create a connection to mongodb server</li>
<li>Set the database name</li>
<li>Set the file name of URLs to import</li>
<li>Start the web scraping</li>
</ol>

# How to use a library

import URLScraperLibrary as usl

usl.startScraping()

# Initial work

1. Install MongoDB.

2. Install Anaconda with Python 3.

3. Get the pymongo library:

easy_install pymongo

OR

pip install pymongo

OR

python -m pip install pymongo

OR

conda install pymonog

OR

python3 -m pip install pymongo
