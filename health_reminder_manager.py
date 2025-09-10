#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康提醒管理器 - 独立设置界面
用于在Wayland环境下管理健康提醒程序
"""

import sys
import os
import subprocess
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QSpinBox, QPushButton, 
                             QTextEdit, QGroupBox, QMessageBox, QSystemTrayIcon,
                             QMenu, QAction, QCheckBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QFont

# 设置环境变量
os.environ['QT_QPA_PLATFORM'] = 'wayland' if os.environ.get('XDG_SESSION_TYPE') == 'wayland' else 'xcb'

class HealthReminderManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scheduler_process = None
        self.settings_file = "user_settings.json"
        self.status_file = "scheduler_status.json"
        self.init_ui()
        self.load_settings()
        self.check_scheduler_status()
        
        # 设置定时器来定期更新状态显示
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_reminder_display)
        self.status_timer.start(5000)  # 每5秒更新一次
        
        # 立即执行一次状态更新
        self.update_reminder_display()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("健康提醒管理器")
        self.setGeometry(100, 100, 500, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 状态显示区域
        self.create_status_section(layout)
        
        # 设置区域
        self.create_settings_section(layout)
        
        # 控制按钮区域
        self.create_control_section(layout)
        
        # 日志显示区域
        self.create_log_section(layout)
        
        # 状态栏
        self.statusBar().showMessage("健康提醒管理器已就绪")
        
    def create_status_section(self, layout):
        """创建状态显示区域"""
        group = QGroupBox("程序状态")
        group_layout = QVBoxLayout(group)
        
        self.status_label = QLabel("状态: 未运行")
        self.status_label.setStyleSheet("font-weight: bold; color: red;")
        group_layout.addWidget(self.status_label)
        
        self.next_reminder_label = QLabel("下次提醒: 未知")
        group_layout.addWidget(self.next_reminder_label)
        
        layout.addWidget(group)
        
    def create_settings_section(self, layout):
        """创建设置区域"""
        group = QGroupBox("提醒设置")
        group_layout = QVBoxLayout(group)
        
        # 眼睛休息间隔
        eye_layout = QHBoxLayout()
        eye_layout.addWidget(QLabel("眼睛休息间隔 (分钟):"))
        self.eye_interval_spin = QSpinBox()
        self.eye_interval_spin.setRange(1, 120)
        self.eye_interval_spin.setValue(40)
        eye_layout.addWidget(self.eye_interval_spin)
        eye_layout.addStretch()
        group_layout.addLayout(eye_layout)
        
        # 喝水提醒间隔
        water_layout = QHBoxLayout()
        water_layout.addWidget(QLabel("喝水提醒间隔 (分钟):"))
        self.water_interval_spin = QSpinBox()
        self.water_interval_spin.setRange(1, 120)
        self.water_interval_spin.setValue(30)
        water_layout.addWidget(self.water_interval_spin)
        water_layout.addStretch()
        group_layout.addLayout(water_layout)
        
        # 启动时显示消息
        self.startup_msg_check = QCheckBox("启动时显示通知")
        self.startup_msg_check.setChecked(True)
        group_layout.addWidget(self.startup_msg_check)
        
        # 应用按钮
        apply_layout = QHBoxLayout()
        self.apply_btn = QPushButton("应用设置")
        self.apply_btn.clicked.connect(self.apply_settings)
        apply_layout.addWidget(self.apply_btn)
        apply_layout.addStretch()
        group_layout.addLayout(apply_layout)
        
        layout.addWidget(group)
        
    def create_control_section(self, layout):
        """创建控制按钮区域"""
        group = QGroupBox("程序控制")
        group_layout = QVBoxLayout(group)
        
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("启动提醒程序")
        self.start_btn.clicked.connect(self.start_scheduler)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("停止提醒程序")
        self.stop_btn.clicked.connect(self.stop_scheduler)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)
        
        self.restart_btn = QPushButton("重启程序")
        self.restart_btn.clicked.connect(self.restart_scheduler)
        button_layout.addWidget(self.restart_btn)
        
        group_layout.addLayout(button_layout)
        
        # 测试按钮
        test_layout = QHBoxLayout()
        self.test_eye_btn = QPushButton("测试眼睛提醒")
        self.test_eye_btn.clicked.connect(self.test_eye_reminder)
        test_layout.addWidget(self.test_eye_btn)
        
        self.test_water_btn = QPushButton("测试喝水提醒")
        self.test_water_btn.clicked.connect(self.test_water_reminder)
        test_layout.addWidget(self.test_water_btn)
        
        group_layout.addLayout(test_layout)
        
        layout.addWidget(group)
        
    def create_log_section(self, layout):
        """创建日志显示区域"""
        group = QGroupBox("运行日志")
        group_layout = QVBoxLayout(group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(150)
        self.log_text.setReadOnly(True)
        group_layout.addWidget(self.log_text)
        
        # 清空日志按钮
        clear_btn = QPushButton("清空日志")
        clear_btn.clicked.connect(self.clear_log)
        group_layout.addWidget(clear_btn)
        
        layout.addWidget(group)
        
    def log_message(self, message):
        """添加日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        
    def clear_log(self):
        """清空日志"""
        self.log_text.clear()
        
    def load_settings(self):
        """加载设置"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.eye_interval_spin.setValue(settings.get('eye_interval', 40))
                    self.water_interval_spin.setValue(settings.get('water_interval', 30))
                    self.startup_msg_check.setChecked(settings.get('startup_message', True))
                    self.log_message("设置已加载")
        except Exception as e:
            self.log_message(f"加载设置失败: {e}")
            
    def save_settings(self):
        """保存设置"""
        try:
            settings = {
                'eye_interval': self.eye_interval_spin.value(),
                'water_interval': self.water_interval_spin.value(),
                'startup_message': self.startup_msg_check.isChecked(),
                'display_time': 5  # 保持兼容性
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            self.log_message("设置已保存")
            return True
        except Exception as e:
            self.log_message(f"保存设置失败: {e}")
            return False
    
    def apply_settings(self):
        """应用设置并更新运行中的程序"""
        try:
            # 保存设置到文件
            if not self.save_settings():
                QMessageBox.warning(self, "错误", "保存设置失败")
                return
            
            # 检查程序是否在运行
            result = subprocess.run(['pgrep', '-f', 'simple_scheduler.py'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                # 程序正在运行，需要重启以应用新设置
                self.log_message("检测到程序正在运行，正在重启以应用新设置...")
                
                # 停止当前程序
                subprocess.run(['pkill', '-f', 'simple_scheduler.py'], 
                             capture_output=True, text=True)
                
                # 等待程序完全停止
                import time
                time.sleep(1)
                
                # 重新启动程序
                subprocess.Popen([sys.executable, 'simple_scheduler.py'])
                
                self.log_message("程序已重启，新设置已应用")
                
                # 更新UI状态
                QTimer.singleShot(2000, self.check_scheduler_status)
                
                # 显示成功消息
                QMessageBox.information(self, "设置已应用", 
                                      f"新设置已应用并重启程序：\n"
                                      f"眼睛休息间隔: {self.eye_interval_spin.value()}分钟\n"
                                      f"喝水提醒间隔: {self.water_interval_spin.value()}分钟")
            else:
                # 程序未运行，只保存设置
                self.log_message("程序未运行，设置已保存，下次启动时将使用新设置")
                QMessageBox.information(self, "设置已保存", 
                                      f"设置已保存：\n"
                                      f"眼睛休息间隔: {self.eye_interval_spin.value()}分钟\n"
                                      f"喝水提醒间隔: {self.water_interval_spin.value()}分钟\n"
                                      f"下次启动程序时将使用新设置")
                
        except Exception as e:
            self.log_message(f"应用设置失败: {e}")
            QMessageBox.critical(self, "错误", f"应用设置失败: {e}")
            
    def check_scheduler_status(self):
        """检查调度器状态"""
        try:
            result = subprocess.run(['pgrep', '-f', 'simple_scheduler.py'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.status_label.setText("状态: 正在运行")
                self.status_label.setStyleSheet("font-weight: bold; color: green;")
                self.start_btn.setEnabled(False)
                self.stop_btn.setEnabled(True)
                self.log_message("检测到提醒程序正在运行")
                self.update_reminder_display()
            else:
                self.status_label.setText("状态: 未运行")
                self.status_label.setStyleSheet("font-weight: bold; color: red;")
                self.start_btn.setEnabled(True)
                self.stop_btn.setEnabled(False)
                self.next_reminder_label.setText("下次提醒: 程序未运行")
        except Exception as e:
            self.log_message(f"检查状态失败: {e}")
    
    def update_reminder_display(self):
        """更新提醒时间显示"""
        try:
            # 检查程序是否在运行
            result = subprocess.run(['pgrep', '-f', 'simple_scheduler.py'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                # 程序正在运行，尝试读取状态文件
                if os.path.exists(self.status_file):
                    with open(self.status_file, 'r', encoding='utf-8') as f:
                        status = json.load(f)
                        
                    next_eye = status.get('next_eye_minutes', 0)
                    next_water = status.get('next_water_minutes', 0)
                    
                    if next_eye > 0 and next_water > 0:
                        # 显示两个提醒的剩余时间
                        display_text = f"下次提醒: 眼睛休息({next_eye:.1f}分钟) | 喝水({next_water:.1f}分钟)"
                        self.next_reminder_label.setText(display_text)
                        self.log_message(f"状态更新: {display_text}")
                    else:
                        self.next_reminder_label.setText("下次提醒: 计算中...")
                        self.log_message(f"状态数据: 眼睛={next_eye}, 喝水={next_water}")
                else:
                    self.next_reminder_label.setText("下次提醒: 状态文件不存在")
            else:
                self.next_reminder_label.setText("下次提醒: 程序未运行")
        except Exception as e:
            self.next_reminder_label.setText(f"下次提醒: 状态检查失败 - {str(e)}")
    
    def start_scheduler(self):
        """启动调度器"""
        # 启动前先保存当前设置
        if not self.save_settings():
            QMessageBox.warning(self, "错误", "保存设置失败，无法启动程序")
            return
            
        try:
            # 启动后台进程
            self.scheduler_process = subprocess.Popen([
                sys.executable, 'simple_scheduler.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.log_message("正在启动健康提醒程序...")
            self.status_label.setText("状态: 正在启动...")
            self.status_label.setStyleSheet("font-weight: bold; color: orange;")
            
            # 延迟检查状态
            QTimer.singleShot(2000, self.check_scheduler_status)
            
        except Exception as e:
            self.log_message(f"启动失败: {e}")
            QMessageBox.critical(self, "错误", f"启动程序失败: {e}")
            
    def stop_scheduler(self):
        """停止调度器"""
        try:
            # 查找并终止进程
            result = subprocess.run(['pkill', '-f', 'simple_scheduler.py'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log_message("健康提醒程序已停止")
                self.status_label.setText("状态: 已停止")
                self.status_label.setStyleSheet("font-weight: bold; color: red;")
                self.start_btn.setEnabled(True)
                self.stop_btn.setEnabled(False)
                self.next_reminder_label.setText("下次提醒: 程序未运行")
                
                # 清理状态文件
                if os.path.exists(self.status_file):
                    os.remove(self.status_file)
            else:
                self.log_message("停止程序失败")
                
        except Exception as e:
            self.log_message(f"停止失败: {e}")
            QMessageBox.critical(self, "错误", f"停止程序失败: {e}")
            
    def restart_scheduler(self):
        """重启调度器"""
        self.log_message("正在重启程序...")
        self.stop_scheduler()
        QTimer.singleShot(1000, self.start_scheduler)
        
    def test_eye_reminder(self):
        """测试眼睛提醒"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            eye_script = os.path.join(current_dir, "eye", "eyecare.py")
            
            if os.path.exists(eye_script):
                subprocess.Popen([sys.executable, eye_script])
                self.log_message("已发送眼睛休息提醒")
            else:
                self.log_message(f"眼睛休息脚本不存在: {eye_script}")
                QMessageBox.warning(self, "警告", "眼睛休息脚本不存在")
        except Exception as e:
            self.log_message(f"测试眼睛提醒失败: {e}")
            
    def test_water_reminder(self):
        """测试喝水提醒"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            water_script = os.path.join(current_dir, "drink_water.py")
            
            if os.path.exists(water_script):
                subprocess.Popen([sys.executable, water_script])
                self.log_message("已发送喝水提醒")
            else:
                self.log_message(f"喝水提醒脚本不存在: {water_script}")
                QMessageBox.warning(self, "警告", "喝水提醒脚本不存在")
        except Exception as e:
            self.log_message(f"测试喝水提醒失败: {e}")
            
    def closeEvent(self, event):
        """关闭事件"""
        reply = QMessageBox.question(self, '确认退出', 
                                   '确定要退出健康提醒管理器吗？\n'
                                   '注意：这不会停止后台运行的提醒程序。',
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("健康提醒管理器")
    
    # 检查是否已经有实例在运行
    if QSystemTrayIcon.isSystemTrayAvailable():
        # 尝试创建系统托盘图标
        tray_icon = QSystemTrayIcon()
        if tray_icon.isSystemTrayAvailable():
            tray_icon.setIcon(app.style().standardIcon(app.style().SP_ComputerIcon))
            tray_icon.setToolTip("健康提醒管理器")
            tray_icon.show()
    
    window = HealthReminderManager()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
