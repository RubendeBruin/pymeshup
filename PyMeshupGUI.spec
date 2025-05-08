# -*- mode: python ; coding: utf-8 -*-


from PyInstaller.utils.hooks import collect_all

datas = [('src/pymeshup/gui/examples','examples')]
binaries = []

hiddenimports = ["vtkmodules.vtkCommonMath",
                 "vtkmodules.vtkCommonTransforms",
                 "vtkmodules.vtkCommonExecutionModel",
                 "vtkmodules.vtkIOCore",
                 "vtkmodules.vtkRenderingCore",
                 "vtkmodules.vtkFiltersCore",
                 "vtkmodules.vtkCommonMisc",
                 "vtkmodules.vtkRenderingVolumeOpenGL2",
                 "vtkmodules.vtkImagingMath",
				 "vtkmodules.all",
				 # ----- capytaine
				 'numpy',
                 'logging',
                 'capytaine',
                 'matplotlib',
                 'scipy',
                 'capytaine.green_functions',
                 'capytaine.green_functions.libs',
                 'capytaine.green_functions.libs.Delhommeau_float64',
                 'capytaine.green_functions.libs.Delhommeau_float32',
                 'capytaine.green_functions.libs.XieDelhommeau_float64',
                 'capytaine.green_functions.libs.XieDelhommeau_float32',
                 # ---------------
                 'OCP',
                 'casadi',
                 'casadi._casadi',
                  ]


tmp_ret = collect_all('pymeshlab')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

block_cipher = None

hookconfig = dict()
hookconfig['matplotlib'] = {"backends":"QtAgg"}  # Needed ???


a = Analysis(
    ['PyMeshupGUI.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig=hookconfig,
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
    [],
    exclude_binaries=True,
    name='PyMeshupGUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PyMeshupGUI',
)

print('==================================================================================)
print('==================================================================================)
print('copy-paste the origin (site-packages) casadi folder into the _internal folder')
print('==================================================================================)
print('==================================================================================)
