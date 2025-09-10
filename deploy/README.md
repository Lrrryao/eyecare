# 部署脚本说明

这个目录包含了健康提醒助手的所有部署和管理脚本。

## 📋 脚本列表

### 🚀 启动脚本
- **`start_health_manager.sh`** - 启动健康提醒管理器（图形界面）
- **`start_manager.sh`** - 启动管理器的备用脚本

### 🖥️ 桌面快捷方式
- **`install_desktop_shortcut.sh`** - 安装桌面快捷方式
- **`uninstall_desktop_shortcut.sh`** - 移除桌面快捷方式

### ⚡ 开机自启动
- **`install_autostart.sh`** - 设置开机自启动
- **`uninstall_autostart.sh`** - 移除开机自启动

## 🎯 使用方法

### 快速启动
```bash
# 启动健康提醒管理器
./deploy/start_health_manager.sh
```

### 桌面快捷方式
```bash
# 安装桌面快捷方式（推荐）
./deploy/install_desktop_shortcut.sh

# 移除桌面快捷方式
./deploy/uninstall_desktop_shortcut.sh
```

### 开机自启动
```bash
# 设置开机自启动
./deploy/install_autostart.sh

# 移除开机自启动
./deploy/uninstall_autostart.sh
```

## 📝 注意事项

1. **权限要求**：所有脚本都需要执行权限
2. **依赖检查**：脚本会自动检查 Python3 和 PyQt5 是否安装
3. **路径要求**：脚本必须在项目根目录下运行
4. **用户权限**：桌面快捷方式和自启动设置仅对当前用户有效

## 🔧 故障排除

如果遇到问题，请检查：
- Python3 是否已安装
- PyQt5 是否已安装：`sudo dnf install python3-PyQt5`
- 脚本是否有执行权限：`chmod +x deploy/*.sh`
- 是否在正确的目录下运行脚本
