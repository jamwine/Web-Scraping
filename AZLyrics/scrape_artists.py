import requests
from bs4 import BeautifulSoup
import string
import time
import python_utils.generic_utils as gu

root_url = "https://www.azlyrics.com"
path = "data/artists"

# Alphabets a-z 
start_urls = {letter:f"{root_url}/{letter}.html" for letter in string.ascii_lowercase}    

# For names beginning with numbers (digits), '#' is encoded as "19"
start_urls["19"] = f"{root_url}/19.html"

artists_tag = "div"
artists_class = {"class":"artist-col"}

data = {}
for letter, url in start_urls.items():
    response = requests.get(url)
    soap = BeautifulSoup(response.text, "lxml")
    
    print(">> Scraping URL: ", url)
    artists_cols = soap.findAll(artists_tag, artists_class)
    for col in artists_cols:
        artists = col.findAll("a")
        for artist in artists:
            data[artist.text] = f"{root_url}/{artist.get('href')}"
    time.sleep(10)
    
gu.save_output_in_json(output_file_path = f'{path}/artists.json', data = data, data_description = 'artists')