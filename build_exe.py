import PyInstaller.__main__
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# List all Python files that need to be included
python_files = [
    "scraper_app.py",  # Main file
    "1_test_KOPS_NOTICE.py",
    "2_test_KOPS_ALARM.py",
    "3_test_KOPS_INFO.py",
    "4_test_KHA_NOTICE.py",
    "5_test_KSPS_NOTICE.py",
    "6_test_KOSQUA_NOTICE.py",
    "7_test_KNAPS_NOTICE.py",
    "8_test_KNAPS_NEWS.py",
    "9_test_KNAPS_PROMOTION.py",
    "10_test_KHAEDU_NOTICE.py",
    "11_test_KPMHNA_NOTICE.py",
    "12_test_KPMHNA_DATA.py",
    "13_test_MEDI_NEWS.py",
    "14_test_KDCA_NOTICE.py",
    "15_test_KDCA_NEWS.py"
]

# Create the PyInstaller command
command = [
    'scraper_app.py',  # Main script
    '--onefile',  # Create a single executable
    '--noconsole',  # Don't show console window
    '--name=corgi-helper',  # Name of the executable
    '--icon=corgi-helper.ico',  # Use the corgi icon
]

# Add all Python files as hidden imports
for file in python_files[1:]:  # Skip the main file
    module_name = os.path.splitext(file)[0]
    command.extend(['--hidden-import', module_name])

# Run PyInstaller
PyInstaller.__main__.run(command) 