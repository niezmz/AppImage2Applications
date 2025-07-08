"""
AppImage2Applications - 主入口文件
将AppImage文件转换为应用菜单快捷方式
适用于Linux系统
"""

import sys
import os

from constants import (
    ERROR_LINUX_ONLY, ERROR_TKINTER_MISSING, ERROR_PIL_MISSING,
    INSTALL_TKINTER_UBUNTU, INSTALL_TKINTER_FEDORA, INSTALL_PIL
)


def check_dependencies():
    """检查依赖项"""
    # 检查操作系统
    if sys.platform != "linux":
        print(ERROR_LINUX_ONLY)
        return False
    
    # 检查tkinter
    try:
        import tkinter
    except ImportError:
        print(ERROR_TKINTER_MISSING)
        print(INSTALL_TKINTER_UBUNTU)
        print(INSTALL_TKINTER_FEDORA)
        return False
    
    # 检查PIL
    try:
        from PIL import Image, ImageTk
    except ImportError:
        print(ERROR_PIL_MISSING)
        print(INSTALL_PIL)
        # PIL不是必需的，只是警告
    
    return True


def main():
    """主函数"""
    # 检查依赖项
    if not check_dependencies():
        return
    
    # 导入GUI模块
    try:
        from gui import AppImage2ApplicationsGUI
    except ImportError as e:
        print(f"导入模块失败: {e}")
        return
    
    # 创建并运行应用程序
    try:
        app = AppImage2ApplicationsGUI()
        app.run()
    except Exception as e:
        print(f"应用程序运行失败: {e}")


if __name__ == "__main__":
    main() 