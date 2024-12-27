import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL of the site
base_url = "https://www.kosqua.net/index.php"
params = {
    'hCode': 'BOARD',
    'bo_idx': '1',
    'page': 'list'
}

def extract_data_from_page(page_number):
    # Add page number to existing parameters
    page_params = params.copy()
    page_params['pg'] = str(page_number)
    
    # print("\n" + "="*50)
    # print(f"DEBUGGING: Starting extraction for page {page_number}")
    # print(f"DEBUGGING: Using URL parameters: {page_params}")
    # print("="*50 + "\n")
    
    # Add headers to mimic a browser and specify encoding
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    
    try:
        # print("DEBUGGING: Attempting to make request...")
        response = requests.get(base_url, params=page_params, headers=headers)
        # print(f"DEBUGGING: Request URL: {response.url}")
        response.encoding = 'utf-8'
        # print(f"DEBUGGING: Response status code: {response.status_code}")
        # print(f"DEBUGGING: Response encoding: {response.encoding}")
    except Exception as e:
        print(f"ERROR: Request failed with exception: {str(e)}")
        return []
    
    try:
        # print("\nDEBUGGING: Parsing HTML with BeautifulSoup...")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table with class 'board_table' (KOSQUA specific)
        table = soup.find('table', class_='board_table')
        
        if not table:
            print("ERROR: Could not find table with class 'board_table'")
            # print("\nDEBUGGING: All tables found:")
            all_tables = soup.find_all('table')
            for i, t in enumerate(all_tables):
                # print(f"\nTable {i}:")
                print(f"Classes: {t.get('class', 'No class')}")
                print(f"First 200 chars: {str(t)[:200]}")
            return []
        
        # Get all rows from tbody
        tbody = table.find('tbody')
        if not tbody:
            print("ERROR: Could not find tbody element")
            return []
        
        rows = tbody.find_all('tr')
        # print(f"\nDEBUGGING: Found {len(rows)} rows in the table")
        
        data = []
        for row in rows:
            try:
                cols = row.find_all('td')
                if len(cols) >= 5:  # KOSQUA table has 5 columns
                    number = cols[0].text.strip()
                    
                    # Get the link element and extract the URL parameters
                    link_element = cols[1].find('a')
                    if link_element:
                        href = link_element.get('href', '')
                        # Extract idx parameter from href
                        idx = href.split('idx=')[1].split('&')[0] if 'idx=' in href else ''
                        # Construct the full URL with all necessary parameters
                        detail_url = f"https://www.kosqua.net/index.php?page=view&idx={idx}&hCode=BOARD&bo_idx=1"
                    else:
                        detail_url = "https://www.kosqua.net/index.php?hCode=BOARD&bo_idx=1"
                    
                    title_element = cols[1].find('a')
                    title = title_element.text.strip() if title_element else cols[1].text.strip()
                    date = cols[3].text.strip()
                    
                    data.append([number, title, date, detail_url])
                    
            except Exception as e:
                print(f"Error processing row: {str(e)}")
                continue
        
        return data
        
    except Exception as e:
        # print(f"ERROR: HTML parsing failed with exception: {str(e)}")
        return []

def scrape_all_pages(start_date, until_date):
    all_data = []
    page_number = 1
    seen_notices = set()
    
    # Convert dates to datetime objects for comparison
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
        
        # print(f"\nProcessing page {page_number}")
        for item in page_data:
            number = item[0]
            title = item[1]
            current_date_str = item[2]
            
            try:
                current_date_dt = pd.to_datetime(current_date_str)
                # print(f"\nProcessing item: {number}")
                # print(f"Date string: {current_date_str}")
                # print(f"Converted date: {current_date_dt}")
                
                # Handle notice posts
                if '공지' in number or '알림' in number:
                    notice_id = f"{title}_{current_date_str}"
                    if notice_id not in seen_notices and until_date_dt <= current_date_dt <= start_date_dt:
                        filtered_data.append(item)
                        seen_notices.add(notice_id)
                    continue
                
                # print(f"Checking if {until_date_dt} <= {current_date_dt} <= {start_date_dt}")
                
                if current_date_dt < until_date_dt:
                    # print("× Date before until_date - stopping")
                    stop_scraping = True
                    break
                elif until_date_dt <= current_date_dt <= start_date_dt:
                    # print("✓ Date in range - adding to results")
                    filtered_data.append(item)
                else:
                    # print("× Date not in range - skipping")
                    pass
                    
            except Exception as e:
                # print(f"Error processing date: {current_date_str}")
                # print(f"Error details: {str(e)}")
                pass
        
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