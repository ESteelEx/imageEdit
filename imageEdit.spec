# -*- mode: python -*-
a = Analysis(['imageedit.py'],
             pathex=['C:\\Users\\mathiasr\\OneDrive\\imageEdit'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='imageedit.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='imageedit.ico')
