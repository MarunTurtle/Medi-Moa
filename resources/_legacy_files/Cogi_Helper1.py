import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import webbrowser

# Base URLs for different pages on the KOPS site
KOPS_NOTICE_BASE_URL = "https://www.kops.or.kr/portal/board/kopsNotice/boardDetail.do?nttNo="
KOPS_INFO_BASE_URL = "https://www.kops.or.kr/portal/ifm/infoProvdStdrDetail.do?nttNo="

# Function to extract NEW badge posts
def extract_new_badge_posts(html_content, base_url, is_info_page=False):
    soup = BeautifulSoup(html_content, 'html.parser')
    posts = []

    # Find all rows in the table body
    rows = soup.find_all('tr')

    for row in rows:
        # Check if the row has a NEW badge
        new_badge = row.find('span', class_='badge_new')
        if new_badge:
            # Extract the title, date, and ID from onclick attribute
            if is_info_page:
                title_tag = row.find('p', class_='board_list_title')
                date_tag = row.find_all('td')[-1]
                onclick_attr = row.find('a', href="#n")['onclick']
                article_id = onclick_attr.split("fnMoveDetail(")[1].split(")")[0]
            else:
                title_tag = row.find('p', class_='board_list_title')
                date_tag = row.find_all('td')[-1]
                onclick_attr = row.find('a', href="#none")['onclick']
                article_id = onclick_attr.split("fnDetail('")[1].split("');")[0]

            link = f"{base_url}{article_id}"

            if title_tag and date_tag and article_id:
                title = title_tag.get_text(strip=True)
                date = date_tag.get_text(strip=True)
                posts.append({'title': title, 'date': date, 'link': link})

    return posts

# Function to start scraping for "공지사항"
def start_scraping_notice():
    url = 'https://www.kops.or.kr/portal/board/kopsNotice/boardList.do'
    source_label.config(text="환자안전보고학습시스템 (KOPS) - 공지사항")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            new_posts = extract_new_badge_posts(html_content, KOPS_NOTICE_BASE_URL)
            
            # Clear previous results
            for widget in result_frame.winfo_children():
                widget.destroy()
            
            if new_posts:
                for post in new_posts:
                    # Create a frame for each post
                    post_frame = ttk.Frame(result_frame)
                    post_frame.pack(fill='x', pady=5)

                    # Title and Date
                    title_label = ttk.Label(post_frame, text=f"제목: {post['title']}", anchor="w")
                    title_label.pack(side="left", padx=5)
                    date_label = ttk.Label(post_frame, text=f"날짜: {post['date']}", anchor="w", width=15)
                    date_label.pack(side="left", padx=5)
                    
                    # Open Link Button
                    link_button = ttk.Button(post_frame, text="열기", command=lambda url=post['link']: webbrowser.open(url))
                    link_button.pack(side="right", padx=5)
            else:
                no_post_label = ttk.Label(result_frame, text="새로운 게시물이 없습니다.", anchor="center")
                no_post_label.pack(fill="x", pady=20)
        else:
            error_label = ttk.Label(result_frame, text="웹페이지를 불러오지 못했습니다.", anchor="center")
            error_label.pack(fill="x", pady=20)
    except Exception as e:
        error_label = ttk.Label(result_frame, text=f"오류 발생: {str(e)}", anchor="center")
        error_label.pack(fill="x", pady=20)

# Function to start scraping for "정보제공지"
def start_scraping_info():
    url = 'https://www.kops.or.kr/portal/ifm/infoProvdStdrList.do'
    source_label.config(text="환자안전보고학습시스템 (KOPS) - 정보제공지")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            new_posts = extract_new_badge_posts(html_content, KOPS_INFO_BASE_URL, is_info_page=True)
            
            # Clear previous results
            for widget in result_frame.winfo_children():
                widget.destroy()
            
            if new_posts:
                for post in new_posts:
                    # Create a frame for each post
                    post_frame = ttk.Frame(result_frame)
                    post_frame.pack(fill='x', pady=5)

                    # Title and Date
                    title_label = ttk.Label(post_frame, text=f"제목: {post['title']}", anchor="w")
                    title_label.pack(side="left", padx=5)
                    date_label = ttk.Label(post_frame, text=f"날짜: {post['date']}", anchor="w", width=15)
                    date_label.pack(side="left", padx=5)
                    
                    # Open Link Button
                    link_button = ttk.Button(post_frame, text="열기", command=lambda url=post['link']: webbrowser.open(url))
                    link_button.pack(side="right", padx=5)
            else:
                no_post_label = ttk.Label(result_frame, text="새로운 게시물이 없습니다.", anchor="center")
                no_post_label.pack(fill="x", pady=20)
        else:
            error_label = ttk.Label(result_frame, text="웹페이지를 불러오지 못했습니다.", anchor="center")
            error_label.pack(fill="x", pady=20)
    except Exception as e:
        error_label = ttk.Label(result_frame, text=f"오류 발생: {str(e)}", anchor="center")
        error_label.pack(fill="x", pady=20)

# Create the main window
window = tk.Tk()
window.title("코기_헬퍼")
window.geometry("1280x720")

# Add a header to indicate the source
header_frame = ttk.Frame(window, padding="10")
header_frame.pack(fill="x")

source_label = ttk.Label(header_frame, text="환자안전보고학습시스템 (KOPS)", font=("Helvetica", 16))
source_label.pack()

# Create buttons for different sections
button_frame = ttk.Frame(window, padding="10")
button_frame.pack(fill="x")

notice_button = ttk.Button(button_frame, text="공지사항", command=start_scraping_notice)
notice_button.pack(side="left", padx=5)

info_button = ttk.Button(button_frame, text="정보제공지", command=start_scraping_info)
info_button.pack(side="left", padx=5)

# Create a frame to display results
result_frame = ttk.Frame(window, padding="10")
result_frame.pack(pady=10, fill="both", expand=True)

# Run the Tkinter event loop
window.mainloop()
