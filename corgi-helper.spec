# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['scraper_app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['1_test_KOPS_NOTICE', '2_test_KOPS_ALARM', '3_test_KOPS_INFO', '4_test_KHA_NOTICE', '5_test_KSPS_NOTICE', '6_test_KOSQUA_NOTICE', '7_test_KNAPS_NOTICE', '8_test_KNAPS_NEWS', '9_test_KNAPS_PROMOTION', '10_test_KHAEDU_NOTICE', '11_test_KPMHNA_NOTICE', '12_test_KPMHNA_DATA', '13_test_MEDI_NEWS', '14_test_KDCA_NOTICE', '15_test_KDCA_NEWS'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='corgi-helper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['corgi-helper.ico'],
)
