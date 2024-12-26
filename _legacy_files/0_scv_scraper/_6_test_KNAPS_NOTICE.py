import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL of the site
base_url = "http://patientsafety.koreanurse.or.kr/announcement"

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
        
        board_list = soup.find('div', class_='board-list')
        if not board_list:
            # print("ERROR: Could not find board-list div")
            return []
            
        items = board_list.find_all('li')
        # print(f"DEBUGGING: Found {len(items)} items")
        
        data = []
        for item in items:
            try:
                date_div = item.find('div', class_='date')
                day = date_div.find('strong', class_='day').text.strip()
                month_year = date_div.find('p').text.strip()
                
                full_date = f"{month_year}.{day}"
                
                title_element = item.find('a', class_='title')
                if title_element:
                    title = title_element.text.strip()
                    # Get the direct URL from href attribute
                    detail_url = title_element.get('href', '')
                else:
                    title = "No title"
                    detail_url = "http://patientsafety.koreanurse.or.kr/announcement"
                
                number = "공지"
                
                data.append([number, title, full_date, detail_url])
                
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
until_date = "2023-01-01"  # Older date

# Update the function call
scraped_data = scrape_all_pages(start_date, until_date)

# Convert to DataFrame with only needed columns
df = pd.DataFrame(scraped_data, columns=["Index", "Title", "Date", "URL"])
# print("\nFirst few rows of data:")
# print(df.head())

# Save to CSV
df.to_csv("scraped_6_knaps_data.csv", index=False, encoding='utf-8-sig')
print("Data saved to scraped_6_knaps_data.csv") 