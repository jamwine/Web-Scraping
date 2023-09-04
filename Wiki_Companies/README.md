# WikiCompanies

This project aims to scrape all the list of US companies and its firmographics data from the Wikipedia infobox.

## Steps to begin

Ensure that you're in the correct directory path before running any spiders, this can be checked using `pwd` command: `.../Web-Scraping/Wiki_Companies`.
The `ls` command should return this:

```bash
$ ls
README.md  scrapy.cfg  Wiki_Companies/
```

1. Run the first scraper `scrapy crawl us_states_url_collection` to generate Wikipedia links of US states having list of companies in a json format.
   * The output files are: `us_state_urls.json` and `us_companies_urls.json` inside the `Wiki_Companies/data/` directory.

2. Run the second scraper `scrapy crawl us_companies_url_collection` to generate a list of US companies Wikipedia links in a json format.
   * The output file is `us_companies_urls.json`, found inside the `Wiki_Companies/data/` directory.

3. Run the third scraper `scrapy crawl company_scraping` to generate the final output of US companies besides its firmographics in a json format.
   * The final output file is `company_scraping.json`, found inside the `Wiki_Companies/data/` directory.
