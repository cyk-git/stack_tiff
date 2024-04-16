# stack_tiff
## 使用方法

### 使用已编译的版本
[Release](https://github.com/cyk-git/stack_tiff/releases)中已经编译好了Windows下可以运行的可执行文件，下载zip文件，解压缩后启动stack_tiff.exe即可。注意该程序虽然有可视化的界面，但也要观察其控制台窗口中的信息。

### 运行Python源文件
需要安装tifffile、tqdm两个库，threading和tkinter是Python标准库，一般不需要额外安装
```bash
pip install tifffile
pip install tqdm
```

### 编译Python代码
Python代码一般不需要编译，但你也可以使用pyinstaller编译代码，让没有Python环境的机器使用。安装和使用pyinstaller的方法如下：
```bash
pip install pyinstaller
pyinstaller --onedir --noupx stack_tiff.py
```
`--onedir`参数表示将编译结果放到一个路径下，相对应的是`--onefile`会把结果放到一个exe文件中，单文件版本执行前会有一定启动延迟
`--noupx`表示不用UPX对文件进行压缩，这样做会使得程序变得很大（毕竟这程序里面几乎自带一个Python环境），但压缩之后会带来一定的启动延迟