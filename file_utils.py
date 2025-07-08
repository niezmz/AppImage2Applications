"""
文件处理工具模块
"""

import os
import stat
import re
from constants import STATUS_FILE_SELECTED

# 格式化文件大小显示
def format_size(size_bytes):
    """格式化文件大小显示"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

# 获取文件信息
def get_file_info(file_path):
    """获取文件信息"""
    try:
        size = os.path.getsize(file_path)
        size_str = format_size(size)
        is_executable = os.access(file_path, os.X_OK)
        permission_text = "有执行权限" if is_executable else "无执行权限"
        
        return {
            'path': file_path,
            'size': size_str,
            'permission': permission_text,
            'is_executable': is_executable
        }
    except Exception as e:
        raise Exception(f"无法读取文件信息: {str(e)}")

# 修复文件执行权限
def fix_execution_permission(file_path):
    """修复文件执行权限"""
    try:
        current_mode = os.stat(file_path).st_mode
        new_mode = current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        os.chmod(file_path, new_mode)
        return True
    except Exception as e:
        raise Exception(f"无法修复执行权限: {str(e)}")

# 从AppImage文件名提取应用名称
def get_app_name(appimage_path):
    """从AppImage文件名提取应用名称"""
    filename = os.path.basename(appimage_path)
    if filename.endswith('.AppImage'):
        name = filename[:-9]
    else:
        name = filename
    
    # 移除版本号
    name = re.sub(r'-[0-9]+\.[0-9]+(\.[0-9]+)?', '', name)
    name = re.sub(r'[_-]v[0-9]+(\.[0-9]+)*', '', name)
    return name

# 验证AppImage文件
def validate_appimage_file(file_path):
    """验证AppImage文件"""
    if not os.path.exists(file_path):
        raise Exception("文件不存在")
    
    if not file_path.lower().endswith('.appimage'):
        raise Exception("不是有效的AppImage文件")
    
    return True 