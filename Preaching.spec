# -*- mode: python ; coding: utf-8 -*-
import sys

# Platform-specific icon
if sys.platform == 'win32':
    icon_file = 'assets/icon.ico'
elif sys.platform == 'darwin':
    icon_file = 'assets/icon.icns'
else:
    icon_file = None  # Linux doesn't use embedded icons

a = Analysis(
    ['preaching/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['preaching', 'preaching.enums', 'preaching.config', 'preaching.models', 'preaching.logic', 'preaching.events', 'preaching.ui', 'preaching.names', 'preaching.items', 'preaching.game', 'preaching.dialogue', 'preaching.conversation', 'preaching.reputation', 'preaching.memory', 'preaching.narrative', 'preaching.version', 'preaching.preachers'],
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
    name='Preaching',
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
    icon=icon_file,
)
