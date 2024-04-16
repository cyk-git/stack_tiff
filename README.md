# stack_tiff
## 使用方法

### 使用已编译的版本
已经编译好了Windows下可以运行的可执行文件，启动stack_tiff.exe即可。虽然有可视化的界面，但也要注意观察其控制台窗口中的信息。

### 运行Python源文件
需要安装tifffile、tqdm两个库，threading和tkinter是Python标准库，一般不需要额外安装
```bash
pip install tifffile
pip install tqdm
```

### 编译Python代码
```bash
pip install pyinstaller
pyinstaller --onedir --noupx stack_tiff.py
```
