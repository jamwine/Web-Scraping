import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chromedriver_autoinstaller import install as chromedriver_install
import python_utils.generic_utils as gu

# Driver (manual install): https://googlechromelabs.github.io/chrome-for-testing/

# Automatically download and install the appropriate ChromeDriver version
chromedriver_install()

def scrape_data(url, output_path="."):
    """
    Scrape tabular data from a webpage, save it as XLSX and CSV files, and return a DataFrame.

    This function uses Selenium and BeautifulSoup to scrape tabular data from a webpage, paginates through the content,
    and saves the data as both XLSX and CSV files. It also returns the scraped data as a DataFrame.

    :param url: The URL of the webpage to scrape.
    :param output_folder: (Optional) The folder where the output files will be saved.
    :return: A Pandas DataFrame containing the scraped data.
    """
    
    # Initialize the webdriver using ChromeDriverManager
    driver = webdriver.Chrome()

    data = {}

    try:
        driver.get(url)

        # Define a WebDriverWait with a timeout of 10 seconds
        wait = WebDriverWait(driver, 10)

        # JavaScript to scroll to an element
        def scroll_to_element(element):
            driver.execute_script("arguments[0].scrollIntoView(true);", element)

        while True:
            # Wait for the "Next" button to become clickable
            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.paginate_button.next")))

            # Scroll to the "Next" button using JavaScript
            scroll_to_element(next_button)

            # Get the current page source and parse it
            soup = BeautifulSoup(driver.page_source, "html.parser")

            table_div = soup.find("div", {"class": "dataTables_scrollBody"})
            table = table_div.find("table")
            rows = table.find_all("tr")

            # Loop through the rows (starting from the second row to skip the header)
            for row in rows[1:]:
                columns = row.find_all("td")
                if len(columns) >= 9:
                    script_name = columns[2].find("a").text.strip()
                    category = columns[3].text.strip()
                    sector = columns[4].text.strip()
                    price = columns[5].text.strip()
                    market_cap = columns[6].text.strip()

                    data[script_name] = {"Category": category,
                                         "Sector": sector,
                                         "Price (in rupees)": price,
                                         "Market Cap (in crores)": market_cap}

            # Check if there is a "Next" button on the page
            if "disabled" in next_button.get_attribute("class"):
                break  # Break the loop if there's no "Next" button

            # Click the "Next" button using JavaScript to avoid interception
            driver.execute_script("arguments[0].click();", next_button)
            # Wait for the page to load and the "Next" button to become clickable again
            wait.until(EC.staleness_of(next_button))

    finally:
        driver.quit()

    filename = "wwipl"
    
    gu.save_output_in_json(output_file_path = f'{output_path}/{filename}.json', data = data, data_description=f'{filename}_UnlistedShares')
    
    df = pd.DataFrame(data).T.reset_index()
    df.columns = ["Script Name", "Category", "Sector", "Price (in rupees)", "Market Cap (in crores)"]
    df.to_csv(f'{output_path}/{filename}.csv', index=False)
    
    print(f"Data scraped!")

    return df


# Main Program
url = "https://wwipl.com/"
_ = scrape_data(url, output_path="data")
