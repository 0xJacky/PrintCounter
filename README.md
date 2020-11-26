# PrintCounter
Version: 1.1

© 0xJacky 2020

支持在 MacOS 和 Windows 拖拽 Docx、PDF 到主窗口自动计算页数

## 依赖
```
pip3 install -r requirements.txt
```

## 编译
```
pyinstaller main.spec
```

## 已知问题
使用 docx2pdf 库在通过 pyinstaller 打包后程序无法运行

save hook-docx2pdf.py to \lib\site-packages\PyInstaller\hooks
```
from PyInstaller.utils.hooks import collect_all
datas, binaries, hiddenimports = collect_all('docx2pdf')
```
https://github.com/AlJohri/docx2pdf/issues/5#issuecomment-671682876

## TODO
支持 Doc 文件在 Windows 下自动计算页数

## LICENSE
MIT
