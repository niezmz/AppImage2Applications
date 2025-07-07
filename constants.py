"""
常量定义文件
"""

# 应用程序配置
APP_TITLE = "AppImage2Applications - AppImage应用菜单快捷方式创建器"
APP_NAME = "AppImage2Applications"
WINDOW_SIZE = "700x600"

# 文件类型
APPIMAGE_EXTENSIONS = [("AppImage files", "*.AppImage"), ("All files", "*.*")]

# 路径配置
ICONS_DIR = "src"
APPLICATIONS_DIR = "~/.local/share/applications"
ICONS_SHARE_DIR = "~/.local/share/icons"

# 图标文件数量
ICON_COUNT = 8

# 状态消息
STATUS_READY = "就绪"
STATUS_FILE_SELECTED = "已选择文件: {}"
STATUS_ICON_SELECTED = "已选择图标 {}"
STATUS_PERMISSION_FIXED = "执行权限已修复"
STATUS_SHORTCUT_CREATED = "快捷方式已创建"

# 错误消息
ERROR_LINUX_ONLY = "错误: 此应用只能在Linux系统上运行"
ERROR_TKINTER_MISSING = "错误: 需要安装tkinter"
ERROR_PIL_MISSING = "警告: PIL未安装，图标预览功能不可用"

# 安装提示
INSTALL_TKINTER_UBUNTU = "在Ubuntu/Debian上运行: sudo apt-get install python3-tk"
INSTALL_TKINTER_FEDORA = "在Fedora上运行: sudo dnf install python3-tkinter"
INSTALL_PIL = "安装方法: pip install pillow" 