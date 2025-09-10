#!/bin/bash
# 移除桌面快捷方式脚本

echo "正在移除健康提醒管理器桌面快捷方式..."

# 获取当前用户
USER=$(whoami)
echo "当前用户: $USER"

# 桌面快捷方式文件路径
DESKTOP_TARGET="$HOME/.local/share/applications/health-reminder.desktop"

# 检查文件是否存在
if [ -f "$DESKTOP_TARGET" ]; then
    # 删除桌面快捷方式文件
    rm "$DESKTOP_TARGET"
    echo "桌面快捷方式已移除: $DESKTOP_TARGET"
    
    # 更新桌面数据库
    DESKTOP_TARGET_DIR="$HOME/.local/share/applications"
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database "$DESKTOP_TARGET_DIR"
        echo "桌面数据库已更新"
    fi
    
    echo "移除完成！"
else
    echo "桌面快捷方式不存在: $DESKTOP_TARGET"
    echo "可能已经被移除或从未安装"
fi
