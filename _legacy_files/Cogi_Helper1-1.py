import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import requests
from bs4 import BeautifulSoup
import webbrowser
from datetime import datetime, timedelta

# Function to extract posts by date for the first site (KOPS 공지사항)
def extract_posts_by_date(html_content, base_url, start_date=None, end_date=None):
    soup = BeautifulSoup(html_content, 'html.parser')
    posts = []
    page_number = 1

    while True:
        rows = soup.find_all('tr')
        stop_paging = False

        for row in rows:
            title_tag = row.find('p', class_='board_list_title')
            date_tags = row.find_all('td')
            
            if len(date_tags) < 2:
                continue
            
            date_tag = date_tags[-1]
            onclick_attr = row.find('a', href="#none")['onclick']

            try:
                article_id = onclick_attr.split("fnDetail('")[1].split("');")[0]
            except IndexError:
                continue

            link = f"{base_url}{article_id}"

            if title_tag and date_tag and article_id:
                title = title_tag.get_text(strip=True)
                try:
                    post_date = datetime.strptime(date_tag.get_text(strip=True), "%Y.%m.%d").date()
                except ValueError:
                    continue

                if start_date and post_date < start_date:
                    stop_paging = True
                    break

                if (start_date is None or post_date >= start_date) and (end_date is None or post_date <= end_date):
                    posts.append({'title': title, 'date': post_date.strftime("%Y.%m.%d"), 'link': link})

        if stop_paging:
            break

        page_number += 1
        next_page_url = f"{base_url}&page={page_number}"
        response = requests.get(next_page_url)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, 'html.parser')

    return posts


def extract_posts_by_date_new_site(html_content, base_url, start_date=None, end_date=None):
    soup = BeautifulSoup(html_content, 'html.parser')
    posts = []
    page_number = 1

    while True:
        rows = soup.find_all('tr')
        stop_paging = False

        for row in rows:
            columns = row.find_all('td')
            
            if len(columns) < 5:
                continue

            title_tag = columns[2].find('p', class_='board_list_title')
            if not title_tag:
                continue
            
            onclick_attr = columns[2].find('a')['onclick']
            try:
                article_id = onclick_attr.split("fnMoveDetail(")[1].split(")")[0]
            except IndexError:
                continue

            link = f"{base_url}{article_id}"
            title = title_tag.get_text(strip=True)

            date_text = columns[4].get_text(strip=True).strip(".")
            try:
                post_date = datetime.strptime(date_text, "%Y.%m.%d").date()
            except ValueError:
                continue

            if start_date and post_date < start_date:
                stop_paging = True
                break

            if (start_date is None or post_date >= start_date) and (end_date is None or post_date <= end_date):
                posts.append({'title': title, 'date': post_date.strftime("%Y.%m.%d"), 'link': link})

        if stop_paging:
            break

        page_number += 1
        next_page_url = f"{base_url}&page={page_number}"
        response = requests.get(next_page_url)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, 'html.parser')

    return posts


def extract_posts_by_date_kha(html_content, base_url, start_date=None, end_date=None):
    soup = BeautifulSoup(html_content, 'html.parser')
    posts = []
    page_number = 1

    while True:
        rows = soup.find_all('tr')
        stop_paging = False

        for row in rows:
            columns = row.find_all('td')
            
            if len(columns) < 11:
                continue

            title_tag = columns[4].find('a')
            if not title_tag:
                continue
            
            onclick_attr = title_tag['onclick']
            try:
                article_id = onclick_attr.split("fnView('")[1].split("',")[0]
            except IndexError:
                continue

            link = f"{base_url}{article_id}"
            title = title_tag.get_text(strip=True)

            date_text = columns[8].get_text(strip=True)
            try:
                post_date = datetime.strptime(date_text, "%Y-%m-%d").date()
            except ValueError:
                continue

            if start_date and post_date < start_date:
                stop_paging = True
                break

            if (start_date is None or post_date >= start_date) and (end_date is None or post_date <= end_date):
                posts.append({'title': title, 'date': post_date.strftime("%Y-%m-%d"), 'link': link})

        if stop_paging:
            break

        page_number += 1
        next_page_url = f"{base_url}&page={page_number}"
        response = requests.get(next_page_url)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, 'html.parser')

    return posts


# Function to start scraping based on the selected site
def start_scraping_notice(base_url, result_frame, status_label, extractor_func, start_date=None, end_date=None):
    try:
        # Update the status label to "Searching..."
        status_label.config(text="검색 중...", padding=(10, 5))
        result_frame.update_idletasks()  # Force update of the GUI

        response = requests.get(base_url)
        if response.status_code == 200:
            html_content = response.text
            posts = extractor_func(html_content, base_url, start_date, end_date)
            
            for widget in result_frame.winfo_children():
                widget.destroy()
            
            if posts:
                for post in posts:
                    post_frame = ttk.Frame(result_frame)
                    post_frame.pack(fill='x', pady=5)

                    title_label = ttk.Label(post_frame, text=f"제목: {post['title']}", anchor="w")
                    title_label.pack(side="left", padx=5)
                    date_label = ttk.Label(post_frame, text=f"날짜: {post['date']}", anchor="w", width=15)
                    date_label.pack(side="left", padx=5)
                    
                    link_button = ttk.Button(post_frame, text="열기", command=lambda url=post['link']: webbrowser.open(url))
                    link_button.pack(side="right", padx=5)
            else:
                no_post_label = ttk.Label(result_frame, text="해당 기간에 새로운 게시물이 없습니다.", anchor="center")
                no_post_label.pack(fill="x", pady=20)
            
            # Update the status label to "Search Complete"
            status_label.config(text="검색 완료", padding=(10, 5))
        else:
            error_label = ttk.Label(result_frame, text="웹페이지를 불러오지 못했습니다.", anchor="center")
            error_label.pack(fill="x", pady=20)
            status_label.config(text="오류 발생", padding=(10, 5))
    except Exception as e:
        error_label = ttk.Label(result_frame, text=f"오류 발생: {str(e)}", anchor="center")
        error_label.pack(fill="x", pady=20)
        status_label.config(text="오류 발생", padding=(10, 5))

# Function to search today's posts
def search_today_posts(base_url, result_frame, status_label, extractor_func):
    today = datetime.today().date()
    start_scraping_notice(base_url, result_frame, status_label, extractor_func, start_date=today, end_date=today)

# Function to search posts within the last week
def search_weekly_posts(base_url, result_frame, status_label, extractor_func):
    today = datetime.today().date()
    one_week_ago = today - timedelta(days=7)
    start_scraping_notice(base_url, result_frame, status_label, extractor_func, start_date=one_week_ago, end_date=today)

# Function to search posts within a date range
def search_date_range(base_url, start_cal, end_cal, result_frame, status_label, extractor_func):
    start_date = start_cal.get_date()
    end_date = end_cal.get_date()
    start_scraping_notice(base_url, result_frame, status_label, extractor_func, start_date=start_date, end_date=end_date)

# Function to create a site tab
def create_site_tab(notebook, site_name, base_url, extractor_func):
    tab_frame = ttk.Frame(notebook)
    notebook.add(tab_frame, text=site_name)

    # Create status label at the top
    status_label = ttk.Label(tab_frame, text="상태 표시줄", anchor="center", padding=(10, 5))
    status_label.pack(fill="x", padx=10, pady=(10, 0))  # Add padding to separate from top

    # Create date range selection frame below status label
    date_frame = ttk.Frame(tab_frame, padding="10")
    date_frame.pack(fill="x")

    today = datetime.today().date()
    first_day_of_month = today.replace(day=1)

    start_cal = DateEntry(date_frame, width=12, background='darkblue', foreground='white', borderwidth=2, year=first_day_of_month.year, month=first_day_of_month.month, day=first_day_of_month.day)
    start_cal.pack(side="left", padx=5)

    end_cal = DateEntry(date_frame, width=12, background='darkblue', foreground='white', borderwidth=2, year=today.year, month=today.month, day=today.day)
    end_cal.pack(side="left", padx=5)

    search_button = ttk.Button(date_frame, text="검색", command=lambda: search_date_range(base_url, start_cal, end_cal, result_frame, status_label, extractor_func))
    search_button.pack(side="left", padx=5)

    today_button = ttk.Button(date_frame, text="TODAY", command=lambda: search_today_posts(base_url, result_frame, status_label, extractor_func))
    today_button.pack(side="left", padx=5)

    weekly_button = ttk.Button(date_frame, text="Weekly", command=lambda: search_weekly_posts(base_url, result_frame, status_label, extractor_func))
    weekly_button.pack(side="left", padx=5)

    # Create a canvas for the result frame
    canvas = tk.Canvas(tab_frame)
    canvas.pack(side="left", fill="both", expand=True)

    # Add a scrollbar to the canvas
    scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure the canvas to work with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Create a frame inside the canvas for the results
    result_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=result_frame, anchor="nw")

# Create the main window
window = tk.Tk()
window.title("코기_헬퍼")
window.geometry("1280x720")

# Create a notebook for tabs
notebook = ttk.Notebook(window)
notebook.pack(fill='both', expand=True)

# Add site tabs
create_site_tab(notebook, "KOPS 공지사항", "https://www.kops.or.kr/portal/board/kopsNotice/boardList.do", extract_posts_by_date)
create_site_tab(notebook, "KOPS 정보 제공 기준", "https://www.kops.or.kr/portal/ifm/infoProvdStdrList.do", extract_posts_by_date_new_site)
create_site_tab(notebook, "KHA 공지사항", "https://www.kha.or.kr/impart/notice/list?siteGb=HOME&siteCd=HOME&rMnuGb=IMP&menuIdx=502", extract_posts_by_date_kha)

# Run the Tkinter event loop
window.mainloop()
