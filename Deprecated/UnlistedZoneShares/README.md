# Unlisted Zone Shares

Parse and extract financial information for stock analysis of companies based on the [Unlisted Zone Shares](https://unlistedzone.com/shares/).

**Unlisted Shares** is one of the leading startup to facilitate in India where transactions of purchase and selling a myriad of Unlisted, ESOP, or Pre-IPO Shares. This study aims to utilize crawling tools, by utilizing Scrapy, to acquire the data that can be found on the aforementioned website and store it in JSON and CSV files.

## Database Specification

| Attributes | Data Type | Description |
|--|--|--|
| Company | text | Indicates the Name of the company. |
| Lot Size | text | Amount of shares for a lot. |
| Last Price | text | Price of the trade made the last time. |

## Project Files

---------------------------------------------------------
    ├── UnlistedZoneShares #Source codes for this project.                        
      |
      │ 
      ├── data    #Folder containing JSON and CSV files                                                  
      |    |
      │    ├── uzs_yyyymmdd.csv                             
      │    |
      │    └── uzs_yyyymmdd.json                
      │                          
      │                    
      ├── scrapy.cfg    #Configuration settings for Scrapy.                        
      │ 
      |
      ├── README.md #The project-level README for developers.  
      │                                                       
      │ 
      │── UnlistedZoneShares    #Scrapy project folder.                            
           │
           ├── spiders                         
           │    |
           │    ├── __init__.py                        
           │    |
           │    └── crawl_unlisted_zone_shares.py                        
           │
           ├── __init__.py
           │
           ├── items.py       
           │           
           ├── middlewares.py      
           │                  
           ├── pipelines.py
           │                    
           ├── settings.py                         

---------------------------------------------------------

## Steps to begin

Ensure that you're in the correct directory path before running any spiders, this can be checked using `pwd` command: `.../Web-Scraping/UnlistedZoneShares`.
The `ls` command should return this:

```bash
$ ls
README.md  scrapy.cfg  UnlistedZoneShares/ data/
```

Run the crawler `scrapy crawl scrape_unlisted_zone_shares` to extract unlisted companies of India in JSON and CSV files.

* The output files are: `uzs_yyyymmdd.json` and `uzs_yyyymmdd.json` inside the `data/` directory.
