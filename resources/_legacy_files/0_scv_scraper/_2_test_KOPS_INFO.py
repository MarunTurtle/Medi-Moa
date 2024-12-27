import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL of the site
base_url = "https://www.kops.or.kr/portal/ifm/infoProvdStdrList.do"

def extract_data_from_page(page_number):
    # print(f"\nDEBUGGING: Starting extraction for page {page_number}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        form_data = {
            'page': str(page_number),
            'menuNo': '200001',
            'boardType': 'BOARD'
        }
        
        response = requests.post(base_url, data=form_data, headers=headers)
        response.raise_for_status()
        
        # print(f"Response status: {response.status_code}")
        # print(f"Response URL: {response.url}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.find('table')
        if not table:
            print("ERROR: Could not find table")
            return []
            
        rows = table.select('tbody tr')
        # print(f"DEBUGGING: Found {len(rows)} rows")
        
        data = []
        for row in rows:
            try:
                number = row.select_one('td:nth-child(1)').text.strip()
                
                # Just use the main info board URL
                detail_url = "https://www.kops.or.kr/portal/ifm/infoProvdStdrList.do"
                
                title_element = row.select_one('td.txt_info p.board_list_title')
                if title_element:
                    title = ' '.join(title_element.stripped_strings)
                else:
                    title = "No title found"
                    
                date = row.select_one('td:nth-child(5)').text.strip().rstrip('.')
                
                data.append([number, title, date, detail_url])
                
            except Exception as e:
                print(f"Error processing row: {str(e)}")
                continue
        
        return data  # Fixed indentation - moved outside the loop
        
    except Exception as e:
        print(f"ERROR: Failed to fetch or parse page: {str(e)}")
        return []

def scrape_all_pages(start_date, until_date):
    all_data = []
    page_number = 1
    seen_items = set()
    
    # Convert dates to datetime objects
    start_date_dt = pd.to_datetime(start_date)
    until_date_dt = pd.to_datetime(until_date)
    # print(f"\nDEBUGGING Date Range:")
    # print(f"Start date (recent): {start_date_dt}")
    # print(f"Until date (older): {until_date_dt}\n")
    
    while True:
        page_data = extract_data_from_page(page_number)
        if not page_data:
            print("No more data found on page")
            break
            
        filtered_data = []
        stop_scraping = False
        
        for item in page_data:
            number = item[0]
            title = item[1]
            current_date_str = item[2]
            
            # Create unique identifier for the item
            item_id = f"{number}_{title}"
            
            # Skip if we've seen this item before
            if item_id in seen_items:
                # print(f"Duplicate item found: {item_id}")
                continue
                
            seen_items.add(item_id)
            
            try:
                current_date_dt = pd.to_datetime(current_date_str)
                
                # Stop if we've gone past the older date
                if current_date_dt < until_date_dt:
                    stop_scraping = True
                    # print(f"Reached date {current_date_str} which is before until_date {until_date}. Stopping...")
                    break
                
                # Include posts between until_date and start_date (inclusive)
                if current_date_dt <= start_date_dt and current_date_dt >= until_date_dt:
                    filtered_data.append(item)
                    # print(f"Added item from date: {current_date_str}")
                    
            except Exception as e:
                print(f"Error processing date: {current_date_str}")
                print(f"Error details: {str(e)}")
                continue
        
        all_data.extend(filtered_data)
        # print(f"\nTotal records collected so far: {len(all_data)}")
        
        if stop_scraping:
            # print("Stopping scraping as we've reached the target date range.")
            break
            
        page_number += 1
    
    return all_data

# Update the date parameters
start_date = "2024-12-31"  # More recent date
until_date = "2023-01-01"  # Older date

# Update the function call
scraped_data = scrape_all_pages(start_date, until_date)

# Convert to DataFrame
df = pd.DataFrame(scraped_data, columns=["Index", "Title", "Date", "Detail URL"])
# print("\nFirst few rows of data:")
# print(df.head())

# Save to CSV
df.to_csv("scraped_2_kops_info.csv", index=False, encoding='utf-8')
print("Data saved to scraped_2_kops_info.csv") 