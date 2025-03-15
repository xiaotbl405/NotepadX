import sys
import os
import shutil
from tkinter import filedialog, messagebox, simpledialog, colorchooser
from typing import Union

def 选择bat():
    file_path = filedialog.askopenfilename(
    title="选择bat文件",  # 对话框标题
    filetypes=[            # 文件类型过滤器
        ("批处理文件", "*.bat"), 
        ("所有文件", "*.*")
    ],
    initialdir=os.getcwd() # 默认打开当前工作目录
    )
    return file_path if file_path else None

def main():


    try:

        
        # 创建路径对象并验证
        x = 选择bat()
        if not os.path.exists(x):
            messagebox.showerror("错误", f"文件不存在: {os.fspath(x)}")
            return

        # 复制.bat文件到当前目录
        temp_bat = "temp.bat"
        shutil.copyfile(x, temp_bat)

        # 生成打包脚本内容
        y = """
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if __name__ == "__main__":
    try:
        bat_path = resource_path('temp.bat')
        with open(bat_path, 'rb') as f:
            content = f.read()
        with open("temp_executed.bat", 'wb') as f:
            f.write(content)
        os.system("temp_executed.bat")
    except Exception as e:
        print(f"执行错误: {e}")
        input("按回车退出...")
        """
        
        # 写入打包脚本
        with open("1.sec", "w", encoding="utf-8") as f:
            f.write(y)

        # 执行打包命令
        os.system(
            f'pyinstaller --noconsole --onefile '
            f'--add-data "{temp_bat};." '
            f'1.sec'
        )

        # 清理临时文件
        files_to_clean = ["1.sec", temp_bat, "temp_executed.bat"]
        for file in files_to_clean:
            if os.path.exists(file):
                os.remove(file)
        
        messagebox.showinfo("成功", f"已生成可执行文件：{os.path.abspath('dist')}")

    except Exception as e:
        messagebox.showerror("错误", f"处理失败: {str(e)}")

if __name__ == "__main__":
    main()
