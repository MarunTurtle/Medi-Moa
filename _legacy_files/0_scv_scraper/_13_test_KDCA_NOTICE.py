import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL of the site
base_url = "https://www.kdca.go.kr/board/board.es"
params = {
    'mid': 'a20504000000',
    'bid': '0014'
}

def extract_data_from_page(page_number):
    # print(f"\nDEBUGGING: Starting extraction for page {page_number}")
    
    # Add page number to parameters
    page_params = params.copy()
    page_params['nPage'] = str(page_number)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    try:
        response = requests.get(base_url, params=page_params, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the content container
        content_div = soup.find('div', class_='dbody')
        if not content_div:
            # print("ERROR: Could not find content container")
            return []
            
        # Get all notice items
        items = content_div.find_all('ul')
        # print(f"DEBUGGING: Found {len(items)} items")
        
        data = []
        for item in items:
            try:
                # Extract elements
                cols = item.find_all('li')
                if len(cols) >= 4:  # Ensure we have all required columns
                    number = cols[0].text.strip()
                    
                    # Get title and URL
                    title_elem = cols[1].find('a')
                    if title_elem:
                        title = title_elem.text.strip()
                        # Extract list_no parameter and construct full URL
                        href = title_elem.get('href', '')
                        if 'list_no=' in href:
                            list_no = href.split('list_no=')[1].split('&')[0]
                            detail_url = f"https://www.kdca.go.kr/board/board.es?mid=a20504000000&bid=0014&act=view&list_no={list_no}"
                        else:
                            detail_url = "https://www.kdca.go.kr/board/board.es?mid=a20504000000&bid=0014"
                    else:
                        title = cols[1].text.strip()
                        detail_url = "https://www.kdca.go.kr/board/board.es?mid=a20504000000&bid=0014"
                    
                    date = cols[3].text.strip()
                    
                    data.append([number, title, date, detail_url])
                    
            except Exception as e:
                continue
                
        return data
        
    except Exception as e:
        # print(f"ERROR: Failed to fetch or parse page: {str(e)}")
        return []

def scrape_all_pages(start_date, until_date):
    all_data = []
    page_number = 1
    seen_notices = set()
    
    # Convert dates to datetime objects
    start_date_dt = pd.to_datetime(start_date)
    until_date_dt = pd.to_datetime(until_date)
    # print(f"\nDEBUGGING Date Range:")
    # print(f"Start date (recent): {start_date_dt}")
    # print(f"Until date (older): {until_date_dt}\n")
    
    while True:
        page_data = extract_data_from_page(page_number)
        if not page_data:
            break
            
        filtered_data = []
        stop_scraping = False
        
        for item in page_data:
            try:
                current_date = pd.to_datetime(item[2])
                
                # Skip if we've gone past the older date
                if current_date < until_date_dt:
                    stop_scraping = True
                    break
                    
                # Skip if we haven't reached the recent date yet
                if current_date > start_date_dt:
                    continue
                    
                # Check for duplicates using title and date
                notice_id = f"{item[1]}_{item[2]}"
                if notice_id not in seen_notices:
                    filtered_data.append(item)
                    seen_notices.add(notice_id)
                    
            except Exception as e:
                # print(f"Error processing date: {item[2]}")
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

# Convert to DataFrame
df = pd.DataFrame(scraped_data, columns=["Index", "Title", "Date", "URL"])
# print("\nFirst few rows of data:")
# print(df.head())

# Save to CSV
df.to_csv("scraped_13_kdca_notice.csv", index=False, encoding='utf-8-sig')
print("Data saved to scraped_13_kdca_notice.csv") 