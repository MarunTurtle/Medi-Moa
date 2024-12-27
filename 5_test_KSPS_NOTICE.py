import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL of the site with required parameters
base_url = "http://www.patientsafety.kr/index.php"
params = {
    'hCode': 'BOARD',
    'bo_idx': '5',
    'page': 'list'
}

def extract_data_from_page(page_number):
    page_params = params.copy()
    page_params['pg'] = str(page_number)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    
    try:
        response = requests.get(base_url, params=page_params, headers=headers)
        response.encoding = 'utf-8'
    except Exception as e:
        print(f"ERROR: Request failed with exception: {str(e)}")
        return []
    
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if "board_list" not in response.text:
            response.encoding = 'euc-kr'
            soup = BeautifulSoup(response.text, 'html.parser')
        
        table = None
        
        # Method 1: Direct class search
        table = soup.find('table', class_='board_list modify_color')
        
        # Method 2: If Method 1 fails, try finding by partial class
        if not table:
            table = soup.find('table', class_='board_list')
            
        # Method 3: If both fail, try finding by structure
        if not table:
            tables = soup.find_all('table')
            for t in tables:
                if t.find('thead') and t.find('tbody'):
                    table = t
                    break
        
        if not table:
            print("ERROR: Could not find appropriate table")
            return []
        
        tbody = table.find('tbody') if table else None
        if not tbody:
            print("ERROR: Could not find tbody element")
            return []
        
        rows = tbody.find_all('tr') if tbody else []
        
        data = []
        for row in rows:
            try:
                cols = row.find_all('td', recursive=False)
                if len(cols) >= 5:
                    number = cols[0].text.strip()
                    
                    # Get the link element and extract the URL parameters
                    link_element = cols[1].find('a')
                    if link_element:
                        href = link_element.get('href', '')
                        # Extract idx parameter from href
                        idx = href.split('idx=')[1].split('&')[0] if 'idx=' in href else ''
                        # Construct the full URL with all necessary parameters
                        detail_url = f"http://www.patientsafety.kr/index.php?page=view&idx={idx}&hCode=BOARD&bo_idx=5"
                    else:
                        detail_url = "http://www.patientsafety.kr/index.php?hCode=BOARD&bo_idx=5"
                    
                    title_element = cols[1].find('a')
                    title = title_element.text.strip() if title_element else cols[1].text.strip()
                    date = cols[4].text.strip()
                    
                    data.append([number, title, date, detail_url])
                    
            except Exception as e:
                print(f"Error processing row: {str(e)}")
                continue
                
        return data
        
    except Exception as e:
        print(f"ERROR: HTML parsing failed with exception: {str(e)}")
        return []

def scrape_all_pages(start_date, until_date):
    all_data = []
    page_number = 1
    seen_notices = set()
    
    # Convert dates to datetime objects for comparison
    start_date_dt = pd.to_datetime(start_date)
    until_date_dt = pd.to_datetime(until_date)
    
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
                elif until_date_dt <= current_date_dt <= start_date_dt:
                    filtered_data.append(item)
                    
            except Exception as e:
                print(f"Error processing date: {current_date_str}")
                print(f"Error details: {str(e)}")
                continue
        
        all_data.extend(filtered_data)
        
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