# 健康提醒助手

这是一个自动化的健康提醒系统，包含眼睛休息提醒和喝水提醒功能。

## 功能特点

- 🕐 **定时提醒**: 眼睛休息每40分钟提醒一次，喝水每30分钟提醒一次
- 🖥️ **系统托盘**: 在系统托盘中运行，不占用桌面空间
- 👁️ **隐藏运行**: 程序不在任务栏显示，完全隐藏在系统托盘中
- ⚙️ **可配置**: 通过配置文件轻松调整提醒间隔
- 🚀 **开机自启**: 自动添加到Windows启动项

## 文件说明

- `task_scheduler.py` - 主程序，负责定时任务管理
- `eyecare.py` - 眼睛休息提醒窗口
- `drink_water.py` - 喝水提醒窗口
- `config.py` - 配置文件，可调整提醒间隔
- `start_health_reminder_hidden.bat` - 完全隐藏启动脚本（推荐）
- `start_health_reminder.bat` - 带控制台的启动脚本（用于调试）

## 使用方法

### 自动启动（推荐）
系统已自动配置为开机自启，重启电脑后会自动运行。

### 手动启动
1. 双击 `start_health_reminder_hidden.bat` 完全隐藏启动（推荐）
2. 双击 `start_health_reminder.bat` 带控制台启动（用于调试）

### 系统托盘操作
- 右键点击系统托盘图标可以：
  - 立即触发眼睛休息提醒
  - 立即触发喝水提醒
  - 查看当前状态
  - 退出程序

## 配置说明

编辑 `config.py` 文件可以调整以下设置：

```python
# 眼睛休息提醒间隔（分钟）
EYE_REMINDER_INTERVAL = 40

# 喝水提醒间隔（分钟）
WATER_REMINDER_INTERVAL = 30

# 提醒窗口显示时间（秒）
REMINDER_DISPLAY_TIME = 5

# 是否启用系统托盘
ENABLE_SYSTEM_TRAY = True

# 是否在启动时显示消息
SHOW_STARTUP_MESSAGE = True
```

## 停止服务

1. 右键点击系统托盘图标，选择"退出"
2. 或在任务管理器中结束 `python.exe` 进程

## 卸载

1. 删除启动文件夹中的 `start_health_reminder_silent.bat`
2. 删除整个 `D:\Eyecare` 文件夹

## 注意事项

- 确保已安装 Python 和 PyQt5
- 图片文件路径需要正确设置
- 程序会在后台运行，不会显示主窗口
