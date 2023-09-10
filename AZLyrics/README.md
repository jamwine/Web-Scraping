# AZLyrics

This project aims to scrape music information such as artists, albums, songs, and lyrics from URL: `https://azlyrics.com/`.

## Steps to begin

Ensure that you're in the correct directory path, this can be checked using `pwd` command: `.../Web-ScrapingAZLyrics`.
The `ls` command should return this:

```bash
$ ls
data/  README.md  scrape_artists.py
```

1. Simply run the Python script that utilizes BeautifulSoap using command `python scrape_artists.py` to save all artists names and their URLs in a json format.
   * The output file is: `artists.json` inside the `data/artists` directory.
