"""
GUI界面模块
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from PIL import Image, ImageTk

from constants import (
    APP_TITLE, WINDOW_SIZE, APPIMAGE_EXTENSIONS, ICON_COUNT,
    STATUS_READY, STATUS_FILE_SELECTED, STATUS_ICON_SELECTED,
    STATUS_PERMISSION_FIXED, STATUS_SHORTCUT_CREATED
)
from file_utils import get_file_info, fix_execution_permission, validate_appimage_file
from desktop_utils import create_app_shortcut, get_icon_paths


class AppImage2ApplicationsGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(True, True)
        
        try:
            self.root.iconname("AppImage2Applications")
        except:
            pass
        
        # 初始化变量
        self.current_file = None
        self.selected_icon = None
        self.icon_buttons = []
        
        self.setup_ui()

    def setup_ui(self):
        """设置用户界面"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="AppImage2Applications", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 说明
        instruction_label = ttk.Label(main_frame, text="点击选择文件按钮来选择AppImage文件，快捷方式将自动放入应用菜单")
        instruction_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # 选择按钮
        select_button = ttk.Button(main_frame, text="选择AppImage文件", command=self.select_file)
        select_button.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        # 文件信息框架
        self.setup_file_info_frame(main_frame)
        
        # 图标选择框架
        self.setup_icon_frame(main_frame)
        
        # 按钮框架
        self.setup_button_frame(main_frame)
        
        # 快捷方式信息框架
        self.setup_shortcut_info_frame(main_frame)
        
        # 状态栏
        self.setup_status_bar(main_frame)

    def setup_file_info_frame(self, parent):
        """设置文件信息框架"""
        self.file_info_frame = ttk.LabelFrame(parent, text="文件信息", padding="5")
        self.file_info_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.file_info_frame.columnconfigure(1, weight=1)
        
        # 文件信息变量
        self.file_path_var = tk.StringVar()
        self.file_size_var = tk.StringVar()
        self.file_permission_var = tk.StringVar()
        
        # 文件信息标签
        ttk.Label(self.file_info_frame, text="文件路径:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(self.file_info_frame, textvariable=self.file_path_var, foreground="blue").grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Label(self.file_info_frame, text="文件大小:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(self.file_info_frame, textvariable=self.file_size_var).grid(row=1, column=1, sticky=(tk.W, tk.E))
        ttk.Label(self.file_info_frame, text="执行权限:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(self.file_info_frame, textvariable=self.file_permission_var).grid(row=2, column=1, sticky=(tk.W, tk.E))

    def setup_icon_frame(self, parent):
        """设置图标选择框架"""
        self.icon_frame = ttk.LabelFrame(parent, text="图标设置", padding="5")
        self.icon_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.icon_frame.columnconfigure(0, weight=1)
        
        # 图标路径变量
        self.icon_path_var = tk.StringVar()
        self.icon_path_var.set("未选择图标")
        
        ttk.Label(self.icon_frame, text="应用图标:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(self.icon_frame, textvariable=self.icon_path_var, foreground="purple").grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # 图标网格显示
        self.icon_canvas_frame = ttk.Frame(self.icon_frame)
        self.icon_canvas_frame.grid(row=1, column=0, columnspan=2, pady=(5, 0))
        self.setup_icon_grid()
        
        # 图标说明
        icon_note = ttk.Label(self.icon_frame, text="说明：点击上方图标选择一个作为应用图标。也可以在src文件夹替换上述8张预设的icon图，规格为512*512的png文件。",
                              foreground="gray", font=("Arial", 8))
        icon_note.grid(row=2, column=0, columnspan=2, pady=(5, 0), sticky=tk.W)

    def setup_icon_grid(self):
        """设置图标网格显示"""
        icon_paths = get_icon_paths()
        
        # 创建4x2的网格布局
        for i in range(ICON_COUNT):
            row = i // 4
            col = i % 4
            icon_num = i + 1
            icon_path = icon_paths[i] if i < len(icon_paths) else None
            
            # 创建图标按钮框架
            icon_frame = ttk.Frame(self.icon_canvas_frame)
            icon_frame.grid(row=row, column=col, padx=5, pady=5)
            
            # 创建图标按钮
            icon_button = ttk.Button(icon_frame, text=f"图标 {icon_num}", 
                                   command=lambda path=icon_path, num=icon_num: self.select_icon_from_grid(path, num))
            icon_button.pack()
            
            # 尝试显示图标预览
            try:
                if icon_path and os.path.exists(icon_path):
                    # 使用PIL加载和缩放图标
                    img = Image.open(icon_path)
                    img = img.resize((32, 32), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    
                    # 创建带图标的按钮
                    icon_button_with_image = ttk.Button(icon_frame, image=photo, 
                                                      command=lambda path=icon_path, num=icon_num: self.select_icon_from_grid(path, num))
                    icon_button_with_image.image = photo  # 保持引用
                    icon_button_with_image.pack()
                    self.icon_buttons.append(icon_button_with_image)
                else:
                    self.icon_buttons.append(icon_button)
            except Exception as e:
                # 如果无法加载图标，使用文本按钮
                self.icon_buttons.append(icon_button)

    def setup_button_frame(self, parent):
        """设置按钮框架"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        self.create_shortcut_button = ttk.Button(button_frame, text="创建应用菜单快捷方式", 
                                               command=self.create_shortcut, state="disabled")
        self.create_shortcut_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.fix_permission_button = ttk.Button(button_frame, text="修复执行权限", 
                                              command=self.fix_permission, state="disabled")
        self.fix_permission_button.pack(side=tk.LEFT)

    def setup_shortcut_info_frame(self, parent):
        """设置快捷方式信息框架"""
        self.shortcut_info_frame = ttk.LabelFrame(parent, text="快捷方式信息", padding="5")
        self.shortcut_info_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        self.shortcut_info_frame.columnconfigure(1, weight=1)
        
        self.shortcut_path_var = tk.StringVar()
        self.shortcut_path_var.set("未创建")
        
        ttk.Label(self.shortcut_info_frame, text="快捷方式位置:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(self.shortcut_info_frame, textvariable=self.shortcut_path_var, foreground="green").grid(row=0, column=1, sticky=(tk.W, tk.E))

    def setup_status_bar(self, parent):
        """设置状态栏"""
        self.status_var = tk.StringVar()
        self.status_var.set(STATUS_READY)
        status_bar = ttk.Label(parent, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

    def select_icon_from_grid(self, icon_path, icon_num):
        """从网格中选择图标"""
        if icon_path and os.path.exists(icon_path):
            self.selected_icon = icon_path
            self.icon_path_var.set(f"图标 {icon_num} ({os.path.basename(icon_path)})")
            self.status_var.set(STATUS_ICON_SELECTED.format(icon_num))
        else:
            messagebox.showerror("错误", f"图标文件不存在: {icon_path}")

    def select_file(self):
        """选择文件"""
        file_path = filedialog.askopenfilename(
            title="选择AppImage文件",
            filetypes=APPIMAGE_EXTENSIONS
        )
        if file_path:
            self.process_file(file_path)

    def process_file(self, file_path):
        """处理选择的文件"""
        try:
            validate_appimage_file(file_path)
            self.current_file = file_path
            self.update_file_info(file_path)
            self.create_shortcut_button.config(state="normal")
            self.fix_permission_button.config(state="normal")
            self.status_var.set(STATUS_FILE_SELECTED.format(os.path.basename(file_path)))
            self.shortcut_path_var.set("未创建")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def update_file_info(self, file_path):
        """更新文件信息显示"""
        try:
            file_info = get_file_info(file_path)
            self.file_path_var.set(file_info['path'])
            self.file_size_var.set(file_info['size'])
            self.file_permission_var.set(file_info['permission'])
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def fix_permission(self):
        """修复执行权限"""
        if not self.current_file:
            return
        
        try:
            fix_execution_permission(self.current_file)
            self.update_file_info(self.current_file)
            self.status_var.set(STATUS_PERMISSION_FIXED)
            messagebox.showinfo("成功", "AppImage文件的执行权限已修复")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def create_shortcut(self):
        """创建快捷方式"""
        if not self.current_file:
            return
        
        try:
            result = create_app_shortcut(self.current_file, self.selected_icon)
            
            if result['success']:
                self.shortcut_path_var.set(result['desktop_path'])
                self.status_var.set(STATUS_SHORTCUT_CREATED)
                
                if result['icon_name']:
                    msg = f"应用菜单快捷方式已创建:\n{result['desktop_path']}\n\n图标已设置。如果图标没有立即更新，请尝试：\n1. 注销并重新登录\n2. 或重启桌面环境\n3. 或在终端运行: gtk-update-icon-cache -f -t ~/.local/share/icons"
                else:
                    msg = f"应用菜单快捷方式已创建:\n{result['desktop_path']}\n\n未设置图标，应用菜单可能无图标。"
                
                messagebox.showinfo("成功", msg)
            else:
                messagebox.showerror("错误", f"创建快捷方式失败: {result['error']}")
        except Exception as e:
            messagebox.showerror("错误", f"创建快捷方式失败: {str(e)}")

    def run(self):
        """运行应用程序"""
        self.root.mainloop() 