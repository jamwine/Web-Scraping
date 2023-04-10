import requests
from bs4 import BeautifulSoup
import pandas as pd


class UpcomingEvents:
    def __init__(self):
        # Use bs4 module to get request from the specified url
        url = 'https://www.python.org/events/python-events/'
        req = requests.get(url)
        self.soup = BeautifulSoup(req.text, 'lxml')

    def get_events(self):
        # Initialize an empty Data frame
        df = pd.DataFrame(columns=['Date', 'Event', 'Location'])

        # Extract the desired data through inspection
        data = self.soup.find('ul', attrs={'class': 'list-recent-events menu'}).findAll('li')

        for i in data:
            # Segregate strings into lists for single-element extraction
            string = i.text.strip().split('\n')
            date = string[2]
            event = string[0]
            location = string[3]

            # Create dictionary to append it inside the Data frame through an iterative process
            df = df._append({'Date': date, 'Event': event, 'Location': location}, ignore_index=True)
        print(df, "\nColumns:", df.columns)


if __name__ == "__main__":
    web = UpcomingEvents()
    web.get_events()
