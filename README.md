# Web-Scraping

This repository contains Web Scraping Projects using Python

* To begin using project, create a virtual environment:
  
```bash
python -m venv /path/to/new/virtual/environment
```

* Activate the Virtual Environment (command can vary on Windows or Linux based systems).
  
```bash
source </path/to/new/virtual/environment>/bin/activate
```

* For instance:

```bash
python -m venv .scrape
source .scrape/bin/activate
```

* Install the dependencies: `pip install -r requirements.txt`

## Scrapy Fundamentals

Scrapy is a very popular open source Python scraping framework for extracting data. It was originally designed for only scraping, but it is has also evolved into a powerful web crawling solution. Scrapy offers a number of powerful features:

* Built-in extensions to make HTTP requests and handle compression, authentication, caching, manipulate user-agents, and HTTP headers

* Built-in support for selecting and extracting data with selector languages such as CSS and XPath, as well as support for utilizing regular expressions for selection of content and links

* Encoding support to deal with languages and non-standard encoding declarations

* Flexible APIs to reuse and write custom middleware and pipelines, which provide a clean and easy way to implement tasks such as automatically downloading assets (for example, images or media) and storing data in storage such as file systems, S3, databases, and others.


### Getting Started with Scrapy

* To create a new project, run the following command in the terminal: `scrapy startproject my_first_spider`

* To create a new spider, first change the directory: `cd my_first_spider`

* Create a spider: `scrapy genspider example example.com`.
When we create a spider, we obtain a Basic Template. The class is built with the data we introduced in the previous command, but the parse method needs to be built by us.

* Run the spider and export data to CSV or JSON

```bash
scrapy crawl example
scrapy crawl example -o name_of_file.csv
scrapy crawl example -o name_of_file.json
```
