#!/bin/bash
# 健康提醒助手开机自启动安装脚本

echo "正在设置健康提醒助手开机自启动..."

# 获取当前用户
USER=$(whoami)
echo "当前用户: $USER"

# 获取当前脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "脚本目录: $SCRIPT_DIR"

# 创建systemd用户服务目录
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"
mkdir -p "$SYSTEMD_USER_DIR"

# 复制服务文件并替换路径
SERVICE_FILE="$SYSTEMD_USER_DIR/eyecare.service"
cp "$SCRIPT_DIR/eyecare.service" "$SERVICE_FILE"

# 替换服务文件中的路径
sed -i "s|/home/lrrrryao/internship/backend/projects/eyecare|$SCRIPT_DIR|g" "$SERVICE_FILE"
sed -i "s|%i|$USER|g" "$SERVICE_FILE"

echo "服务文件已创建: $SERVICE_FILE"

# 重新加载systemd配置
systemctl --user daemon-reload

# 启用服务
systemctl --user enable eyecare.service

echo "开机自启动已启用！"
echo ""
echo "管理命令："
echo "  启动服务: systemctl --user start eyecare"
echo "  停止服务: systemctl --user stop eyecare"
echo "  查看状态: systemctl --user status eyecare"
echo "  查看日志: journalctl --user -u eyecare -f"
echo "  禁用自启动: systemctl --user disable eyecare"
echo ""
echo "注意：服务将在下次登录时自动启动。"
echo "如需立即启动，请运行: systemctl --user start eyecare"
