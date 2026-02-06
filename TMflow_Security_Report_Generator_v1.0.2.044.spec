# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ui_modular.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['finite_state_reporter', 'finite_state_reporter.core', 'finite_state_reporter.core.reporter', 'requests', 'json', 'datetime', 'os', 'sys', 'threading', 'tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox', 'tkinter.scrolledtext', 'reportlab', 'reportlab.pdfgen', 'reportlab.pdfgen.canvas', 'matplotlib', 'matplotlib.pyplot', 'numpy', 'pandas', 'subprocess', 'tempfile', 'logging', 'collections', 'PIL', 'PIL.Image'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['sklearn', 'scipy', 'tensorflow', 'torch'],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],
    name='TMflow_Security_Report_Generator_v1.0.2.044',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
