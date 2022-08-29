# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['Remote-PC (TG).py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['psutil', 'aiotestspeed.aio', 'pyautogui', 'bot_parts'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Remote-PC (TG)',
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
    icon='/media/sneppi/0094C07094C06A2C/Users/racer/AppData/Roaming/Sneppi-PC_bot/remote_pc/sneppi.ico',
)
