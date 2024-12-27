import flet as ft
import pandas as pd
from datetime import datetime, timedelta
import importlib
import sys
import os

# Column width constants
SITE_COL_WIDTH = 65
NUMBER_COL_WIDTH = 40
DATE_COL_WIDTH = 75
TEXT_SIZE = 13
DATA_TEXT_SIZE = 12

# Import all scraper modules
scraper_modules = {
    "KOPS 공지사항": "1_test_KOPS_NOTICE",
    "KOPS 발령": "2_test_KOPS_ALARM",
    "KOPS 정보제공지": "3_test_KOPS_INFO",
    "대한병원협회 공지사항": "4_test_KHA_NOTICE",
    "대한환자안전학회 공지사항": "5_test_KSPS_NOTICE",
    "한국의료질향상학회 공지사항": "6_test_KOSQUA_NOTICE",
    "지역환자안전센터 공지사항": "7_test_KNAPS_NOTICE",
    "지역환자안전센터 소식지": "8_test_KNAPS_NEWS",
    "지역환자안전센터 교육행사": "9_test_KNAPS_PROMOTION",
    "대한병원협회교육 공지사항": "10_test_KHAEDU_NOTICE",
    "정신간호사회 공지사항": "11_test_KPMHNA_NOTICE",
    "정신간호사회 자료실": "12_test_KPMHNA_DATA",
    "의료&복지 뉴스": "13_test_MEDI_NEWS",
    "질병관리청 공지사항": "14_test_KDCA_NOTICE",
    "질병관리청 보도자료": "15_test_KDCA_NEWS"
}

def validate_dates(start_date, until_date):
    try:
        start_dt = pd.to_datetime(start_date)
        until_dt = pd.to_datetime(until_date)
        if start_dt < until_dt:
            return False, "시작일이 종료일보다 늦어야 합니다"
        return True, None
    except Exception:
        return False, "올바른 날짜 형식이 아닙니다 (YYYY-MM-DD)"

def main(page: ft.Page):
    global selected_sites
    selected_sites = set()
    
    # Create status container
    status_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("", size=14, color="grey", weight=ft.FontWeight.BOLD)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5
        ),
        margin=ft.margin.only(top=5, bottom=5)
    )

    # Define results_view at the start
    results_view = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Container(
                    content=ft.Text("사이트", size=TEXT_SIZE, weight=ft.FontWeight.W_500),
                    width=SITE_COL_WIDTH
                )
            ),
            ft.DataColumn(
                ft.Container(
                    content=ft.Text("번호", size=TEXT_SIZE, weight=ft.FontWeight.W_500),
                    width=NUMBER_COL_WIDTH
                )
            ),
            ft.DataColumn(ft.Text("제목", size=TEXT_SIZE, weight=ft.FontWeight.W_500)),  # Responsive
            ft.DataColumn(
                ft.Container(
                    content=ft.Text("날짜", size=TEXT_SIZE, weight=ft.FontWeight.W_500),
                    width=DATE_COL_WIDTH
                )
            ),
        ],
        rows=[],
        visible=False,
        border=ft.border.all(0.5, "0x0F000000"),
        border_radius=10,
        vertical_lines=ft.border.BorderSide(0.5, "0x0F000000"),
        horizontal_lines=ft.border.BorderSide(0.5, "0x0F000000"),
        column_spacing=40,
        heading_row_color=ft.Colors.with_opacity(0.02, ft.Colors.BLACK),  # Very subtle header background
        heading_row_height=50,
        data_row_color={"hovered": "0x0A000000"},
        data_row_min_height=45,
        show_bottom_border=True,
    )
    
    def create_site_checkbox(site_name):
        return ft.Container(
            content=ft.Checkbox(
                label=site_name,
                value=False,
                on_change=lambda e, s=site_name: handle_site_selection(e, s)
            ),
            margin=ft.margin.only(bottom=2, right=5),
            height=30,
            tooltip=site_name
        )

    def handle_select_all(e):
        # Update all checkboxes in the grid
        for control in site_grid.controls:
            if isinstance(control, ft.Container) and isinstance(control.content, ft.Checkbox):
                control.content.value = e.control.value
                if e.control.value:
                    selected_sites.add(control.content.label)
                else:
                    selected_sites.discard(control.content.label)
        page.update()

    def handle_site_selection(e, site_name):
        if e.control.value:
            selected_sites.add(site_name)
        else:
            selected_sites.discard(site_name)
            # Update "Select All" checkbox if any site is unchecked
            select_all_checkbox.value = len(selected_sites) == len(scraper_modules)
        page.update()

    # Create site grid
    site_grid = ft.GridView(
        runs_count=1,
        max_extent=400,
        child_aspect_ratio=3.5,
        spacing=5,
        run_spacing=5,
        controls=[create_site_checkbox(site_name) for site_name in scraper_modules.keys()]
    )

    # Create select all checkbox
    select_all_checkbox = ft.Checkbox(
        label="전체 선택",
        value=False,
        on_change=handle_select_all
    )

    # Update page styling for a cleaner look
    page.title = "의료정보 검색"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.window.width = 1280
    page.window.height = 720
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    
    # Add header text
    header = ft.Text(
        value="의료 MOA",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE,
        text_align=ft.TextAlign.CENTER,
    )

    def on_tab_change(e):
        if date_range_tabs.selected_index == 0:  # 오늘
            today = datetime.now().strftime("%Y-%m-%d")
            start_date_picker.value = today
            until_date_picker.value = today
            custom_date_row.visible = False
        elif date_range_tabs.selected_index == 1:  # 일주일
            today = datetime.now()
            week_ago = (today - timedelta(days=7)).strftime("%Y-%m-%d")
            start_date_picker.value = today.strftime("%Y-%m-%d")
            until_date_picker.value = week_ago
            custom_date_row.visible = False
        else:  # 직접 선택
            custom_date_row.visible = True
        
        start_date_picker.update()
        until_date_picker.update()
        custom_date_row.update()

    # Make date selection more intuitive
    date_range_tabs = ft.Tabs(
        selected_index=0,  # Default to "오늘"
        tabs=[
            ft.Tab(text="오늘"),
            ft.Tab(text="일주일"),
            ft.Tab(text="직접 선택"),
        ],
        height=40,
        on_change=lambda e: on_tab_change(e),
    )

    # Improve date picker styling
    until_date_picker = ft.TextField(
        label="시작일",  # Fixed label
        value=(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
        width=180,
        height=45,
        text_size=16,
        border_radius=8,
        prefix_icon=ft.Icons.CALENDAR_TODAY,
    )
    start_date_picker = ft.TextField(
        label="종료일",  # Fixed label
        value=datetime.now().strftime("%Y-%m-%d"),
        width=180,
        height=45,
        text_size=16,
        border_radius=8,
        prefix_icon=ft.Icons.CALENDAR_TODAY,
    )

    def scrape_data(e):
        clear_results()
        if not selected_sites:
            status_container.content.controls[0].value = "웹사이트를 선택해주세요"
            page.update()
            return
        
        results_view.visible = False  # Hide table while searching
        all_scraped_data = []  # Initialize the list here
        
        try:
            status_container.content.controls[0].value = "검색 중입니다..."
            scrape_button.disabled = True
            page.update()
            
            for site in selected_sites:
                try:
                    module_name = scraper_modules[site]
                    module = importlib.import_module(module_name)
                    
                    if date_range_tabs.selected_index == 0:
                        start_date, until_date = get_date_range("today")
                    elif date_range_tabs.selected_index == 1:
                        start_date, until_date = get_date_range("week")
                    else:
                        start_date = start_date_picker.value
                        until_date = until_date_picker.value

                    is_valid, error_message = validate_dates(start_date, until_date)
                    if not is_valid:
                        status_container.content.controls[0].value = error_message
                        scrape_button.disabled = False
                        page.update()
                        return

                    # Add site name to each scraped item
                    site_data = module.scrape_all_pages(start_date, until_date)
                    if site_data:  # Check if data exists
                        for item in site_data:
                            # Convert item to tuple if it's a list
                            item_tuple = tuple(item) if isinstance(item, list) else item
                            # Create new tuple with site name as first element
                            all_scraped_data.append((site,) + item_tuple)
                except ImportError as ie:
                    status_container.content.controls[0].value = f"모듈을 찾을 수 없습니다: {module_name}"
                    print(f"Import error: {str(ie)}")
                    continue
                except Exception as e:
                    status_container.content.controls[0].value = f"{site} 스크래핑 중 오류 발생: {str(e)}"
                    print(f"Scraping error for {site}: {str(e)}")
                    continue
            
            if all_scraped_data:
                # Sort combined results by date
                try:
                    all_scraped_data.sort(key=lambda x: pd.to_datetime(x[3]), reverse=True)
                    show_results(all_scraped_data)
                except Exception as e:
                    status_container.content.controls[0].value = f"데이터 정렬 중 오류 발생: {str(e)}"
            else:
                status_container.content.controls[0].value = "검색 결과가 없습니다."
            
            scrape_button.disabled = False
            page.update()
            
        except Exception as e:
            status_container.content.controls[0].value = f"오류가 발생했습니다: {str(e)}"
            scrape_button.disabled = False
            page.update()
            return

    # Move button creation after scrape_data function definition
    scrape_button = ft.ElevatedButton(
        text="검색하기",
        on_click=scrape_data,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor={
                ft.ControlState.DEFAULT: ft.Colors.BLUE,
                ft.ControlState.HOVERED: ft.Colors.BLUE_700,
            },
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        height=45,
        width=120,
    )

    custom_date_row = ft.Row(
        [until_date_picker, start_date_picker],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        visible=False  # Hide by default
    )

    # Create left panel for checkboxes (simplified)
    left_panel = ft.Container(
        content=ft.Column([
            select_all_checkbox,
            site_grid
        ]),
        width=100,
        padding=5,
    )

    # Create right panel for search controls and results
    right_panel = ft.Container(
        content=ft.Column([
            # Search controls
            ft.Container(
                content=ft.Column([
                    ft.Row(
                        [date_range_tabs],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    custom_date_row,
                    ft.Row(
                        [scrape_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [status_container],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]),
                padding=0,
            ),
            # Results container with center alignment
            ft.Container(
                content=results_view,
                alignment=ft.alignment.center,
                padding=ft.padding.symmetric(horizontal=0),
            ),
        ]),
        expand=True,
        padding=ft.padding.only(left=120),
    )

    # Update the main layout
    page.add(
        header,
        ft.Row(
            [left_panel, right_panel],
            expand=True,
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.START
        ),
    )

    def get_date_range(range_type):
        today = datetime.now()
        if range_type == "today":
            return today.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")
        elif range_type == "week":
            week_ago = today - timedelta(days=7)
            return today.strftime("%Y-%m-%d"), week_ago.strftime("%Y-%m-%d")
        return None, None

    def create_url_button(url):
        return ft.TextButton(
            text="링크",
            url=url,
            tooltip=url,
            style=ft.ButtonStyle(
                color={
                    ft.ControlState.DEFAULT: ft.Colors.BLUE_600,
                    ft.ControlState.HOVERED: ft.Colors.BLUE_800,
                },
                overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),
                padding=ft.padding.all(10),
            )
        )

    def clear_results():
        results_view.rows.clear()
        results_view.visible = False
        status_container.content.controls[0].value = ""
        page.update()

    def show_results(data):
        try:
            results_view.rows.clear()
            
            if not data:
                status_container.content.controls[0].value = "검색 결과가 없습니다."
                results_view.visible = False
                page.update()
                return
            
            status_container.content.controls[0].value = f"총 {len(data)}개의 결과를 찾았습니다."
            
            for item in data:
                try:
                    row = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Container(content=ft.Text(item[0], size=DATA_TEXT_SIZE), width=SITE_COL_WIDTH)),
                            ft.DataCell(ft.Container(content=ft.Text(str(item[1]), size=DATA_TEXT_SIZE), width=NUMBER_COL_WIDTH)),
                            ft.DataCell(  # Title - responsive
                                content=ft.TextButton(
                                    text=item[2],
                                    url=item[4],
                                    style=ft.ButtonStyle(
                                        color={
                                            ft.ControlState.DEFAULT: ft.Colors.BLUE_600,
                                            ft.ControlState.HOVERED: ft.Colors.BLUE_800,
                                        },
                                        padding=10,
                                    ),
                                    tooltip=item[4],
                                ),
                            ),
                            ft.DataCell(ft.Container(content=ft.Text(str(item[3]), size=DATA_TEXT_SIZE), width=DATE_COL_WIDTH)),
                        ]
                    )
                    results_view.rows.append(row)
                except IndexError as ie:
                    print(f"Data format error for item: {item}")
                    print(f"Index error: {str(ie)}")
                    continue
                except Exception as e:
                    print(f"Error processing row: {str(e)}")
                    continue
            
            results_view.visible = True
            page.update()
            
        except Exception as e:
            status_container.content.controls[0].value = f"결과 표시 중 오류 발생: {str(e)}"
            page.update()

if __name__ == "__main__":
    ft.app(target=main) 