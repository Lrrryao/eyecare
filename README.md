# 健康提醒助手 (fedora版)

这是一个专为 Linux 系统设计的自动化健康提醒系统，包含眼睛休息提醒和喝水提醒功能。支持 Fedora发行版。



## 📁 文件说明

### 核心程序
- `simple_scheduler.py` - 主程序，负责定时任务管理和后台运行
- `health_reminder_manager.py` - 图形管理界面，用于配置和监控
- `settings_manager.py` - 设置管理器
- `settings_window.py` - 设置窗口界面

### 提醒程序
- `eye/eyecare.py` - 眼睛休息提醒窗口
- `drink_water.py` - 喝水提醒窗口

### 部署脚本 (deploy/)
- `start_health_manager.sh` - 启动健康提醒管理器
- `install_desktop_shortcut.sh` - 安装桌面快捷方式
- `uninstall_desktop_shortcut.sh` - 移除桌面快捷方式
- `install_autostart.sh` - 设置开机自启动
- `uninstall_autostart.sh` - 移除开机自启动

### 配置文件
- `user_settings.json` - 用户设置文件
- `scheduler_status.json` - 程序状态文件（运行时自动生成）
- `requirements.txt` - Python 依赖包列表

## 🚀 快速开始

### 1. 安装依赖

```bash
# Fedora/CentOS/RHEL
sudo dnf install python3-PyQt5 python3-pip

# Ubuntu/Debian
sudo apt install python3-pyqt5 python3-pip
```

### 2. 启动程序

```bash
# 方式1：直接启动管理器（推荐）
python3 health_reminder_manager.py

# 方式2：使用启动脚本
./deploy/start_health_manager.sh

# 方式3：直接启动后台程序
python3 simple_scheduler.py
```

### 3. 安装桌面快捷方式（可选）

```bash
./deploy/install_desktop_shortcut.sh
```

安装后可以在应用程序菜单中找到"健康提醒管理器"。

### 4. 设置开机自启动（可选）

```bash
./deploy/install_autostart.sh
```

## 🎯 使用方法

### 图形管理界面

1. **启动管理器**：运行 `python3 health_reminder_manager.py`
2. **调整设置**：
   - 修改眼睛休息间隔（默认40分钟）
   - 修改喝水提醒间隔（默认30分钟）
   - 选择是否显示启动通知
3. **应用设置**：点击"应用设置"按钮，设置立即生效
4. **启动程序**：点击"启动提醒程序"开始后台运行
5. **监控状态**：查看"下次提醒"时间倒计时

### 程序控制

- **启动程序**：在管理器中点击"启动提醒程序"
- **停止程序**：在管理器中点击"停止提醒程序"
- **重启程序**：在管理器中点击"重启程序"
- **测试提醒**：使用"测试眼睛提醒"和"测试喝水提醒"按钮

### 系统托盘操作（X11环境）

如果系统托盘可用，右键点击托盘图标可以：
- 立即触发眼睛休息提醒
- 立即触发喝水提醒
- 查看当前状态
- 打开设置窗口
- 退出程序

## ⚙️ 配置说明

### 通过图形界面配置（推荐）

使用 `health_reminder_manager.py` 图形界面：
- 实时调整提醒间隔
- 立即应用设置
- 查看运行状态

### 手动编辑配置文件

编辑 `user_settings.json` 文件：

```json
{
  "eye_interval": 40,
  "water_interval": 30,
  "startup_message": true,
  "display_time": 5
}
```

## 🔧 系统要求

- **操作系统**: Linux (Fedora, Ubuntu, Debian, CentOS 等)
- **Python**: Python 3.6+
- **依赖包**: PyQt5
- **桌面环境**: GNOME, KDE, XFCE 等（支持 Wayland 或 X11）

## 📋 管理命令

### 服务管理

```bash
# 查看服务状态
systemctl --user status eyecare

# 启动服务
systemctl --user start eyecare

# 停止服务
systemctl --user stop eyecare

# 查看服务日志
journalctl --user -u eyecare -f
```

### 进程管理

```bash
# 查看运行中的程序
ps aux | grep simple_scheduler

# 停止所有相关进程
pkill -f simple_scheduler.py
```

## 🗑️ 卸载

### 移除桌面快捷方式
```bash
./deploy/uninstall_desktop_shortcut.sh
```

### 移除开机自启动
```bash
./deploy/uninstall_autostart.sh
```

### 完全卸载
```bash
# 停止所有相关进程
pkill -f simple_scheduler.py

# 删除项目目录
rm -rf /home/$(whoami)/internship/backend/projects/eyecare
```

## 🐛 故障排除

### 常见问题

1. **PyQt5 未安装**
   ```bash
   sudo dnf install python3-PyQt5  # Fedora
   sudo apt install python3-pyqt5  # Ubuntu
   ```

2. **系统托盘不可用**
   - 在 Wayland 环境下，程序会自动使用系统通知
   - 在 X11 环境下，确保系统托盘服务正在运行

3. **权限问题**
   ```bash
   chmod +x deploy/*.sh
   ```

4. **桌面快捷方式不显示**
   ```bash
   ./deploy/install_desktop_shortcut.sh
   update-desktop-database ~/.local/share/applications
   ```

### 日志查看

- **管理器日志**：在图形界面的日志区域查看
- **系统服务日志**：`journalctl --user -u eyecare -f`
- **程序输出**：直接运行 `python3 simple_scheduler.py` 查看控制台输出

## 📄 许可证

本项目采用 MIT 许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

---

**注意**: 这个版本专为 Linux 系统设计，与 Windows 版本不兼容。如需 Windows 版本，请查看其他分支。