# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ui_modular.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['finite_state_reporter', 'finite_state_reporter.core', 'finite_state_reporter.core.reporter', 'finite_state_reporter.pdf', 'finite_state_reporter.pdf.styles', 'finite_state_reporter.pdf.flowables', 'finite_state_reporter.pdf.page_templates', 'finite_state_reporter.pdf.colors', 'reportlab', 'reportlab.pdfgen', 'reportlab.pdfgen.canvas', 'reportlab.lib', 'reportlab.lib.pagesizes', 'reportlab.lib.styles', 'reportlab.lib.units', 'reportlab.lib.colors', 'reportlab.platypus', 'matplotlib', 'matplotlib.pyplot', 'numpy', 'pandas', 'PIL'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['sklearn', 'scipy', 'pytest', 'IPython', 'notebook'],
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
    name='TMflow_Security_Report_Generator_v1.0.2.046',
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
