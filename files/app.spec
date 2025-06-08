# -*- mode: python ; coding: utf-8 -*-
import os
import glob
from PyInstaller.utils.hooks import (
    get_package_paths,
    collect_submodules,
    collect_data_files,
    collect_dynamic_libs,
    copy_metadata  # ✅ 舊版用這個
)

# ✅ 替代 collect_metadata：收集 transformers 與 tqdm 的 metadata
datas = ( copy_metadata('tqdm') +
    copy_metadata('transformers') +
    copy_metadata('regex') +
    copy_metadata('requests') +
    copy_metadata('filelock') +
    copy_metadata('numpy') +
    copy_metadata('packaging') +
    copy_metadata('huggingface_hub') +
    copy_metadata('pydantic') +
    copy_metadata('pyzbar') +
    copy_metadata('pylibdmtx') +
    copy_metadata('tokenizers') +  # transformers 子模組之一
    copy_metadata('safetensors') )



    
site_packages_path = get_package_paths("transformers")[1]  # 取 transformers 所在的 site-packages 路徑
metadata_dirs = glob.glob(os.path.join(site_packages_path, '*.dist-info'))
datas += [(d, '.') for d in metadata_dirs]


# ✅ 收集 pydantic 所有子模組
hiddenimports = ['pydantic.fields', 'tqdm'] + collect_submodules('pydantic')

# ✅ 加入資料檔（等同 --add-data ".;."）
datas += [('.', '.')]

# ✅ 加入 pyzbar 與 pylibdmtx 的 DLLs
binaries = [
    ('C:/Users/Daniel/.conda/envs/leda/Lib/site-packages/pyzbar/libiconv.dll', '.'),
    ('C:/Users/Daniel/.conda/envs/leda/Lib/site-packages/pyzbar/libzbar-64.dll', '.'),
]

# ✅ 加入整個 pyzbar 和 pylibdmtx 資料夾的 DLL（若有需要）
binaries += collect_dynamic_libs('pyzbar')
binaries += collect_dynamic_libs('pylibdmtx')

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=False,
    name='leda_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True  # 改 False 可以關閉終端視窗
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='leda_app',
)
