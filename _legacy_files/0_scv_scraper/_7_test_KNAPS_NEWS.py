import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta

# Base URL of the site
base_url = "http://patientsafety.koreanurse.or.kr/news"

def extract_data_from_page(page_number):
    # Add page number to URL if needed
    url = f"{base_url}?page={page_number}"
    
    # print("\n" + "="*50)
    # print(f"DEBUGGING: Starting extraction for page {page_number}")
    # print("="*50 + "\n")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        news_list = soup.find('div', class_='promotion-list news')
        if not news_list:
            # print("ERROR: Could not find promotion-list news div")
            return []
            
        items = news_list.find_all('li')
        # print(f"DEBUGGING: Found {len(items)} items")
        
        data = []
        for item in items:
            try:
                text_box = item.find('div', class_='text_box')
                if text_box:
                    title = text_box.find('div', class_='text').text.strip()
                    date = text_box.find('div', class_='date').text.strip()
                    
                    # Get the direct URL from the parent 'a' tag with class 'box'
                    link_element = item.find('a', class_='box')
                    if link_element and 'href' in link_element.attrs:
                        detail_url = link_element['href']
                    else:
                        detail_url = "http://patientsafety.koreanurse.or.kr/news"
                    
                    # Extract number from URL or set as N/A
                    number = detail_url.split('/')[-1] if detail_url != "http://patientsafety.koreanurse.or.kr/news" else "N/A"
                    
                    data.append([number, title, date, detail_url])
                    
            except Exception as e:
                print(f"Error processing item: {str(e)}")
                continue
                
        return data
        
    except Exception as e:
        # print(f"ERROR: Failed to fetch or parse page: {str(e)}")
        return []

def scrape_all_pages(start_date, until_date):
    all_data = []
    page_number = 1
    seen_titles = set()
    
    start_date_dt = pd.to_datetime(start_date)
    until_date_dt = pd.to_datetime(until_date)
    # print(f"\nDEBUGGING Date Range:")
    # print(f"Start date (recent): {start_date_dt}")
    # print(f"Until date (older): {until_date_dt}\n")
    
    while True:
        page_data = extract_data_from_page(page_number)
        if not page_data:
            # print(f"No data found on page {page_number}, stopping...")
            break
        
        filtered_data = []
        stop_scraping = False
        
        for item in page_data:
            title = item[1]
            current_date_str = item[2]
            
            try:
                current_date_dt = pd.to_datetime(current_date_str)
                
                if title in seen_titles:
                    continue
                    
                if current_date_dt < until_date_dt:
                    stop_scraping = True
                    break
                elif until_date_dt <= current_date_dt <= start_date_dt:
                    filtered_data.append(item)
                    seen_titles.add(title)
                    
            except Exception as e:
                # print(f"Error processing date: {current_date_str}")
                # print(f"Error details: {str(e)}")
                continue
        
        all_data.extend(filtered_data)
        # print(f"\nTotal records collected so far: {len(all_data)}")
        
        if stop_scraping:
            break
            
        page_number += 1
    
    return all_data

# Update the date parameters
start_date = "2024-12-31"  # More recent date
until_date = "2024-01-01"  # Older date

# Update the function call
scraped_data = scrape_all_pages(start_date, until_date)

# Convert to DataFrame with only needed columns
df = pd.DataFrame(scraped_data, columns=["Index", "Title", "Date", "URL"])
# print("\nFirst few rows of data:")
# print(df.head())

# Save to CSV
df.to_csv("scraped_7_knaps_news.csv", index=False, encoding='utf-8-sig')
print("Data saved to scraped_7_knaps_news.csv") 