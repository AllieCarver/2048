# -*- mode: python -*-
a = Analysis(['2048.py'],
             pathex=['/home/killerdigby/python-game-project/2048'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
a.datas += [('README.md', 'README.md', 'DATA')] 
a.datas += [('data/gameover.png', 'data/gameover.png', 'DATA')] 
a.datas += [('data/2048.png', 'data/2048.png', 'DATA')] 
a.datas += [('data/loadscreen.png', 'data/loadscreen.png', 'DATA')] 
a.datas += [('data/win.png', 'data/win.png', 'DATA')]              
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='2048',
          debug=False,
          strip=None,
          upx=True,
          console=True )
