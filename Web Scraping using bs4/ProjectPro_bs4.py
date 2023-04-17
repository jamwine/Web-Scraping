import time as t
import requests
from bs4 import BeautifulSoup
import pandas as pd


class ProjectPro:
    def __init__(self):
        # Initialize user-agent
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
        }

    def get_data(self, df, page_number):
        # Setups for bs4
        url = 'https://www.projectpro.io/blog/page_no/' + str(page_number)
        req = requests.get(url, self.headers)

        # Scraping Code
        soup = BeautifulSoup(req.text, 'lxml')
        dates = soup.find_all('div', attrs={'class', 'p-3'})

        for i in dates:
            projects = i.find('a').text.strip()
            date = i.find('time').text
            links = i.find('img').get('data-src')
            df.loc[len(df)] = {'projects': projects, 'date': date, 'links': links}


if __name__ == '__main__':
    # Object Initialization
    web = ProjectPro()

    # DataFrame
    df = pd.DataFrame(columns=['projects', 'date', 'links'])

    page_limit = 7
    # Pagination
    for page_number in range(1, page_limit+1):
        t.sleep(3)
        web.get_data(df, page_number)

    # Save as storage
    df.to_excel("project_pro_bs4.xlsx")
    df.to_json("project_pro_bs4.json")
    df.to_xml("project_pro_bs4.xml")

