#!/bin/bash
# 安装桌面快捷方式脚本

echo "正在安装健康提醒管理器桌面快捷方式..."

# 获取当前用户
USER=$(whoami)
echo "当前用户: $USER"

# 获取当前脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "脚本目录: $SCRIPT_DIR"

# 桌面快捷方式文件
DESKTOP_FILE="$SCRIPT_DIR/health-reminder.desktop"
DESKTOP_TARGET="$HOME/.local/share/applications/health-reminder.desktop"
DESKTOP_TARGET_DIR="$HOME/.local/share/applications"

# 检查源文件是否存在
if [ ! -f "$DESKTOP_FILE" ]; then
    echo "错误: 桌面快捷方式文件不存在: $DESKTOP_FILE"
    exit 1
fi

# 创建目标目录
mkdir -p "$DESKTOP_TARGET_DIR"

# 复制桌面快捷方式文件
cp "$DESKTOP_FILE" "$DESKTOP_TARGET"

# 设置执行权限
chmod +x "$DESKTOP_TARGET"

echo "桌面快捷方式已安装到: $DESKTOP_TARGET"

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$DESKTOP_TARGET_DIR"
    echo "桌面数据库已更新"
fi

# 检查图标文件
ICON_FILE="$SCRIPT_DIR/../drink.png"
if [ -f "$ICON_FILE" ]; then
    echo "图标文件存在: $ICON_FILE"
else
    echo "警告: 图标文件不存在: $ICON_FILE"
    echo "快捷方式将使用默认图标"
fi

echo ""
echo "安装完成！"
echo "现在你可以："
echo "1. 在应用程序菜单中找到 '健康提醒管理器'"
echo "2. 在桌面环境中搜索 '健康提醒' 或 'health reminder'"
echo "3. 双击桌面快捷方式启动程序"
echo ""
echo "如需移除快捷方式，请运行:"
echo "rm '$DESKTOP_TARGET'"
