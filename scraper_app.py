import flet as ft
import pandas as pd
from datetime import datetime, timedelta
import importlib
import sys
import os

# Import all scraper modules
scraper_modules = {
    "KOPS 공지사항": "1_test_KOPS_NOTICE",
    "KOPS 정보제공지": "2_test_KOPS_INFO",
    "대한병원협회 공지사항": "3_test_KHA_NOTICE",
    "대한환자안전학회 공지사항": "4_test_KSPS_NOTICE",
    "한국의료질향상학회 공지사항": "5_test_KOSQUA_NOTICE",
    "지역환자안전센터 공지사항": "6_test_KNAPS_NOTICE",
    "지역환자안전센터 소식지": "7_test_KNAPS_NEWS",
    "지역환자안전센터 교육행사": "8_test_KNAPS_PROMOTION",
    "대한병원협회교육 공지사항": "9_test_KHAEDU_NOTICE",
    "정신간호사회 공지사항": "10_test_KPMHNA_NOTICE",
    "정신간호사회 자료실": "11_test_KPMHNA_DATA",
    "의료&복지 뉴스": "12_test_MEDI_NEWS",
    "질병관리청 공지사항": "13_test_KDCA_NOTICE",
    "질병관리청 보도자료": "14_test_KDCA_NEWS"
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
    
    # Move loading_text definition to the top of main
    loading_text = ft.Text(
        "검색중...",
        size=16,
        color="blue",
        weight=ft.FontWeight.BOLD,
        visible=False,
    )

    # Create status container after loading_text is defined
    status_container = ft.Container(
        content=ft.Column(
            controls=[
                loading_text,
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
            ft.DataColumn(ft.Text("사이트", size=13, weight=ft.FontWeight.W_500)),
            ft.DataColumn(ft.Text("번호", size=13, weight=ft.FontWeight.W_500)),
            ft.DataColumn(ft.Text("제목", size=13, weight=ft.FontWeight.W_500)),
            ft.DataColumn(ft.Text("날짜", size=13, weight=ft.FontWeight.W_500)),
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
    page.window.width = 1500
    page.window.height = 1000
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
            results_view.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("")),  # Site column
                        ft.DataCell(ft.Text("")),  # Number column
                        ft.DataCell(ft.Text("웹사이트를 선택해주세요", color="red")),  # Title column
                        ft.DataCell(ft.Text(""))   # Date column
                    ]
                )
            )
            results_view.visible = True
            page.update()
            return
        
        results_view.visible = True
        all_scraped_data = []
        
        try:
            loading_text.visible = True
            status_container.content.controls[1].value = ""
            scrape_button.disabled = True
            page.update()
            
            for site in selected_sites:
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
                    results_view.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("")),  # Site column
                                ft.DataCell(ft.Text(error_message, color="red")),
                                ft.DataCell(ft.Text("")),
                                ft.DataCell(ft.Text("")),
                                ft.DataCell(ft.Text(""))
                            ]
                        )
                    )
                    page.update()
                    return

                # Add site name to each scraped item
                site_data = module.scrape_all_pages(start_date, until_date)
                for item in site_data:
                    # Convert item to tuple if it's a list
                    item_tuple = tuple(item) if isinstance(item, list) else item
                    # Create new tuple with site name as first element
                    all_scraped_data.append((site,) + item_tuple)
            
            # Sort combined results by date
            all_scraped_data.sort(key=lambda x: pd.to_datetime(x[3]), reverse=True)
            show_results(all_scraped_data)
            
        except Exception as e:
            results_view.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("")),  # Site column
                        ft.DataCell(ft.Text(f"오류가 발생했습니다: {str(e)}", color="red")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text(""))
                    ]
                )
            )
        
        loading_text.visible = False
        scrape_button.disabled = False
        page.update()

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
        page.update()

    def show_results(data):
        results_view.rows.clear()
        
        status_container.content.controls[1].value = f"총 {len(data)}개의 결과를 찾았습니다." if data else ""
        
        if not data:
            results_view.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("")),          # Site column
                        ft.DataCell(ft.Text("")),          # Number column
                        ft.DataCell(ft.Text("검색 결과가 없습니다.", size=12)),  # Title column
                        ft.DataCell(ft.Text(""))           # Date column
                    ]
                )
            )
            page.update()
            return
        
        for item in data:
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(item[0], size=12)),  # Site name
                    ft.DataCell(ft.Text(str(item[1]), size=12)),  # Number
                    ft.DataCell(
                        content=ft.TextButton(
                            text=item[2],
                            url=item[4],
                            style=ft.ButtonStyle(
                                color={
                                    ft.ControlState.DEFAULT: ft.Colors.BLUE_600,  # Updated to ft.Colors
                                    ft.ControlState.HOVERED: ft.Colors.BLUE_800,  # Updated to ft.Colors
                                },
                                padding=10,
                            ),
                            tooltip=item[4],
                        ),
                    ),
                    ft.DataCell(ft.Text(str(item[3]), size=12)),  # Date
                ]
            )
            results_view.rows.append(row)
        
        page.update()

if __name__ == "__main__":
    ft.app(target=main) 