#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的健康提醒调度器
"""

import sys
import os
import subprocess
import time
from datetime import datetime
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon

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
        
        # 设置系统托盘
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(QIcon("D:/Eyecare/Eyecare/drink.png"))
        self.tray_icon.setToolTip("健康提醒助手")
        
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(None, "系统托盘", "系统托盘不可用")
            sys.exit(1)
        
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
        
        # 显示托盘图标
        self.tray_icon.show()
        
        # 显示启动消息
        self.show_startup_message()
    
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
    
    def show_eye_reminder(self):
        """显示眼睛休息提醒 - 直接调用原始脚本"""
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 显示眼睛休息提醒")
            # 直接调用原始的眼睛休息脚本
            subprocess.Popen([sys.executable, "D:/Eyecare/Eyecare/eye/eyecare.py"])
        except Exception as e:
            print(f"显示眼睛提醒时出错: {e}")
    
    def show_water_reminder(self):
        """显示喝水提醒 - 直接调用原始脚本"""
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 显示喝水提醒")
            # 直接调用原始的喝水提醒脚本
            subprocess.Popen([sys.executable, "D:/Eyecare/Eyecare/drink_water.py"])
        except Exception as e:
            print(f"显示喝水提醒时出错: {e}")
    
    def show_startup_message(self):
        """显示启动消息"""
        self.tray_icon.showMessage(
            "健康提醒助手",
            f"定时提醒已启动\n眼睛休息: {self.eye_interval}分钟\n喝水提醒: {self.water_interval}分钟",
            QSystemTrayIcon.Information,
            3000
        )
    
    def show_status(self):
        """显示当前状态"""
        next_eye = self.eye_timer.remainingTime() / 60000
        next_water = self.water_timer.remainingTime() / 60000
        
        status_msg = f"""健康提醒助手状态
        
眼睛休息提醒: {next_eye:.1f}分钟后 (间隔: {self.eye_interval}分钟)
喝水提醒: {next_water:.1f}分钟后 (间隔: {self.water_interval}分钟)

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
    
    def quit_app(self):
        """退出应用程序"""
        self.tray_icon.hide()
        self.app.quit()
    
    def run(self):
        """运行应用程序"""
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    scheduler = SimpleScheduler()
    scheduler.run()
