import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL of the site
base_url = "http://www.mediwelfare.com/news/articleList.html"

def extract_data_from_page(page_number):
    # print(f"\nDEBUGGING: Starting extraction for page {page_number}")
    
    # Add page parameter to URL
    params = {
        'page': str(page_number)
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all article rows
        rows = soup.find_all('div', class_='table-row')
        if not rows:
            # print("No rows found on page")
            return []
            
        # print(f"Found {len(rows)} rows")
        data = []
        
        for row in rows:
            try:
                # Extract category (section)
                section = row.find('small', class_='list-section').text.strip('[]')
                
                # Extract title and URL
                title_element = row.find('a', class_='links')
                if title_element:
                    title = title_element.text.strip()
                    # Get the article ID and construct full URL
                    href = title_element.get('href', '')
                    if 'idxno=' in href:
                        article_id = href.split('idxno=')[1]
                        detail_url = f"http://www.mediwelfare.com/news/articleView.html?idxno={article_id}"
                    else:
                        detail_url = "http://www.mediwelfare.com/news/articleList.html"
                else:
                    title = ""
                    detail_url = "http://www.mediwelfare.com/news/articleList.html"
                
                # Extract date and format it
                dated_div = row.find('div', class_='list-dated')
                if dated_div:
                    date = dated_div.text.strip().split('|')[1].strip()
                    date = date.split()[0]  # Remove time part
                else:
                    date = ""
                
                data.append([section, title, date, detail_url])
                
            except Exception as e:
                continue
                
        return data
        
    except Exception as e:
        # print(f"ERROR: Failed to fetch or parse page: {str(e)}")
        return []

def scrape_all_pages(start_date, until_date):
    all_data = []
    page_number = 1
    seen_titles = set()
    
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
                # Parse date from the item
                current_date = pd.to_datetime(item[2])
                
                # Check if we've gone past the date range
                if current_date < until_date_dt:
                    stop_scraping = True
                    break
                    
                # Skip if we haven't reached the date range yet
                if current_date > start_date_dt:
                    continue
                    
                # Use title as unique identifier
                title = item[1]
                if title not in seen_titles:
                    filtered_data.append(item)
                    seen_titles.add(title)
                    
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

# Update DataFrame creation
df = pd.DataFrame(scraped_data, columns=["Index", "Title", "Date", "URL"])

# Save to CSV
df.to_csv("scraped_12_mediwelfare_news.csv", index=False, encoding='utf-8-sig')
print("Data saved to scraped_12_mediwelfare_news.csv")