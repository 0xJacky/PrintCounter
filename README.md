# PrintCounter
Version: 1.2

© 0xJacky 2020 - 2021

打印价格计算器

## Features
拖拽文件自动计算页数  
支持文件类型

| |doc|docx|pdf|
|:----:|:----:|:----:|:----:|
|Windows|√|√|√|
|macOS|x|√|√|

## 依赖
```
pip3 install -r requirements.txt
```
### Poppler
#### Windows

Windows users will have to build or download poppler for Windows. I recommend [@oschwartz10612 version](https://github.com/oschwartz10612/poppler-windows/releases/) which is the most up-to-date. You will then have to add the `bin/` folder to [PATH](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/) or use `poppler_path = r"C:\path\to\poppler-xx\bin" as an argument` in `convert_from_path`.

#### Mac
```
brew install poppler
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

## LICENSE
MIT
