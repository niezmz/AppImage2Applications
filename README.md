# AppImage2Applications

一个用于Linux系统的Python应用，可以将AppImage文件转换为应用菜单快捷方式。

## 功能特性

1. **图形用户界面** - 使用tkinter创建的现代化GUI界面
2. **文件选择** - 通过文件对话框选择AppImage文件
3. **权限检查** - 自动检查AppImage文件是否具有执行权限
4. **权限修复** - 一键修复AppImage文件的执行权限
5. **图标选择** - 内置8个预设图标，点击即可选择
6. **快捷方式创建** - 在应用菜单创建.desktop快捷方式文件
7. **自动权限设置** - 为创建的快捷方式设置正确的执行权限
8. **图标预览** - 实时预览图标效果

## 系统要求

- Linux操作系统
- Python 3.6+
- tkinter（通常需要额外安装）
- Pillow（用于图标预览）

## 安装依赖

### 1. 安装系统依赖

#### Ubuntu/Debian系统
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

#### Fedora系统
```bash
sudo dnf install python3-tkinter
```

#### Arch Linux
```bash
sudo pacman -S tk
```

### 2. 安装Python依赖

```bash
pip install pillow
```

## 使用方法

### 运行应用
```bash
python3 appimage2applications.py
```

## 使用步骤

1. **启动应用** - 运行Python脚本，会打开一个图形界面窗口
2. **选择AppImage文件** - 点击"选择AppImage文件"按钮，选择要处理的AppImage文件
3. **查看文件信息** - 应用会显示文件路径、大小和执行权限状态
4. **选择图标** - 在图标网格中点击选择一个图标（8个预设图标可选）
5. **修复权限**（可选） - 如果AppImage没有执行权限，点击"修复执行权限"按钮
6. **创建快捷方式** - 点击"创建应用菜单快捷方式"按钮，应用会在应用菜单创建.desktop文件

## 文件说明

- `appimage2applications.py` - 主程序文件，支持图标选择和预览
- `src/` - 预设图标文件夹，包含8个PNG格式的图标文件
- `requirements.txt` - 项目依赖文件
- `README.md` - 项目说明文档

## 功能详解

### 权限检查
应用会自动检查AppImage文件是否具有执行权限（x权限）。如果没有权限，文件将无法运行。

### 权限修复
点击"修复执行权限"按钮后，应用会为AppImage文件添加用户、组和其他用户的执行权限。

### 图标选择
- 应用内置8个预设图标，以4x2网格形式显示
- 点击任意图标即可选择，支持实时预览
- 选择的图标会自动复制到 `~/.local/share/icons/` 目录

### 快捷方式创建
创建的.desktop文件包含以下信息：
- 应用名称（从文件名自动提取）
- 执行路径（AppImage文件的完整路径）
- 图标路径（指向选择的图标文件）
- 应用分类
- 启动窗口类名

### 应用菜单集成
快捷方式会被创建到 `~/.local/share/applications/` 目录，这样：
- 可以在GNOME的"活动"菜单中搜索到
- 可以在KDE的应用菜单中找到
- 支持所有标准Linux桌面环境

## 预设图标

应用内置了8个高质量的PNG图标，位于 `src/` 文件夹中：
- 1.png - 8.png
- 图标尺寸：549KB - 1.8MB
- 格式：PNG，支持透明背景

## 注意事项

1. **权限要求** - 应用需要写入 `~/.local/share/` 目录的权限
2. **图标格式** - 仅支持PNG格式图标，确保最佳兼容性
3. **系统兼容性** - 此应用专为Linux系统设计，不支持其他操作系统
4. **AppImage格式** - 支持标准的AppImage文件格式
5. **桌面环境** - 适用于GNOME、KDE、XFCE等主流桌面环境

## 故障排除

### 问题：应用无法启动
**解决方案：**
- 确保安装了python3-tk：`sudo apt-get install python3-tk`
- 确保安装了pillow：`pip install pillow`
- 检查Python版本：`python3 --version`

### 问题：图标无法显示
**解决方案：**
- 确保安装了pillow：`pip install pillow`
- 检查src文件夹是否存在：`ls src/`
- 确保图标文件为PNG格式

### 问题：无法创建快捷方式
**解决方案：**
- 检查应用目录权限：`ls -la ~/.local/share/applications`
- 确保有写入权限：`chmod 755 ~/.local/share/applications`

### 问题：AppImage无法运行
**解决方案：**
- 使用应用内的"修复执行权限"功能
- 或手动设置权限：`chmod +x your-app.AppImage`

### 问题：快捷方式在应用菜单中找不到
**解决方案：**
- 刷新应用菜单：`update-desktop-database ~/.local/share/applications`
- 重启桌面环境或注销再登录
- 在"活动"菜单中搜索应用名称

## 开发信息

- **编程语言：** Python 3
- **GUI框架：** tkinter
- **图像处理：** Pillow (PIL)
- **目标平台：** Linux
- **许可证：** MIT

## 清理快捷方式

如需删除创建的快捷方式：
```bash
# 删除应用菜单快捷方式
rm ~/.local/share/applications/应用名称.desktop

# 删除图标文件
rm ~/.local/share/icons/应用名称.png

# 刷新应用菜单
update-desktop-database ~/.local/share/applications
```

## 贡献

欢迎提交问题报告和功能建议！ 