import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from chromedriver_autoinstaller import install as chromedriver_install
import python_utils.generic_utils as gu
import pendulum
import time

# Automatically download and install the appropriate ChromeDriver version
chromedriver_install()

# Driver (manual install): https://googlechromelabs.github.io/chrome-for-testing/

def close_pop_up(driver):
    try:
        # Check if the pop-up is present, if it is, close it
        pop_up_close_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@class='close']")))
        pop_up_close_button.click()
    except:
        pass
    
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
    source_name = "rf"
    today = pendulum.today().date()
    etl_date = today.to_date_string()

    try:
        driver.get(url)

        # Define a WebDriverWait with a timeout of 10 seconds
        wait = WebDriverWait(driver, 10)

        while True:           
            # Get the current page source
            page_source = driver.page_source

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')

            # Find all table rows excluding the header row
            data_rows = soup.find_all('tr')[1:]

            # Iterate through each data row and extract the desired information
            for row in data_rows:
                cells = row.find_all('td')
                if len(cells) == 4:  # Ensure that there are exactly 4 cells in each row
                    
                    company_name = cells[0].get_text(strip=True)
                    industry = cells[1].get_text(strip=True)
                    price = cells[2].get_text(strip=True)
                    min_qty = cells[3].get_text(strip=True)

                data[company_name] = {"Price": price,
                                      "Lot Size": min_qty,
                                      "Industry": industry,
                                      "Source": source_name,
                                      "ETL Date": etl_date
                                      }

            # Close any pop-up advertisements
            close_pop_up(driver)
            
            # Try to find the "Next" button by its attributes, if it's not found, break the loop
            try:
                next_button = driver.find_element("xpath", "//*[@class='paginate_button next']")  # Modify the XPath as needed
            except:
                break
            
            # Check if the "Next" button is disabled, if so, break the loop
            if 'disabled' in next_button.get_attribute('class'):
                break

            # Click the "Next" button to go to the next page
            next_button.click()
            
            # Wait for a short while to load the next page (you may need to adjust this)
            time.sleep(5)
            
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
url = "https://rurashfin.com/unlisted-shares-list/"
_ = scrape_data(url, output_path="data")
