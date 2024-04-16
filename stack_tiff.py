import tifffile
import os
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from threading import Thread

def create_multiframe_tiff(start_frame, end_frame, tiff_dir, output_dir, output_file_name , auto_split_number = 0, use_bigtiff=True):
    """
    将指定范围的单帧 TIFF 图片合并为一个或多个 TIFF 文件，并显示进度条。
    当 TIFF 文件大小接近 4GB 时，如果未使用 BigTIFF，则会分割存储到新的文件中。
    
    参数:
        start_frame (int): 起始帧号。
        end_frame (int): 结束帧号。
        tiff_dir (str): 包含 TIFF 文件的文件夹路径。
        output_dir (str): 输出文件夹路径。
        output_file_name (str): 输出文件名(不含后缀)。
        auto_split_number (int): 自动分割的帧数，如果为 0 则不分割。
        use_bigtiff (bool): 是否使用 BigTIFF 格式，如果否，则在文件达到 4GB 时分割。
    """
    max_size = 4 * 1024**3 - 1024**2  # 4GB 的字节数, 保留 1MB 的冗余
    current_size = 0
    file_index = 0
    frame_index = 0
    frame_count = end_frame - start_frame + 1

    def open_new_file():
        nonlocal current_size, tiff_writer, file_index
        if tiff_writer:
            tiff_writer.close()
        current_file = os.path.join(output_dir, f"{output_file_name}_{file_index}.tif")
        tiff_writer = tifffile.TiffWriter(current_file, bigtiff=use_bigtiff)
        file_index += 1
        current_size = 0
        return current_file
    
    tiff_writer = None
    # open_new_file()  # 初始化第一个文件

    for frame_number in tqdm(range(start_frame, end_frame + 1), total=frame_count, desc="Processing frames",unit = "frames"):
        file_name = os.path.join(tiff_dir, f"{frame_number:08d}.tif")
        if os.path.exists(file_name):
            image = tifffile.imread(file_name)
            image_size = image.nbytes  # 估算图像大小
            if (not use_bigtiff and current_size + image_size > max_size) or (frame_index==0) or (auto_split_number > 0 and frame_index % auto_split_number == 0):
                open_new_file()  # 开启新文件
            tiff_writer.write(image)
            current_size += image_size
        else:
            tqdm.write(f"文件 {file_name} 不存在，跳过此帧。")
        frame_index += 1

    if tiff_writer:
        tiff_writer.close()

    print(f"多帧 TIFF 文件处理完成。")

# # 使用示例
# create_multiframe_tiff(start_frame=0, 
#                        end_frame = 7999,
#                        tiff_dir= r"C:\Experiment\Experiment_2023-07-19_13-20-02\0_Camera-A_Fake Master", 
#                        output_dir = r"C:\Experiment\Experiment_2023-07-19_13-20-02\0_Camera-A_Fake Master\output",
#                        output_file_name = "output",
#                        auto_split_number = 2000,
#                        use_bigtiff = False)
def run_tiff_creation(start_frame, end_frame, folder_path, output_path, auto_split_number, auto_split_on, use_bigtiff):
    try:
        output_dir, output_file = os.path.split(output_path)
        output_file_name, _ = os.path.splitext(output_file)
        create_multiframe_tiff(int(start_frame), int(end_frame), folder_path, output_dir,output_file_name, (auto_split_number if auto_split_on else 0), use_bigtiff)
        messagebox.showinfo("成功", "TIFF 文件已成功生成！")
    except Exception as e:
        messagebox.showerror("错误", str(e))

# 创建主窗口
print("创建主窗口中……")
root = tk.Tk()
root.title("TIFF 合并工具")
# 设置网格的权重，使得网格中的某些行和列能够随窗口大小变化而伸缩
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=2)
root.grid_columnconfigure(2, weight=0)
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)
root.grid_rowconfigure(4, weight=0)
root.grid_rowconfigure(5, weight=0)
root.grid_rowconfigure(6, weight=1)

# 按钮回调函数
def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, folder)

def browse_output():
    file = filedialog.asksaveasfilename(defaultextension=".tif", filetypes=[("TIFF files", "*.tif")])
    if file:
        output_path_entry.delete(0, tk.END)
        output_path_entry.insert(0, file)

print("创建窗口控件中……")
# 布局
tk.Label(root, text="起始帧号:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
start_frame_entry_var = tk.IntVar()
start_frame_entry_var.set(0)
start_frame_entry = tk.Entry(root,textvariable=start_frame_entry_var)
start_frame_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
tk.Label(root, text="请使用文件名对应帧号").grid(row=0, column=2, sticky="e", padx=5, pady=5)

tk.Label(root, text="结束帧号:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
end_frame_entry_var = tk.IntVar()
end_frame_entry_var.set(3999)
end_frame_entry = tk.Entry(root,textvariable=end_frame_entry_var)
end_frame_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
tk.Label(root, text="请使用文件名对应帧号").grid(row=1, column=2, sticky="e", padx=5, pady=5)

tk.Label(root, text="输入文件夹路径:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
folder_path_entry = tk.Entry(root)
folder_path_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
folder_browse_button = tk.Button(root, text="浏览...", command=browse_folder)
folder_browse_button.grid(row=2, column=2, sticky="ew", padx=5)

tk.Label(root, text="输出文件路径:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
output_path_entry = tk.Entry(root)
output_path_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
output_browse_button = tk.Button(root, text="浏览...", command=browse_output)
output_browse_button.grid(row=3, column=2, sticky="ew", padx=5)

tk.Label(root, text="自动分割:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
auto_split_entry_var = tk.IntVar()
auto_split_entry_var.set(2000)
auto_split_entry = tk.Entry(root,textvariable=auto_split_entry_var)
auto_split_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
auto_split_on_var = tk.BooleanVar(value=True)
auto_split_on_checkbutton = tk.Checkbutton(root, text="启用", variable=auto_split_on_var)
auto_split_on_checkbutton .grid(row=4, column=2, columnspan=2, sticky="w", pady=5)

# BigTIFF 选择
use_bigtiff_var = tk.BooleanVar(value=False)
bigtiff_checkbutton = tk.Checkbutton(root, text="允许Tiff大于4GB（使用BigTiff格式）", variable=use_bigtiff_var)
bigtiff_checkbutton.grid(row=5, column=1, columnspan=2, sticky="w", pady=5)


def on_run_clicked():
    thread = Thread(target=run_tiff_creation, args=(
        start_frame_entry_var.get(),
        end_frame_entry_var.get(),
        folder_path_entry.get(),
        output_path_entry.get(),
        auto_split_entry_var.get(),
        auto_split_on_var.get(),
        use_bigtiff_var.get()
    ))
    thread.start()

run_button = tk.Button(root, text="生成 TIFF", command=on_run_clicked)
run_button.grid(row=5, column=0, sticky="ew", padx=5, pady=5)

print("调整窗口设置中……")
# 显示窗口并立即更新
root.update_idletasks()  # 强制更新窗口状态

# 获取当前窗口大小并设置为最小尺寸
current_width = root.winfo_width()
current_height = root.winfo_height()
root.minsize(current_width, current_height)
root.maxsize(root.winfo_screenwidth(), root.winfo_height())

print("欢迎使用！")
root.mainloop()
