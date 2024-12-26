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
        
        # print("\nDEBUGGING: First 1000 characters of response:")
        # print(response.text[:1000])
        # print("\nDEBUGGING: Response length:", len(response.text))
        
        if "board_list" not in response.text:
            # print("\nTrying different encoding...")
            response.encoding = 'euc-kr'
            soup = BeautifulSoup(response.text, 'html.parser')
        
        # print("\nDEBUGGING: Looking for table structure...")
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
                    # print("Found table with thead and tbody")
                    table = t
                    break
        
        if table:
            # print("DEBUGGING: Found the table with classes 'board_list modify_color'")
            # print(f"DEBUGGING: Table HTML snippet:\n{str(table)[:200]}...")
            pass
        else:
            print("ERROR: Could not find appropriate table")
            # print("\nDEBUGGING: All tables found:")
            # for i, t in enumerate(all_tables):
            #     print(f"\nTable {i}:")
            #     print(f"Classes: {t.get('class', 'No class')}")
            #     print(f"First 200 chars: {str(t)[:200]}")
            return []
        
        tbody = table.find('tbody') if table else None
        if tbody:
            # print("DEBUGGING: Found tbody element")
            # print(f"DEBUGGING: Number of rows in tbody: {len(tbody.find_all('tr'))}")
            pass
        else:
            print("ERROR: Could not find tbody element")
            return []
        
        rows = tbody.find_all('tr') if tbody else []
        # print(f"\nDEBUGGING: Found {len(rows)} rows in the table")
        
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
        
        # print(f"\nDEBUGGING: Successfully extracted {len(data)} rows of data")
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
                
                if '공지' in number:
                    notice_id = f"{title}_{current_date_str}"
                    if notice_id not in seen_notices:
                        # print("✓ Adding notice post")
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
                print(f"Error processing date: {current_date_str}")
                print(f"Error details: {str(e)}")
                continue
        
        all_data.extend(filtered_data)
        # print(f"\nTotal records collected so far: {len(all_data)}")
        
        if stop_scraping:
            break
            
        page_number += 1
    
    return all_data

# Update the date parameters
start_date = "2024-12-31"  # More recent date
until_date = "2024-12-01"  # Older date

# Update the function call
scraped_data = scrape_all_pages(start_date, until_date)

# Convert to DataFrame with only needed columns
df = pd.DataFrame(scraped_data, columns=["Index", "Title", "Date", "URL"])
# print("\nFirst few rows of data:")
# print(df.head())

# Save to CSV
df.to_csv("scraped_4_ksps_data.csv", index=False, encoding='utf-8-sig')
print("Data saved to scraped_4_ksps_data.csv")