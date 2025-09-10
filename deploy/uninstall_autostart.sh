#!/bin/bash
# 健康提醒助手开机自启动卸载脚本

echo "正在移除健康提醒助手开机自启动..."

# 停止服务
echo "停止服务..."
systemctl --user stop eyecare.service 2>/dev/null

# 禁用服务
echo "禁用服务..."
systemctl --user disable eyecare.service 2>/dev/null

# 重新加载systemd配置
systemctl --user daemon-reload

# 删除服务文件
SERVICE_FILE="$HOME/.config/systemd/user/eyecare.service"
if [ -f "$SERVICE_FILE" ]; then
    rm "$SERVICE_FILE"
    echo "服务文件已删除: $SERVICE_FILE"
else
    echo "服务文件不存在: $SERVICE_FILE"
fi

echo "开机自启动已移除！"
echo "健康提醒助手将不再在开机时自动启动。"
