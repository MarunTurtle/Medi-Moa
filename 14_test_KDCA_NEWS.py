import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL of the site
base_url = "https://www.kdca.go.kr/board/board.es"
params = {
    'mid': 'a20501010000',
    'bid': '0015'
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
            
        # Get all news items
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
                            detail_url = f"https://www.kdca.go.kr/board/board.es?mid=a20501010000&bid=0015&act=view&list_no={list_no}"
                        else:
                            detail_url = "https://www.kdca.go.kr/board/board.es?mid=a20501010000&bid=0015"
                    else:
                        title = cols[1].text.strip()
                        detail_url = "https://www.kdca.go.kr/board/board.es?mid=a20501010000&bid=0015"
                    
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
                number = item[0]  # Get the number from the item list
                
                # Handle notice posts
                if '공지' in number or '알림' in number:
                    notice_id = f"{item[1]}_{item[2]}"  # Using title and date as ID
                    if notice_id not in seen_notices and until_date_dt <= current_date <= start_date_dt:
                        filtered_data.append(item)
                        seen_notices.add(notice_id)
                    continue
                    
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

# Test code that only runs when the file is executed directly
if __name__ == "__main__":
    from datetime import datetime, timedelta
    
    # Example date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    # Format dates as strings
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    
    # Test the scraper
    results = scrape_all_pages(end_date_str, start_date_str)
    print(f"Found {len(results)} items") 