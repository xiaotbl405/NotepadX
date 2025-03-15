import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
import re
from markdown import markdown
import tkinter.font as tkfont
import os
import sys
import threading
def resource_path(relative_path):  
    if hasattr(sys, '_MEIPASS'):  # 打包后路径  
        base_path = sys._MEIPASS  
    else:  # 开发时路径  
        base_path = os.path.abspath(".")  
    return os.path.join(base_path, relative_path) 
class 文本编辑器应用:
    def __init__(self, 主窗口):
        self.主窗口 = 主窗口
        self.主窗口.title("未命名 - Python文本编辑器")
        self.文件路径 = None
        self.文本修改状态 = False
        self.当前模式 = "普通文本"  # 支持：普通文本/Markdown/Python
        self.语法高亮标签 = {
            '标题': {'正则': r'^#+.+', '颜色': '#0066CC'},
            '粗体': {'正则': r'\*\*.+?\*\*', '颜色': '#B22222'},
            '斜体': {'正则': r'\*.+?\*', '颜色': '#228B22'},
            '代码块': {'正则': r'```[\s\S]*?```', '颜色': '#666666'},
            '链接': {'正则': r'$.*?$$.*?$', '颜色': '#0000FF'},
            '注释': {'正则': r'#.*$', '颜色': '#008000'},
            '关键字': {'正则': r'\b(?:def|class|if|else|for|while|import|from|try|except)\b', '颜色': '#0000FF'},
            '字符串': {'正则': r'(\".*?\"|\'.*?\')', '颜色': '#BA2121'}
        }

        # 初始化界面
        self.创建界面组件()
        self.设置菜单栏()
        self.绑定快捷键()
        self.初始化语法高亮()

    def 创建界面组件(self):
        # 主文本区域
        self.文本区域 = tk.Text(self.主窗口, wrap="word", undo=True, font=("等距更纱黑体 SC", 12))
        self.文本区域.pack(expand=True, fill="both")

        # 滚动条
        滚动条 = tk.Scrollbar(self.文本区域)
        滚动条.pack(side="right", fill="y")
        滚动条.config(command=self.文本区域.yview)
        self.文本区域.config(yscrollcommand=滚动条.set)

        # 状态栏
        self.状态栏 = tk.Label(self.主窗口, text="就绪", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.状态栏.pack(side=tk.BOTTOM, fill=tk.X)

        # 绑定文本修改事件
        self.文本区域.bind("<<Modified>>", self.文本修改事件)

    def 设置菜单栏(self):
        菜单栏 = tk.Menu(self.主窗口)

        # 文件菜单
        文件菜单 = tk.Menu(菜单栏, tearoff=0)
        文件菜单.add_command(label="新建", command=self.新建文件, accelerator="Ctrl+N")
        文件菜单.add_command(label="打开...", command=self.打开文件, accelerator="Ctrl+O")
        文件菜单.add_command(label="保存", command=self.保存文件, accelerator="Ctrl+S")
        文件菜单.add_command(label="另存为...", command=self.另存为文件)
        文件菜单.add_separator()
        文件菜单.add_command(label="退出", command=self.退出程序)
        菜单栏.add_cascade(label="文件", menu=文件菜单)

        # 编辑菜单
        编辑菜单 = tk.Menu(菜单栏, tearoff=0)
        编辑菜单.add_command(label="撤销", command=self.撤销操作, accelerator="Ctrl+Z")
        编辑菜单.add_command(label="恢复", command=self.恢复操作, accelerator="Ctrl+Y")
        编辑菜单.add_separator()
        编辑菜单.add_command(label="剪切", command=self.剪切文本, accelerator="Ctrl+X")
        编辑菜单.add_command(label="复制", command=self.复制文本, accelerator="Ctrl+C")
        编辑菜单.add_command(label="粘贴", command=self.粘贴文本, accelerator="Ctrl+V")
        编辑菜单.add_command(label="全选", command=self.全选文本, accelerator="Ctrl+A")
        编辑菜单.add_separator()
        编辑菜单.add_command(label="查找...", command=self.查找文本, accelerator="Ctrl+F")
        菜单栏.add_cascade(label="编辑", menu=编辑菜单)

        # 视图菜单
        视图菜单 = tk.Menu(菜单栏, tearoff=0)
        视图菜单.add_command(label="Markdown预览", command=self.markdown预览)
        视图菜单.add_command(label="切换模式", command=self.切换编辑模式)
        视图菜单.add_separator()
        视图菜单.add_command(label="颜色主题...", command=self.选择颜色主题)
        菜单栏.add_cascade(label="视图", menu=视图菜单)

        # 帮助菜单
        帮助菜单 = tk.Menu(菜单栏, tearoff=0)
        帮助菜单.add_command(label="使用帮助", command=self.显示帮助窗口)
        帮助菜单.add_command(label="关于", command=self.显示关于信息)
        菜单栏.add_cascade(label="帮助", menu=帮助菜单)
        
        # 更多菜单
        更多 = tk.Menu(菜单栏, tearoff=0)
        更多.add_command(label="bat转exe",command=self.bat转exeme)
        更多.add_command(label="vbs转exe",command=self.vbs转exeme)
        菜单栏.add_cascade(label="更多功能",menu=更多)
        

        self.主窗口.config(menu=菜单栏)
    def vbs转exe(self):
        #os.system("python vbstoexe.py")
        ax = resource_path('vbstoexe.exe')
        with open(ax,'rb') as f:
            vbstoexe = f.read()
        with open("vte.exe",'wb') as f:
            f.write(vbstoexe)
        os.system("start vte.exe")
    def vbs转exeme(self):
        thread1 = threading.Thread(target=self.vbs转exe)
        thread1.start()
    def 选择bat(self):
        file_path = filedialog.askopenfilename(
        title="选择bat文件",  # 对话框标题
        filetypes=[            # 文件类型过滤器
            ("批处理文件", "*.bat"), 
            ("所有文件", "*.*")
        ],
        initialdir=os.getcwd() # 默认打开当前工作目录
        )
        return file_path if file_path else None
    def bat转exe(self):
        #bat文件 = self.选择bat()
        #if bat文件:
        ax = resource_path('batoexe.exe')
            #messagebox.showinfo("提示",f"{bat文件}，不懂的确认后继续")
        with open(ax,'rb') as f:
            batoexe = f.read()
        with open("bte.exe",'wb') as f:
            f.write(batoexe)
           # 打包代码 = f'python batoexe.py "{bat文件}"'
            #os.system(打包代码)
        #else:
            #messagebox.showerror("错误", "你尚未选择文件")
        #messagebox.showinfo("提示","运行中")
        os.system("start bte.exe")
        #os.system("python batoexe.py")
    def bat转exeme(self):
        thread = threading.Thread(target=self.bat转exe)
        thread.start()
    def 绑定快捷键(self):
        快捷键组合 = [
            ("<Control-n>", self.新建文件),
            ("<Control-o>", self.打开文件),
            ("<Control-s>", self.保存文件),
            ("<Control-z>", self.撤销操作),
            ("<Control-y>", self.恢复操作),
            ("<Control-x>", self.剪切文本),
            ("<Control-c>", self.复制文本),
            ("<Control-v>", self.粘贴文本),
            ("<Control-a>", self.全选文本),
            ("<Control-f>", self.查找文本),
        ]
        for 组合, 回调 in 快捷键组合:
            self.主窗口.bind_all(组合, lambda e, cb=回调: cb())

    # 文件操作功能
    def 新建文件(self):
        if self.检查是否需要保存():
            self.文本区域.delete(1.0, tk.END)
            self.文件路径 = None
            self.主窗口.title("未命名 - Python文本编辑器")
            self.文本修改状态 = False

    def 打开文件(self):
        if self.检查是否需要保存():
            路径 = filedialog.askopenfilename(filetypes=[
                ("文本文件", "*.txt"),
                ("Markdown文件", "*.md"),
                ("Python文件", "*.py"),
                ("所有文件", "*.*")
            ])
            if 路径:
                try:
                    with open(路径, "r", encoding="utf-8") as 文件:
                        内容 = 文件.read()
                    self.文本区域.delete(1.0, tk.END)
                    self.文本区域.insert(tk.END, 内容)
                    self.文件路径 = 路径
                    self.主窗口.title(f"{路径} - Python文本编辑器")
                    self.文本修改状态 = False
                    self.自动检测文件类型(路径)
                    self.应用语法高亮()
                except Exception as 错误:
                    messagebox.showerror("错误", f"打开文件失败：\n{str(错误)}")

    def 保存文件(self):
        if self.文件路径:
            try:
                内容 = self.文本区域.get(1.0, tk.END)
                with open(self.文件路径, "w", encoding="utf-8") as 文件:
                    文件.write(内容)
                self.文本修改状态 = False
                self.主窗口.title(f"{self.文件路径} - Python文本编辑器")
            except Exception as 错误:
                messagebox.showerror("错误", f"保存文件失败：\n{str(错误)}")
        else:
            self.另存为文件()

    def 另存为文件(self):
        路径 = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("文本文件", "*.txt"),
                ("Markdown文件", "*.md"),
                ("Python文件", "*.py"),
                ("所有文件", "*.*")
            ]
        )
        if 路径:
            self.文件路径 = 路径
            self.保存文件()
            self.自动检测文件类型(路径)

    # 编辑功能
    def 撤销操作(self):
        try:
            self.文本区域.edit_undo()
        except tk.TclError:
            pass

    def 恢复操作(self):
        try:
            self.文本区域.edit_redo()
        except tk.TclError:
            pass

    def 剪切文本(self):
        self.文本区域.event_generate("<<Cut>>")

    def 复制文本(self):
        self.文本区域.event_generate("<<Copy>>")

    def 粘贴文本(self):
        self.文本区域.event_generate("<<Paste>>")

    def 全选文本(self):
        self.文本区域.tag_add(tk.SEL, "1.0", tk.END)
        self.文本区域.mark_set(tk.INSERT, "1.0")
        self.文本区域.see(tk.INSERT)
        return "break"

    # Markdown和语法高亮功能
    def 初始化语法高亮(self):
        # 配置文本标签样式
        默认字体 = tkfont.Font(font=self.文本区域["font"])
        for 标签名称, 样式 in self.语法高亮标签.items():
            self.文本区域.tag_configure(标签名称, 
                                      foreground=样式['颜色'],
                                      font=(默认字体.actual()['family'], 
                                          默认字体.actual()['size'], 
                                          'bold' if 标签名称 == '标题' else 'normal'))

    def 应用语法高亮(self, event=None):
        if self.当前模式 == "普通文本":
            return

        # 清除现有标签
        for 标签 in self.语法高亮标签.keys():
            self.文本区域.tag_remove(标签, "1.0", tk.END)

        内容 = self.文本区域.get("1.0", tk.END)
        
        # 根据当前模式应用高亮规则
        if self.当前模式 == "Markdown":
            for 行号, 行内容 in enumerate(内容.split('\n'), start=1):
                self.处理_markdown行(行号, 行内容)
        elif self.当前模式 == "Python":
            self.处理_python语法(内容)

    def 处理_markdown行(self, 行号, 行内容):
        起始位置 = f"{行号}.0"
        for 标签名称, 配置 in self.语法高亮标签.items():
            if 标签名称 in ['关键字', '注释']:  # 跳过Python专用标签
                continue
            for 匹配 in re.finditer(配置['正则'], 行内容):
                开始 = 匹配.start()
                结束 = 匹配.end()
                self.文本区域.tag_add(标签名称, 
                                    f"{行号}.{开始}", 
                                    f"{行号}.{结束}")

    def 处理_python语法(self, 内容):
        # 处理多行语法（如字符串）
        字符串模式 = re.compile(r'(\'\'\'[\s\S]*?\'\'\'|\"\"\"[\s\S]*?\"\"\"|\'.*?\'|\".*?\")')
        字符串位置 = []
        for 匹配 in 字符串模式.finditer(内容):
            字符串位置.append((匹配.start(), 匹配.end()))
            self.文本区域.tag_add('字符串', 
                                f"1.0 + {匹配.start()} chars", 
                                f"1.0 + {匹配.end()} chars")

        # 处理其他语法元素
        for 匹配 in re.finditer(self.语法高亮标签['关键字']['正则'], 内容):
            if not any(开始 <= 匹配.start() <= 结束 for (开始, 结束) in 字符串位置):
                self.文本区域.tag_add('关键字', 
                                    f"1.0 + {匹配.start()} chars", 
                                    f"1.0 + {匹配.end()} chars")

        for 匹配 in re.finditer(self.语法高亮标签['注释']['正则'], 内容):
            if not any(开始 <= 匹配.start() <= 结束 for (开始, 结束) in 字符串位置):
                self.文本区域.tag_add('注释', 
                                    f"1.0 + {匹配.start()} chars", 
                                    f"1.0 + {匹配.end()} chars")

    def markdown预览(self):
        预览窗口 = tk.Toplevel(self.主窗口)
        预览窗口.title("Markdown预览")
        预览文本 = tk.Text(预览窗口, wrap="word", state=tk.DISABLED)
        预览文本.pack(expand=True, fill="both")

        html内容 = markdown(self.文本区域.get(1.0, tk.END))
        预览文本.config(state=tk.NORMAL)
        预览文本.delete(1.0, tk.END)
        预览文本.insert(tk.END, html内容)
        预览文本.config(state=tk.DISABLED)

    # 其他功能
    def 切换编辑模式(self):
        模式选项 = ["普通文本", "Markdown", "Python"]
        当前索引 = 模式选项.index(self.当前模式)
        新索引 = (当前索引 + 1) % len(模式选项)
        self.当前模式 = 模式选项[新索引]
        self.状态栏.config(text=f"当前模式：{self.当前模式}")
        self.应用语法高亮()

    def 自动检测文件类型(self, 文件路径):
        if 文件路径.endswith('.md'):
            self.当前模式 = "Markdown"
        elif 文件路径.endswith('.py'):
            self.当前模式 = "Python"
        else:
            self.当前模式 = "普通文本"
        self.状态栏.config(text=f"当前模式：{self.当前模式}")

    def 选择颜色主题(self):
        颜色 = colorchooser.askcolor(title="选择颜色主题")
        if 颜色:
            self.文本区域.config(bg=颜色, insertbackground='black')

    def 查找文本(self):
        查找内容 = simpledialog.askstring("查找", "输入要查找的内容：")
        if 查找内容:
            起始位置 = self.文本区域.search(查找内容, "1.0", stopindex=tk.END, nocase=True)
            if 起始位置:
                结束位置 = f"{起始位置}+{len(查找内容)}c"
                self.文本区域.tag_remove("查找高亮", "1.0", tk.END)
                self.文本区域.tag_add("查找高亮", 起始位置, 结束位置)
                self.文本区域.tag_config("查找高亮", background="yellow")
                self.文本区域.see(起始位置)

    def 显示帮助窗口(self):
        帮助文本 = """使用帮助：

基本操作：
Ctrl+N - 新建文件
Ctrl+O - 打开文件
Ctrl+S - 保存文件
Ctrl+Z/Y - 撤销/恢复操作

特殊功能：
• 支持Markdown语法高亮和预览
• 支持Python代码高亮
• 可切换编辑模式
• 自定义颜色主题
• 支持查找功能
"""
        帮助窗口 = tk.Toplevel(self.主窗口)
        帮助窗口.title("使用帮助")
        文本区域 = tk.Text(帮助窗口, wrap="word", width=60, height=20)
        文本区域.pack(padx=10, pady=10)
        文本区域.insert(tk.END, 帮助文本)
        文本区域.config(state=tk.DISABLED)

    def 显示关于信息(self):
        messagebox.showinfo(
            "关于",
            "Python高级文本编辑器\n版本 1.0\n"
            "支持Markdown和代码高亮\n"
            "作者:小推BL"
        )

    def 文本修改事件(self, event=None):
        if self.文本区域.edit_modified():
            self.文本修改状态 = True
            标题 = self.主窗口.title()
            if not 标题.startswith("*"):
                self.主窗口.title(f"*{标题}")
            self.文本区域.edit_modified(False)
            self.应用语法高亮()

    def 检查是否需要保存(self):
        if self.文本修改状态:
            响应 = messagebox.askyesnocancel(
                "保存修改",
                "是否在继续操作前保存当前修改？"
            )
            if 响应 is None:  # 取消操作
                return False
            if 响应:  # 用户选择保存
                self.保存文件()
        return True

    def 退出程序(self):
        if self.检查是否需要保存():
            self.主窗口.destroy()

if __name__ == "__main__":
    主窗口 = tk.Tk()
    主窗口.geometry("1000x700")
    编辑器 = 文本编辑器应用(主窗口)
    主窗口.mainloop()
