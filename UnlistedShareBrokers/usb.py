import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from chromedriver_autoinstaller import install as chromedriver_install
import python_utils.generic_utils as gu
import pendulum

# Automatically download and install the appropriate ChromeDriver version
chromedriver_install()

# Driver (manual install): https://googlechromelabs.github.io/chrome-for-testing/

def scrape_data(url, output_path="."):
    """
    Scrape tabular data from a webpage, save it as JSON and CSV files, and return a DataFrame.

    This function uses Selenium and BeautifulSoup to scrape tabular data from a webpage, paginates through the content,
    and saves the data as both JSON and CSV files. It also returns the scraped data as a DataFrame.

    :param url: The URL of the webpage to scrape.
    :param output_folder: (Optional) The folder where the output files will be saved.
    :return: A Pandas DataFrame containing the scraped data.
    """
    
    # Initialize the webdriver using ChromeDriverManager
    driver = webdriver.Chrome()

    data = {}
    source_name = "usb"
    today = pendulum.today().date()
    etl_date = today.to_date_string()

    try:
        driver.get(url)

        # Define a WebDriverWait with a timeout of 10 seconds
        wait = WebDriverWait(driver, 10)

        # Get the current page source
        page_source = driver.page_source

        # Parse the page source with BeautifulSoup
        # content = page_source.encode('utf-8').strip()
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all table rows excluding the header row
        table = soup.find("table", {"class": "posts-data-table dataTable no-footer dtr-inline"})
        tbody = table.find("tbody")
        data_rows = tbody.find_all('tr')

        # Iterate through each data row and extract the desired information
        for row in data_rows:
            cells = row.find_all('td')
            
            # Check if the row has at least 6 columns
            if len(cells) >= 6:
                # Extract the data from the columns
                company_name = cells[1].find("a").get_text().strip()
                buy_price = cells[2].get_text().strip()
                sell_price = cells[3].get_text().strip()
                lot_size = cells[4].get_text().strip()
                isin = cells[5].get_text().strip()

            data[company_name] = {"Price": buy_price,
                                    "Sell Price": sell_price,
                                    "Lot Size": lot_size,
                                    "ISIN": isin,
                                    "Source": source_name,
                                    "ETL Date": etl_date
                                    }

    except Exception as e:
        print(f"Exception while scraping: {str(e)}")
    finally:
        driver.quit()

    filename = f'{source_name}_{today.strftime("%Y%m%d")}'
    gu.save_output_in_json(output_file_path = f'{output_path}/{filename}.json', data = data, data_description=f'{source_name}_UnlistedShares')
    
    df = pd.DataFrame(data).T
    columns = list(df.columns)
    df = df.reset_index()
    df.columns = ["Company Name"] + columns
    df.to_csv(f'{output_path}/{filename}.csv', index=False)
    
    print(f"Data scraped!")

    return df


# Main Program
url = "https://www.unlistedsharebrokers.com/"
_ = scrape_data(url, output_path="data")
