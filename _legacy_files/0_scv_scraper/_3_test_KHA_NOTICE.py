import requests
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
import concurrent.futures
from functools import lru_cache
from tqdm import tqdm
from datetime import datetime, timedelta

# Create a session for better performance
session = requests.Session()

# Base URL of the site
base_url = "https://www.kha.or.kr/impart/notice/list"

@lru_cache(maxsize=1000)
def parse_date(date_str):
    return pd.to_datetime(date_str)

def extract_data_from_page(page_number):
    params = {'page': page_number}
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find('table', class_='board_list')
    if not table:
        return []
    
    rows = table.find_all('tr')[1:]  # Skip header
    if not rows:
        return []
    
    # Get first and last dates of the page for quick check
    try:
        first_row_date = pd.to_datetime(rows[0].find_all('td', recursive=False)[8].text.strip())
        last_row_date = pd.to_datetime(rows[-1].find_all('td', recursive=False)[8].text.strip())
        page_date_range = {'first': first_row_date, 'last': last_row_date}
    except Exception as e:
        print(f"Error getting page date range: {str(e)}")
        return []
    
    data = []
    for row in rows:
        try:
            cols = row.find_all('td', recursive=False)
            if len(cols) >= 11:
                number = cols[0].text.strip()
                title = cols[4].text.strip()
                date = cols[8].text.strip()
                
                # Just use the main notice board URL
                detail_url = "https://www.kha.or.kr/impart/notice/list"
                
                data.append([number, title, date, detail_url])
        except Exception as e:
            print(f"Error processing row: {str(e)}")
            continue
    
    return {'data': data, 'date_range': page_date_range}

def scrape_all_pages(start_date, until_date):
    all_data = []
    page_number = 1
    seen_notices = set()
    
    start_date_dt = pd.to_datetime(start_date)
    until_date_dt = pd.to_datetime(until_date)
    # print(f"\nDEBUGGING Date Range:")
    # print(f"Start date (recent): {start_date_dt}")
    # print(f"Until date (older): {until_date_dt}\n")
    
    # First, find the starting page (where last row date >= start_date)
    while True:
        page_result = extract_data_from_page(page_number)
        if not page_result:
            break
            
        page_last_date = page_result['date_range']['last']
        # print(f"\nChecking page {page_number} - Last date: {page_last_date}")
        
        if page_last_date >= start_date_dt:
            page_number += 1
        else:
            page_number -= 1  # Go back to last valid page
            break
    
    # print(f"\nStarting collection from page {page_number}")
    
    # Now collect data until we hit the until_date
    while True:
        page_result = extract_data_from_page(page_number)
        if not page_result:
            break
            
        page_first_date = page_result['date_range']['first']
        page_last_date = page_result['date_range']['last']
        
        # print(f"\nProcessing page {page_number}")
        # print(f"Page date range: {page_last_date} to {page_first_date}")
        
        # Skip page if it's completely outside our date range
        if page_first_date < until_date_dt:
            # print(f"Reached date {page_first_date} which is before until_date {until_date}. Stopping...")
            # print("Stopping scraping as we've reached the target date range.")
            break
        
        if page_last_date > start_date_dt:
            # print("Page is after start_date - skipping")
            page_number += 1
            continue
        
        # Process page data
        for item in page_result['data']:
            number = item[0]
            title = item[1]
            current_date = pd.to_datetime(item[2])
            
            # Handle notice posts
            if '공지' in number:
                notice_id = f"{title}_{current_date}"
                if notice_id not in seen_notices:
                    all_data.append(item)
                    seen_notices.add(notice_id)
                continue
            
            # Check if date is in range
            if until_date_dt <= current_date <= start_date_dt:
                all_data.append(item)
        
        # print(f"Total records collected: {len(all_data)}")
        page_number += 1
    
    return all_data

# Update the date parameters
start_date = "2024-12-31"  # More recent date
until_date = "2024-11-30"  # Older date

# Update the function call
scraped_data = scrape_all_pages(start_date, until_date)

# Convert to DataFrame with only needed columns
df = pd.DataFrame(scraped_data, columns=["Index", "Title", "Date", "URL"])

# Save to CSV
df.to_csv("scraped_3_kha_data.csv", index=False, encoding='utf-8-sig')
print("Data saved to scraped_3_kha_data.csv")