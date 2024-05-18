import requests
from bs4 import BeautifulSoup
import pendulum
import pandas as pd
import python_utils.generic_utils as gu


def scrape_data(url, output_path="."):
    """
    Scrape tabular data from a webpage, save it as JSON and CSV files, and return a DataFrame.

    This function uses BeautifulSoup to scrape tabular data from a webpage, paginates through the content,
    and saves the data as both JSON and CSV files. It also returns the scraped data as a DataFrame.

    :param url: The URL of the webpage to scrape.
    :param output_folder: (Optional) The folder where the output files will be saved.
    :return: A Pandas DataFrame containing the scraped data.
    """
    
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    data = {}
    source_name = "bsus"
    today = pendulum.today().date()
    etl_date = today.to_date_string()

    # Check if the request was successful
    if response.status_code == 200:
        
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Locate the table with the specified ID
        table = soup.find('table', {'id': 'tablepress-12'})
        
        # Check if the table was found
        if table:
            # Loop through the rows of the table (skip the header row)
            for row in table.find_all('tr')[1:]:
                # Extract data from each cell in the row
                cells = row.find_all('td')
                
                if len(cells) >= 5:
                    # Extract the specific data you need
                    company_name = cells[1].get_text(strip=True)
                    share_price = cells[2].get_text(strip=True)
                    sector = cells[3].get_text(strip=True)
                    isin = cells[4].get_text(strip=True)
                    special_comment = cells[5].get_text(strip=True)

                    data[company_name] = {"Share Price": share_price,
                                        "Sector": sector,
                                        "ISIN": isin,
                                        "Special Comment": special_comment,
                                        "Source": source_name,
                                        "ETL Date": etl_date
                                        }   
        else:
            print("Table not found on the web page.")
        
        
        # Check if the second table was found
        table = soup.find('table', {'id': 'tablepress-13'})
        if table:
            # Loop through the rows of the table (skip the header row)
            for row in table.find_all('tr')[1:]:
                # Extract data from each cell in the row
                cells = row.find_all('td')
                
                if len(cells) >= 5:
                    # Extract the specific data you need
                    company_name = cells[0].a.get_text(strip=True) if cells[0].a else ""
                    selling_rate = cells[1].get_text(strip=True)
                    sector = cells[3].get_text(strip=True)
                    isin = cells[4].get_text(strip=True)
                    
                    data[company_name] = {"Share Price": selling_rate,
                                        "Sector": sector,
                                        "ISIN": isin,
                                        "Source": source_name,
                                        "ETL Date": etl_date
                                        }
        else:
            print("Table not found on the web page.")
        
    else:
        print("Failed to retrieve the web page. Status code:", response.status_code)
            

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
url = "https://buysellunlistedshares.com/"
_ = scrape_data(url, output_path="data")
