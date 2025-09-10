#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的健康提醒调度器
"""

import sys
import os
import subprocess
import time
import signal
from datetime import datetime
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon

def format_time_display(minutes):
    """将小数分钟转换为分钟秒格式显示"""
    if minutes <= 0:
        return "0分钟"
    
    # 分离整数部分和小数部分
    whole_minutes = int(minutes)
    decimal_part = minutes - whole_minutes
    
    # 将小数部分转换为秒
    seconds = int(decimal_part * 60)
    
    if whole_minutes > 0 and seconds > 0:
        return f"{whole_minutes}分钟{seconds}秒"
    elif whole_minutes > 0:
        return f"{whole_minutes}分钟"
    else:
        return f"{seconds}秒"

# 设置环境变量以支持系统托盘
# 在Wayland环境下，尝试使用wayland平台，如果失败则回退到xcb
if os.environ.get('XDG_SESSION_TYPE') == 'wayland':
    # 在Wayland下，系统托盘支持有限，我们使用通知系统
    os.environ['QT_QPA_PLATFORM'] = 'wayland'
    print("检测到Wayland环境，将使用通知系统替代系统托盘")
else:
    os.environ['QT_QPA_PLATFORM'] = 'xcb'  # 使用X11

# 导入设置管理器
try:
    from settings_manager import SettingsManager
except ImportError:
    # 如果设置管理器不存在，使用默认值
    class SettingsManager:
        def load_settings(self):
            return {"eye_interval": 40, "water_interval": 30}
        def save_settings(self, settings):
            pass

# 通知系统类（用于Wayland环境）
class NotificationSystem:
    def __init__(self):
        self.available = self.check_notification_support()
    
    def check_notification_support(self):
        """检查系统通知支持"""
        try:
            # 尝试使用notify-send命令
            result = subprocess.run(['which', 'notify-send'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def send_notification(self, title, message, urgency='normal', timeout=5000):
        """发送系统通知"""
        if not self.available:
            print(f"通知: {title} - {message}")
            return
        
        try:
            subprocess.run([
                'notify-send',
                '-u', urgency,
                '-t', str(timeout),
                title,
                message
            ])
        except Exception as e:
            print(f"发送通知失败: {e}")
            print(f"通知: {title} - {message}")

class SimpleScheduler:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # 初始化设置管理器
        self.settings_manager = SettingsManager()
        user_settings = self.settings_manager.load_settings()
        
        # 当前设置
        self.eye_interval = user_settings.get("eye_interval", 40)  # 分钟
        self.water_interval = user_settings.get("water_interval", 30)  # 分钟
        
        # 初始化通知系统
        self.notification_system = NotificationSystem()
        
        # 状态文件路径（仅用于显示下次提醒时间）
        self.status_file = "scheduler_status.json"
        
        # 设置系统托盘
        self.tray_icon = QSystemTrayIcon()
        
        # 尝试设置图标，如果失败则使用默认图标
        try:
            # 首先尝试使用项目目录中的图标
            icon_paths = [
                "drink.png",
                "drink_water.jpg", 
                "eye/eye.jpg",
                "/usr/share/pixmaps/python3.xpm",  # 系统默认图标
                "/usr/share/icons/gnome/16x16/status/dialog-information.png"
            ]
            
            icon_set = False
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    self.tray_icon.setIcon(QIcon(icon_path))
                    icon_set = True
                    break
            
            if not icon_set:
                # 如果没有找到图标，创建一个简单的默认图标
                self.tray_icon.setIcon(self.app.style().standardIcon(self.app.style().SP_ComputerIcon))
        except Exception as e:
            print(f"设置图标时出错: {e}")
            # 使用默认图标
            self.tray_icon.setIcon(self.app.style().standardIcon(self.app.style().SP_ComputerIcon))
        
        self.tray_icon.setToolTip("健康提醒助手")
        
        # 检查系统托盘是否可用
        if not QSystemTrayIcon.isSystemTrayAvailable():
            if os.environ.get('XDG_SESSION_TYPE') == 'wayland':
                print("Wayland环境：系统托盘不可用，将使用通知系统")
                self.tray_available = False
                self.use_notifications = True
            else:
                print("系统托盘不可用，尝试启动X11会话...")
                # 在Linux上，尝试设置环境变量
                os.environ['QT_QPA_PLATFORM'] = 'xcb'
                os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
                
                # 重新检查
                if not QSystemTrayIcon.isSystemTrayAvailable():
                    print("警告: 系统托盘仍然不可用，程序将以无托盘模式运行")
                    self.tray_available = False
                    self.use_notifications = True
                else:
                    self.tray_available = True
                    self.use_notifications = False
        else:
            self.tray_available = True
            self.use_notifications = False
        
        # 创建托盘菜单
        self.create_tray_menu()
        
        # 定时器设置
        self.eye_timer = QTimer()
        self.water_timer = QTimer()
        
        # 设置定时器间隔（毫秒）
        self.eye_interval_ms = self.eye_interval * 60 * 1000
        self.water_interval_ms = self.water_interval * 60 * 1000
        
        # 连接定时器信号
        self.eye_timer.timeout.connect(self.show_eye_reminder)
        self.water_timer.timeout.connect(self.show_water_reminder)
        
        # 启动定时器
        self.start_timers()
        
        # 显示托盘图标（如果可用）
        if self.tray_available:
            self.tray_icon.show()
            # 显示启动消息
            self.show_startup_message()
        else:
            if self.use_notifications:
                print("程序已启动，使用通知系统。")
                # 显示启动通知
                self.notification_system.send_notification(
                    "健康提醒助手",
                    f"定时提醒已启动\n眼睛休息: {self.eye_interval}分钟\n喝水提醒: {self.water_interval}分钟",
                    'normal', 5000
                )
            else:
                print("程序已启动，但系统托盘不可用。程序将在后台运行。")
            print("使用 Ctrl+C 来停止程序。")
            # 设置信号处理器以便通过Ctrl+C退出
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)
    
    def create_tray_menu(self):
        """创建系统托盘菜单"""
        menu = QMenu()
        
        # 立即提醒选项
        eye_action = QAction("立即休息眼睛", self.app)
        eye_action.triggered.connect(self.show_eye_reminder)
        menu.addAction(eye_action)
        
        water_action = QAction("立即喝水提醒", self.app)
        water_action.triggered.connect(self.show_water_reminder)
        menu.addAction(water_action)
        
        menu.addSeparator()
        
        # 状态显示
        status_action = QAction("查看状态", self.app)
        status_action.triggered.connect(self.show_status)
        menu.addAction(status_action)
        
        # 设置选项
        settings_action = QAction("设置", self.app)
        settings_action.triggered.connect(self.show_settings)
        menu.addAction(settings_action)
        
        menu.addSeparator()
        
        # 退出选项
        quit_action = QAction("退出", self.app)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(menu)
    
    def start_timers(self):
        """启动定时器"""
        self.eye_timer.start(self.eye_interval_ms)
        self.water_timer.start(self.water_interval_ms)
        print(f"定时器已启动 - 眼睛休息: {self.eye_interval}分钟, 喝水提醒: {self.water_interval}分钟")
        
        # 设置定时器来定期更新状态文件（仅用于显示下次提醒时间）
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_reminder_status)
        self.status_timer.start(5000)  # 每5秒更新一次
        self.update_reminder_status()  # 立即更新一次
    
    def show_eye_reminder(self):
        """显示眼睛休息提醒 - 直接调用原始脚本"""
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 显示眼睛休息提醒")
            
            # 在Wayland环境下发送通知
            if self.use_notifications:
                self.notification_system.send_notification(
                    "眼睛休息提醒",
                    "该休息眼睛了！请看向远处或闭眼休息一下。",
                    'normal', 8000
                )
            
            # 获取当前脚本所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            eye_script = os.path.join(current_dir, "eye", "eyecare.py")
            
            if os.path.exists(eye_script):
                subprocess.Popen([sys.executable, eye_script])
            else:
                print(f"眼睛休息脚本不存在: {eye_script}")
        except Exception as e:
            print(f"显示眼睛提醒时出错: {e}")
    
    def show_water_reminder(self):
        """显示喝水提醒 - 直接调用原始脚本"""
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 显示喝水提醒")
            
            # 在Wayland环境下发送通知
            if self.use_notifications:
                self.notification_system.send_notification(
                    "喝水提醒",
                    "该喝水了！保持身体水分充足很重要。",
                    'normal', 8000
                )
            
            # 获取当前脚本所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            water_script = os.path.join(current_dir, "drink_water.py")
            
            if os.path.exists(water_script):
                subprocess.Popen([sys.executable, water_script])
            else:
                print(f"喝水提醒脚本不存在: {water_script}")
        except Exception as e:
            print(f"显示喝水提醒时出错: {e}")
    
    def show_startup_message(self):
        """显示启动消息"""
        if self.tray_available:
            self.tray_icon.showMessage(
                "健康提醒助手",
                f"定时提醒已启动\n眼睛休息: {self.eye_interval}分钟\n喝水提醒: {self.water_interval}分钟",
                QSystemTrayIcon.Information,
                3000
            )
        else:
            print(f"健康提醒助手已启动 - 眼睛休息: {self.eye_interval}分钟, 喝水提醒: {self.water_interval}分钟")
    
    def show_status(self):
        """显示当前状态"""
        next_eye = self.eye_timer.remainingTime() / 60000
        next_water = self.water_timer.remainingTime() / 60000
        
        eye_time_str = format_time_display(next_eye)
        water_time_str = format_time_display(next_water)
        
        status_msg = f"""健康提醒助手状态
        
眼睛休息提醒: {eye_time_str}后 (间隔: {self.eye_interval}分钟)
喝水提醒: {water_time_str}后 (间隔: {self.water_interval}分钟)

运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        QMessageBox.information(None, "状态信息", status_msg)
    
    def show_settings(self):
        """显示设置窗口"""
        try:
            from settings_window import SettingsWindow
            
            settings_window = SettingsWindow(
                self.eye_interval,
                self.water_interval,
                5,  # 显示时间（这个版本不需要）
                True,  # 启动消息
                self.app.activeWindow()
            )
            settings_window.settings_changed.connect(self.update_settings)
            settings_window.exec_()
        except Exception as e:
            print(f"显示设置窗口时出错: {e}")
            QMessageBox.critical(None, "错误", f"无法打开设置窗口: {e}")
    
    def update_settings(self, eye_interval, water_interval, display_time, startup_msg):
        """更新设置"""
        try:
            print(f"收到设置更新: 眼睛={eye_interval}分钟, 喝水={water_interval}分钟")
            
            # 更新当前设置
            self.eye_interval = eye_interval
            self.water_interval = water_interval
            
            # 保存设置到文件
            settings = {
                "eye_interval": eye_interval,
                "water_interval": water_interval,
                "display_time": display_time,
                "startup_message": startup_msg
            }
            self.settings_manager.save_settings(settings)
            
            # 重新计算间隔
            new_eye_interval = eye_interval * 60 * 1000
            new_water_interval = water_interval * 60 * 1000
            
            # 停止当前定时器
            self.eye_timer.stop()
            self.water_timer.stop()
            
            # 更新间隔
            self.eye_interval_ms = new_eye_interval
            self.water_interval_ms = new_water_interval
            
            # 重新启动定时器
            self.eye_timer.start(self.eye_interval_ms)
            self.water_timer.start(self.water_interval_ms)
            
            print(f"设置已更新并保存 - 眼睛休息: {eye_interval}分钟, 喝水提醒: {water_interval}分钟")
            
            # 显示更新消息
            self.tray_icon.showMessage(
                "设置已更新",
                f"眼睛休息: {eye_interval}分钟\n喝水提醒: {water_interval}分钟",
                QSystemTrayIcon.Information,
                2000
            )
            
        except Exception as e:
            print(f"更新设置时出错: {e}")
            QMessageBox.critical(None, "错误", f"更新设置失败: {e}")
    
    def update_reminder_status(self):
        """更新提醒状态文件（仅用于显示下次提醒时间）"""
        try:
            import json
            
            # 计算下次提醒时间
            next_eye_minutes = self.eye_timer.remainingTime() / 60000 if self.eye_timer.isActive() else 0
            next_water_minutes = self.water_timer.remainingTime() / 60000 if self.water_timer.isActive() else 0
            
            status = {
                "next_eye_minutes": max(0, next_eye_minutes),
                "next_water_minutes": max(0, next_water_minutes),
                "eye_interval": self.eye_interval,
                "water_interval": self.water_interval
            }
            
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(status, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"更新提醒状态失败: {e}")
    
    def signal_handler(self, signum, frame):
        """处理信号（Ctrl+C等）"""
        print("\n收到退出信号，正在关闭程序...")
        self.quit_app()
    
    def quit_app(self):
        """退出应用程序"""
        if self.tray_available:
            self.tray_icon.hide()
        
        # 清理状态文件
        try:
            if os.path.exists(self.status_file):
                os.remove(self.status_file)
        except Exception as e:
            print(f"清理状态文件失败: {e}")
            
        print("健康提醒助手正在退出...")
        self.app.quit()
    
    def run(self):
        """运行应用程序"""
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    scheduler = SimpleScheduler()
    scheduler.run()
