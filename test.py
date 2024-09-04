import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL of the site
base_url = "https://www.kha.or.kr/impart/notice/list"

# Function to extract data from a single page
def extract_data_from_page(page_number):
    params = {'page': page_number}  # Parameters for pagination
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all the rows in the table
    rows = soup.select('table.board_list tr')[1:]  # Skip the header row
    
    data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 0:
            number = cols[0].text.strip()
            department = cols[2].text.strip()
            title = cols[4].text.strip()
            author = cols[6].text.strip()
            date = cols[8].text.strip()
            views = cols[10].text.strip()

            data.append([number, department, title, author, date, views])
    
    return data

# Function to iterate over all pages until a specified date
def scrape_all_pages(until_date):
    all_data = []
    page_number = 1
    while True:
        page_data = extract_data_from_page(page_number)
        if not page_data:
            break
        
        all_data.extend(page_data)
        
        # Check if the last date on this page is older than the specified date
        last_date = page_data[-1][4]
        if last_date < until_date:
            break
        
        page_number += 1
    
    return all_data

# Define the date you want to scrape until (format: YYYY-MM-DD)
until_date = "2024-08-01"

# Scrape the data
scraped_data = scrape_all_pages(until_date)

# Convert to DataFrame
df = pd.DataFrame(scraped_data, columns=["Number", "Department", "Title", "Author", "Date", "Views"])

# Display the dataframe in the console
print(df)

# Save to CSV (optional)
df.to_csv("scraped_data.csv", index=False)
print("Data saved to scraped_data.csv")
