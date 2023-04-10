import requests
from bs4 import BeautifulSoup
import pandas as pd


class WikiTables:
    def __init__(self):
        # Use bs4 module to get request from the specified url
        url = 'https://en.wikipedia.org/wiki/Minnesota'
        req = requests.get(url)
        self.soup = BeautifulSoup(req.text, 'lxml')

    def get_table(self, df):
        # Extract the first batch of data through inspection
        table = self.soup.find('table', attrs={'class': 'wikitable sortable mw-collapsible'})

        for t in table.findAll('tr'):
            # find the sample in lists
            sample = t.findAll('td')

            if not sample == []:
                # Use index to extract all the tabular data
                year = sample[0].text.strip()
                repub_num = sample[1].text.strip()
                repub_perc = sample[2].text.strip()
                demo_num = sample[3].text.strip()
                demo_perc = sample[4].text.strip()
                third_num = sample[5].text.strip()
                third_perc = sample[6].text.strip()

                # Create a dictionary to append each element of the table through an iterative process
                df = df._append({'year': year,  'repub_num': repub_num,  'repub_perc': repub_perc,  'demo_num': demo_num,
                                'demo_perc': demo_perc,  'third_num': third_num, 'third_perc': third_perc},
                               ignore_index=True)
        print(df, "\nColumns:", df.columns)


if __name__ == "__main__":
    web = WikiTables()

    # Initialize an empty Data frame
    df = pd.DataFrame(columns=['year', 'repub_num', 'repub_perc', 'demo_num', 'demo_perc', 'third_num', 'third_perc'])

    web.get_table(df)
