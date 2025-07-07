"""
AppImage2Applications - 将AppImage文件转换为应用菜单快捷方式
适用于Linux系统（无拖放功能，仅放入applications，预设图标选择）
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import stat
import subprocess
import sys
from pathlib import Path
import shutil
import re
from PIL import Image, ImageTk

class AppImage2Applications:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AppImage2Applications - AppImage应用菜单快捷方式创建器")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        try:
            self.root.iconname("AppImage2Applications")
        except:
            pass
        self.setup_ui()

    def setup_ui(self):
        # 初始化图标按钮列表
        self.icon_buttons = []
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        title_label = ttk.Label(main_frame, text="AppImage2Applications", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        instruction_label = ttk.Label(main_frame, text="点击选择文件按钮来选择AppImage文件，快捷方式将自动放入应用菜单（不放入桌面）")
        instruction_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        select_button = ttk.Button(main_frame, text="选择AppImage文件", command=self.select_file)
        select_button.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        self.file_info_frame = ttk.LabelFrame(main_frame, text="文件信息", padding="5")
        self.file_info_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.file_info_frame.columnconfigure(1, weight=1)
        self.file_path_var = tk.StringVar()
        self.file_size_var = tk.StringVar()
        self.file_permission_var = tk.StringVar()
        ttk.Label(self.file_info_frame, text="文件路径:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(self.file_info_frame, textvariable=self.file_path_var, foreground="blue").grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Label(self.file_info_frame, text="文件大小:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(self.file_info_frame, textvariable=self.file_size_var).grid(row=1, column=1, sticky=(tk.W, tk.E))
        ttk.Label(self.file_info_frame, text="执行权限:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(self.file_info_frame, textvariable=self.file_permission_var).grid(row=2, column=1, sticky=(tk.W, tk.E))
        # 图标选择区域
        self.icon_frame = ttk.LabelFrame(main_frame, text="图标设置", padding="5")
        self.icon_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.icon_frame.columnconfigure(0, weight=1)
        self.icon_path_var = tk.StringVar()
        self.icon_path_var.set("未选择图标")
        ttk.Label(self.icon_frame, text="应用图标:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(self.icon_frame, textvariable=self.icon_path_var, foreground="purple").grid(row=0, column=1, sticky=(tk.W, tk.E))
        # 图标网格显示
        self.icon_canvas_frame = ttk.Frame(self.icon_frame)
        self.icon_canvas_frame.grid(row=1, column=0, columnspan=2, pady=(5, 0))
        self.setup_icon_grid()
        # 图标说明
        icon_note = ttk.Label(self.icon_frame, text="说明：点击上方图标选择一个作为应用图标。Linux桌面环境需要PNG格式的图标文件才能正常显示。", 
                              foreground="gray", font=("Arial", 8))
        icon_note.grid(row=2, column=0, columnspan=2, pady=(5, 0), sticky=tk.W)
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        self.create_shortcut_button = ttk.Button(button_frame, text="创建应用菜单快捷方式", command=self.create_shortcut, state="disabled")
        self.create_shortcut_button.pack(side=tk.LEFT, padx=(0, 10))
        self.fix_permission_button = ttk.Button(button_frame, text="修复执行权限", command=self.fix_permission, state="disabled")
        self.fix_permission_button.pack(side=tk.LEFT)
        self.shortcut_info_frame = ttk.LabelFrame(main_frame, text="快捷方式信息", padding="5")
        self.shortcut_info_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        self.shortcut_info_frame.columnconfigure(1, weight=1)
        self.shortcut_path_var = tk.StringVar()
        self.shortcut_path_var.set("未创建")
        ttk.Label(self.shortcut_info_frame, text="快捷方式位置:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(self.shortcut_info_frame, textvariable=self.shortcut_path_var, foreground="green").grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        self.current_file = None
        self.selected_icon = None

    def setup_icon_grid(self):
        """设置图标网格显示"""
        # 创建4x2的网格布局
        for i in range(8):
            row = i // 4
            col = i % 4
            icon_num = i + 1
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", f"{icon_num}.png")
            
            # 创建图标按钮框架
            icon_frame = ttk.Frame(self.icon_canvas_frame)
            icon_frame.grid(row=row, column=col, padx=5, pady=5)
            
            # 创建图标按钮
            icon_button = ttk.Button(icon_frame, text=f"图标 {icon_num}", 
                                   command=lambda path=icon_path, num=icon_num: self.select_icon_from_grid(path, num))
            icon_button.pack()
            
            # 尝试显示图标预览
            try:
                if os.path.exists(icon_path):
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

    def select_icon_from_grid(self, icon_path, icon_num):
        """从网格中选择图标"""
        if os.path.exists(icon_path):
            self.selected_icon = icon_path
            self.icon_path_var.set(f"图标 {icon_num} ({os.path.basename(icon_path)})")
            self.status_var.set(f"已选择图标 {icon_num}")
        else:
            messagebox.showerror("错误", f"图标文件不存在: {icon_path}")

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="选择AppImage文件",
            filetypes=[("AppImage files", "*.AppImage"), ("All files", "*.*")]
        )
        if file_path:
            self.process_file(file_path)

    def process_file(self, file_path):
        self.current_file = file_path
        self.update_file_info(file_path)
        self.create_shortcut_button.config(state="normal")
        self.fix_permission_button.config(state="normal")
        self.status_var.set(f"已选择文件: {os.path.basename(file_path)}")
        self.shortcut_path_var.set("未创建")

    def update_file_info(self, file_path):
        try:
            self.file_path_var.set(file_path)
            size = os.path.getsize(file_path)
            size_str = self.format_size(size)
            self.file_size_var.set(size_str)
            is_executable = os.access(file_path, os.X_OK)
            permission_text = "有执行权限" if is_executable else "无执行权限"
            self.file_permission_var.set(permission_text)
        except Exception as e:
            messagebox.showerror("错误", f"无法读取文件信息: {str(e)}")

    def format_size(self, size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def fix_permission(self):
        if not self.current_file:
            return
        try:
            current_mode = os.stat(self.current_file).st_mode
            new_mode = current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
            os.chmod(self.current_file, new_mode)
            self.update_file_info(self.current_file)
            self.status_var.set("执行权限已修复")
            messagebox.showinfo("成功", "AppImage文件的执行权限已修复")
        except Exception as e:
            messagebox.showerror("错误", f"无法修复执行权限: {str(e)}")

    def create_shortcut(self):
        if not self.current_file:
            return
        try:
            if not os.access(self.current_file, os.X_OK):
                self.fix_permission()
            app_name = self.get_app_name(self.current_file)
            icon_name = self.setup_icon(app_name)
            applications_dir = os.path.expanduser("~/.local/share/applications")
            os.makedirs(applications_dir, exist_ok=True)
            app_file_path = os.path.join(applications_dir, f"{app_name}.desktop")
            self.create_desktop_file(app_file_path, self.current_file, app_name, icon_name)
            os.chmod(app_file_path, 0o755)
            self.shortcut_path_var.set(app_file_path)
            self.refresh_applications_menu()
            self.status_var.set(f"快捷方式已创建")
            if icon_name:
                msg = f"应用菜单快捷方式已创建:\n{app_file_path}\n\n图标已设置。如果图标没有立即更新，请尝试：\n1. 注销并重新登录\n2. 或重启桌面环境\n3. 或在终端运行: gtk-update-icon-cache -f -t ~/.local/share/icons"
            else:
                msg = f"应用菜单快捷方式已创建:\n{app_file_path}\n\n未设置图标，应用菜单可能无图标。"
            messagebox.showinfo("成功", msg)
        except Exception as e:
            messagebox.showerror("错误", f"创建快捷方式失败: {str(e)}")

    def setup_icon(self, app_name):
        """
        设置图标：如果用户选择了图标，复制到~/.local/share/icons并返回图标名
        """
        if not self.selected_icon:
            return None
        try:
            icons_dir = os.path.expanduser("~/.local/share/icons")
            os.makedirs(icons_dir, exist_ok=True)
            icon_name = app_name.lower()
            # 获取原图标扩展名
            ext = os.path.splitext(self.selected_icon)[1].lower()
            if ext not in ['.png', '.svg']:
                messagebox.showwarning("警告", "图标文件格式不是PNG或SVG，可能无法正常显示")
            # 复制图标到icons目录
            dst = os.path.join(icons_dir, icon_name + ext)
            shutil.copyfile(self.selected_icon, dst)
            # 返回图标名（不带扩展名）
            return os.path.splitext(os.path.basename(dst))[0]
        except Exception as e:
            messagebox.showerror("错误", f"设置图标失败: {str(e)}")
            return None

    def refresh_applications_menu(self):
        try:
            # 更新桌面数据库
            subprocess.run(["update-desktop-database", os.path.expanduser("~/.local/share/applications")], capture_output=True, timeout=5)
            # 强制刷新图标缓存
            subprocess.run(["gtk-update-icon-cache", "-f", "-t", os.path.expanduser("~/.local/share/icons")], capture_output=True, timeout=5)
            # 尝试刷新系统图标缓存
            subprocess.run(["gtk-update-icon-cache", "-f", "-t", "/usr/share/icons"], capture_output=True, timeout=5)
        except Exception:
            pass

    def get_app_name(self, appimage_path):
        filename = os.path.basename(appimage_path)
        if filename.endswith('.AppImage'):
            name = filename[:-9]
        else:
            name = filename
        name = re.sub(r'-[0-9]+\.[0-9]+(\.[0-9]+)?', '', name)
        name = re.sub(r'[_-]v[0-9]+(\.[0-9]+)*', '', name)
        return name

    def create_desktop_file(self, desktop_path, appimage_path, app_name, icon_name):
        if icon_name:
            icon_line = f"Icon={icon_name}"
        else:
            icon_line = f"Icon={appimage_path}"
        desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={app_name}
Comment={app_name} Application
Exec={appimage_path}
{icon_line}
Terminal=false
Categories=Application;
StartupWMClass={app_name}
"""
        with open(desktop_path, 'w', encoding='utf-8') as f:
            f.write(desktop_content)

    def run(self):
        self.root.mainloop()

def main():
    if sys.platform != "linux":
        print("错误: 此应用只能在Linux系统上运行")
        return
    try:
        import tkinter
    except ImportError:
        print("错误: 需要安装tkinter")
        print("在Ubuntu/Debian上运行: sudo apt-get install python3-tk")
        print("在Fedora上运行: sudo dnf install python3-tkinter")
        return
    # 检查PIL是否可用
    try:
        from PIL import Image, ImageTk
    except ImportError:
        print("警告: PIL未安装，图标预览功能不可用")
        print("安装方法: pip install pillow")
    app = AppImage2Applications()
    app.run()

if __name__ == "__main__":
    main() 