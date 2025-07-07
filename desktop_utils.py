"""
桌面文件处理模块
"""

import os
import shutil
import subprocess
from file_utils import get_app_name


def create_desktop_file(desktop_path, appimage_path, app_name, icon_name):
    """创建桌面文件"""
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


def setup_icon(app_name, selected_icon_path):
    """
    设置图标：如果用户选择了图标，复制到~/.local/share/icons并返回图标名
    """
    if not selected_icon_path:
        return None
    
    try:
        icons_dir = os.path.expanduser("~/.local/share/icons")
        os.makedirs(icons_dir, exist_ok=True)
        icon_name = app_name.lower()
        
        # 获取原图标扩展名
        ext = os.path.splitext(selected_icon_path)[1].lower()
        if ext not in ['.png', '.svg']:
            raise Exception("图标文件格式不是PNG或SVG，可能无法正常显示")
        
        # 复制图标到icons目录
        dst = os.path.join(icons_dir, icon_name + ext)
        shutil.copyfile(selected_icon_path, dst)
        
        # 返回图标名（不带扩展名）
        return os.path.splitext(os.path.basename(dst))[0]
    except Exception as e:
        raise Exception(f"设置图标失败: {str(e)}")


def refresh_applications_menu():
    """刷新应用程序菜单"""
    try:
        # 更新桌面数据库
        subprocess.run(["update-desktop-database", os.path.expanduser("~/.local/share/applications")], 
                      capture_output=True, timeout=5)
        # 强制刷新图标缓存
        subprocess.run(["gtk-update-icon-cache", "-f", "-t", os.path.expanduser("~/.local/share/icons")], 
                      capture_output=True, timeout=5)
        # 尝试刷新系统图标缓存
        subprocess.run(["gtk-update-icon-cache", "-f", "-t", "/usr/share/icons"], 
                      capture_output=True, timeout=5)
    except Exception:
        pass


def create_app_shortcut(appimage_path, selected_icon_path=None):
    """创建应用程序快捷方式"""
    try:
        # 验证文件权限
        if not os.access(appimage_path, os.X_OK):
            from file_utils import fix_execution_permission
            fix_execution_permission(appimage_path)
        
        # 获取应用名称
        app_name = get_app_name(appimage_path)
        
        # 设置图标
        icon_name = setup_icon(app_name, selected_icon_path)
        
        # 创建applications目录
        applications_dir = os.path.expanduser("~/.local/share/applications")
        os.makedirs(applications_dir, exist_ok=True)
        
        # 创建桌面文件
        app_file_path = os.path.join(applications_dir, f"{app_name}.desktop")
        create_desktop_file(app_file_path, appimage_path, app_name, icon_name)
        
        # 设置桌面文件权限
        os.chmod(app_file_path, 0o755)
        
        # 刷新应用程序菜单
        refresh_applications_menu()
        
        return {
            'success': True,
            'desktop_path': app_file_path,
            'app_name': app_name,
            'icon_name': icon_name
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def get_icon_paths():
    """获取图标文件路径列表"""
    icon_paths = []
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join(base_dir, "src")
    
    for i in range(1, 9):  # 1-8
        icon_path = os.path.join(icons_dir, f"{i}.png")
        icon_paths.append(icon_path)
    
    return icon_paths 