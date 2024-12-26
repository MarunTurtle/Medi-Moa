import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import webbrowser

# 웹에서 첫 5개의 게시물 제목을 추출하는 함수
def get_titles():
    url = 'https://www.kha.or.kr/impart/notice/list?siteGb=HOME&siteCd=HOME&rMnuGb=IMP&menuIdx=502'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 게시물 제목이 있는 태그들 찾기
    titles = []
    for idx, row in enumerate(soup.find_all('td', class_='subject ellipsis'), start=1):
        title = row.text.strip()
        titles.append(f"{idx}. {title}")
        if idx == 5:  # 첫 5개의 제목만 추출
            break

    return titles

# 버튼 클릭 시 호출되는 함수
def show_titles():
    titles = get_titles()
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "\n".join(titles))

# 웹 브라우저에서 해당 사이트 열기
def open_website():
    webbrowser.open("https://www.kha.or.kr/impart/notice/list?siteGb=HOME&siteCd=HOME&rMnuGb=IMP&menuIdx=502")

# GUI 설정
root = tk.Tk()
root.title("KHA 사이트 첫 5개 게시물 제목 추출기")

# 버튼 및 텍스트 영역 설정
fetch_button = ttk.Button(root, text="첫 5개 게시물 제목 가져오기", command=show_titles)
fetch_button.pack(pady=10)

result_text = tk.Text(root, height=10, width=80)
result_text.pack(pady=10)

open_button = ttk.Button(root, text="웹사이트 열기", command=open_website)
open_button.pack(pady=10)

# 메인 루프 실행
root.mainloop()
