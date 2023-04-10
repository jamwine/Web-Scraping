import requests
from bs4 import BeautifulSoup
import pandas as pd


class QuoteScraping:
    def __init__(self):
        # Use bs4 module to get request from the specified url
        url = 'https://quotes.toscrape.com/'
        req = requests.get(url)
        self.soup = BeautifulSoup(req.text, 'lxml')

        # Initialize an empty Data frame
        self.data_frame = pd.DataFrame(columns=['Quote', 'Author', 'Tags'])

    def get_data(self):
        # Extract the first batch of data through inspection
        data = self.soup.find_all('div', attrs={'class': 'quote'})

        for i in data:
            # find the sample in lists
            sample = i.find_all()

            # If sample is not an empty list
            if not sample == []:
                # Extract individual element
                quote = sample[0].text.strip()
                author = sample[1].text.replace('by ', '').replace('(about)', '').strip()
                tags = sample[5].get('content')

                # Store inside the initialized Data Frame
                self.data_frame = self.data_frame._append({'Quote': quote, 'Author': author, 'Tags': tags},
                                                          ignore_index=True)
        print(self.data_frame)
        print(self.data_frame.columns, " Size of Data Frame:", len(self.data_frame))


if __name__ == "__main__":
    web = QuoteScraping()
    web.get_data()
