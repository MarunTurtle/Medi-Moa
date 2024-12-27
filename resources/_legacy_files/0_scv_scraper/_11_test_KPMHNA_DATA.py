import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL of the site
base_url = "https://www.kpmhna.or.kr/sub6/6_1.php"

def extract_data_from_page(page_number):
    # print(f"\nDEBUGGING: Starting extraction for page {page_number}")
    
    # Add page parameter to URL if needed
    params = {
        'page': str(page_number),
        'b_name': 'data_board_2'  # Changed from notice_board
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        
        # Explicitly set the encoding to EUC-KR
        response.encoding = 'euc-kr'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all rows in tbody
        rows = soup.select('tbody tr')
        if not rows:
            # print("No rows found on page")
            return []
            
        # print(f"DEBUGGING: Found {len(rows)} rows")
        
        data = []
        for row in rows:
            try:
                # Extract number
                number_elem = row.select_one('.w_no')
                number = number_elem.text.strip() if number_elem else "N/A"
                
                # Extract title and URL
                title_elem = row.select_one('.w_tit a')
                if title_elem:
                    title = title_elem.text.strip()
                    # Extract number parameter from href and construct full URL
                    href = title_elem.get('href', '')
                    if 'number=' in href:
                        post_number = href.split('number=')[1].split('&')[0]
                        detail_url = f"https://www.kpmhna.or.kr/sub6/6_1.php?mode=view&number={post_number}&b_name=data_board_2"
                    else:
                        detail_url = "https://www.kpmhna.or.kr/sub6/6_1.php"
                else:
                    title = "N/A"
                    detail_url = "https://www.kpmhna.or.kr/sub6/6_1.php"
                
                # Extract date
                date_elem = row.select_one('.w_date')
                date = date_elem.text.strip() if date_elem else "N/A"
                
                data.append([number, title, date, detail_url])
                
            except Exception as e:
                continue
                
        return data
        
    except Exception as e:
        # print(f"ERROR: Failed to fetch or parse page: {str(e)}")
        return []

def scrape_all_pages(start_date, until_date):
    page_number = 1
    all_data = []
    
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
                
                # Stop if we've gone past the older date
                if current_date_dt < until_date_dt:
                    stop_scraping = True
                    # print(f"\nReached date {current_date_str} which is before until_date {until_date}. Stopping...")
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
df.to_csv("scraped_11_kpmhna_data.csv", index=False, encoding='utf-8-sig')
print("Data saved to scraped_11_kpmhna_data.csv") 