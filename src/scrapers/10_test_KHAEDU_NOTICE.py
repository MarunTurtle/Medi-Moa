import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL of the site
base_url = "https://khaedu.or.kr/board/cha_notice"

def extract_data_from_page(page_number):
    # print(f"\nDEBUGGING: Starting extraction for page {page_number}")
    
    # Add page parameter to URL if needed
    url = f"{base_url}?page={page_number}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all list items in the table body
        items = soup.select('ul.default_table_list li.table-body li')
        if not items:
            # print("No items found on page")
            return []
            
        # print(f"DEBUGGING: Found {len(items)} items")
        
        data = []
        for item in items:
            try:
                # Extract number (handle both regular and notice cases)
                number_elem = item.find('span', class_='list_no')
                if number_elem:
                    marker = number_elem.find('span', class_='marker')
                    if marker and '공지' in marker.text:
                        number = '공지'
                    else:
                        number = number_elem.text.strip()
                else:
                    number = "N/A"
                
                # Extract title and URL
                title_elem = item.find('span', class_='lsit_tit').find('a')
                if title_elem:
                    title = title_elem.text.strip()
                    detail_url = title_elem.get('href', '')
                else:
                    title = "N/A"
                    detail_url = "https://khaedu.or.kr/board/cha_notice"
                
                # Extract date
                date_elem = item.find('span', class_='lsit_date')
                date = date_elem.text.strip() if date_elem else "N/A"
                
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
            number = item[0]
            title = item[1]
            current_date_str = item[2]
            
            try:
                current_date_dt = pd.to_datetime(current_date_str)
                
                # Handle notice posts
                if '공지' in number or '알림' in number:
                    notice_id = f"{title}_{current_date_str}"
                    if notice_id not in seen_notices and until_date_dt <= current_date_dt <= start_date_dt:
                        filtered_data.append(item)
                        seen_notices.add(notice_id)
                    continue
                
                # Stop if we've gone past the older date
                if current_date_dt < until_date_dt:
                    stop_scraping = True
                    break
                
                # Include posts between until_date and start_date (inclusive)
                if until_date_dt <= current_date_dt <= start_date_dt:
                    filtered_data.append(item)
                    
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