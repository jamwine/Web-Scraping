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

## Scrapy Fundamentals

Scrapy is the most powerful web scraping framework in Python

* To create a new project, run the following command in the terminal: `scrapy startproject my_first_spider`

* To create a new spider, first change the directory: `cd my_first_spider`

* Create an spider: `scrapy genspider example example.com`
When we create a spider, we obtain a Basic Template. The class is built with the data we introduced in the previous command, but the parse method needs to be built by us.

* Run the spider and export data to CSV or JSON

```bash
scrapy crawl example
scrapy crawl example -o name_of_file.csv
scrapy crawl example -o name_of_file.json
```
