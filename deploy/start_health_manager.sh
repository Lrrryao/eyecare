#!/bin/bash
# 健康提醒管理器启动脚本

echo "启动健康提醒管理器..."

# 切换到项目根目录
cd "$(dirname "$0")/.."

# 检查Python3是否可用
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3"
    exit 1
fi

# 检查PyQt5是否安装
python3 -c "import PyQt5" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "错误: 未找到PyQt5，请先安装:"
    echo "sudo dnf install python3-PyQt5"
    exit 1
fi

# 启动管理器
python3 health_reminder_manager.py
