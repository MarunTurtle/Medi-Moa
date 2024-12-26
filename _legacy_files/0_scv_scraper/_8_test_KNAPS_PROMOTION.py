import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL of the site
base_url = "http://patientsafety.koreanurse.or.kr/promotion"

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
        
        promotion_list = soup.find('div', class_='promotion-list')
        if not promotion_list:
            # print("ERROR: Could not find promotion-list div")
            return []
            
        items = promotion_list.find_all('li')
        # print(f"DEBUGGING: Found {len(items)} items")
        
        data = []
        for item in items:
            try:
                text_box = item.find('div', class_='text_box')
                if text_box:
                    title = text_box.find('div', class_='text').text.strip()
                    date_range = text_box.find('div', class_='date').text.strip()
                    
                    # Get the direct URL from the parent 'a' tag with class 'box'
                    link_element = item.find('a', class_='box')
                    if link_element and 'href' in link_element.attrs:
                        detail_url = link_element['href']
                    else:
                        detail_url = "http://patientsafety.koreanurse.or.kr/promotion"
                    
                    # Extract number from URL or set as N/A
                    number = detail_url.split('/')[-1] if detail_url != "http://patientsafety.koreanurse.or.kr/promotion" else "N/A"
                    
                    # Split date range into start and end dates
                    start_date, end_date = date_range.split(' ~ ')
                    
                    data.append([number, title, start_date, end_date, detail_url])
                    
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
            start_date_str = item[2]
            end_date_str = item[3]
            
            try:
                item_start_date = pd.to_datetime(start_date_str)
                item_end_date = pd.to_datetime(end_date_str)
                
                if title in seen_titles:
                    continue
                    
                if (until_date_dt <= item_start_date <= start_date_dt or
                    until_date_dt <= item_end_date <= start_date_dt):
                    filtered_data.append(item)
                    seen_titles.add(title)
                elif item_end_date < until_date_dt:
                    stop_scraping = True
                    break
                    
            except Exception as e:
                # print(f"Error processing dates: {start_date_str} - {end_date_str}")
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

# Convert to DataFrame with combined date format
df = pd.DataFrame(scraped_data, columns=["Index", "Title", "Start_Date", "End_Date", "URL"])
df['Date'] = df['Start_Date'] + ' - ' + df['End_Date']
df = df[["Index", "Title", "Date"]]  # Reorder and keep only needed columns

# Save to CSV
df.to_csv("scraped_8_knaps_promotion.csv", index=False, encoding='utf-8-sig')
print("Data saved to scraped_8_knaps_promotion.csv")