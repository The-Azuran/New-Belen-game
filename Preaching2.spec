# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['preaching/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['preaching', 'preaching.ui', 'preaching.game', 'preaching.models', 'preaching.enums', 'preaching.config', 'preaching.logic', 'preaching.events', 'preaching.names', 'preaching.items'],
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
    name='Preaching2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
