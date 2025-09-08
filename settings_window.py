#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置窗口 - 用于调整提醒时间间隔
"""

import sys
import os
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QSpinBox, QPushButton, QGroupBox, QFormLayout,
                             QMessageBox, QCheckBox)
from PyQt5.QtGui import QFont, QIcon

class SettingsWindow(QDialog):
    # 定义信号，用于通知主程序设置已更改
    settings_changed = pyqtSignal(int, int, int, bool)
    
    def __init__(self, current_eye_interval=40, current_water_interval=30, 
                 current_display_time=5, current_startup_msg=True, parent=None):
        super().__init__(parent)
        self.current_eye_interval = current_eye_interval
        self.current_water_interval = current_water_interval
        self.current_display_time = current_display_time
        self.current_startup_msg = current_startup_msg
        
        self.init_ui()
        self.setWindowFlags(self.windowFlags() | Qt.Tool | Qt.FramelessWindowHint)
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("健康提醒设置")
        self.setWindowIcon(QIcon("D:/Eyecare/drink.png"))
        self.resize(350, 280)
        
        # 设置窗口样式
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border: 2px solid #cccccc;
                border-radius: 10px;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QLabel {
                color: #333333;
            }
            QSpinBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QCheckBox {
                color: #333333;
            }
        """)
        
        # 主布局
        main_layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("健康提醒设置")
        title_label.setFont(QFont("微软雅黑", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # 时间设置组
        time_group = QGroupBox("提醒时间设置")
        time_layout = QFormLayout()
        
        # 眼睛休息间隔
        self.eye_spinbox = QSpinBox()
        self.eye_spinbox.setRange(1, 120)  # 1分钟到2小时
        self.eye_spinbox.setValue(self.current_eye_interval)
        self.eye_spinbox.setSuffix(" 分钟")
        time_layout.addRow("眼睛休息间隔:", self.eye_spinbox)
        
        # 喝水提醒间隔
        self.water_spinbox = QSpinBox()
        self.water_spinbox.setRange(1, 120)  # 1分钟到2小时
        self.water_spinbox.setValue(self.current_water_interval)
        self.water_spinbox.setSuffix(" 分钟")
        time_layout.addRow("喝水提醒间隔:", self.water_spinbox)
        
        # 窗口显示时间
        self.display_spinbox = QSpinBox()
        self.display_spinbox.setRange(3, 30)  # 3秒到30秒
        self.display_spinbox.setValue(self.current_display_time)
        self.display_spinbox.setSuffix(" 秒")
        time_layout.addRow("提醒窗口显示时间:", self.display_spinbox)
        
        time_group.setLayout(time_layout)
        main_layout.addWidget(time_group)
        
        # 其他设置组
        other_group = QGroupBox("其他设置")
        other_layout = QVBoxLayout()
        
        # 启动消息
        self.startup_checkbox = QCheckBox("启动时显示消息")
        self.startup_checkbox.setChecked(self.current_startup_msg)
        other_layout.addWidget(self.startup_checkbox)
        
        other_group.setLayout(other_layout)
        main_layout.addWidget(other_group)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        # 应用按钮
        self.apply_btn = QPushButton("应用设置")
        self.apply_btn.clicked.connect(self.apply_settings)
        button_layout.addWidget(self.apply_btn)
        
        # 确定按钮
        self.ok_btn = QPushButton("确定")
        self.ok_btn.clicked.connect(self.ok_clicked)
        button_layout.addWidget(self.ok_btn)
        
        # 取消按钮
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        # 设置窗口居中
        self.center_window()
    
    def center_window(self):
        """将窗口居中显示"""
        if self.parent():
            parent_geometry = self.parent().geometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
            self.move(x, y)
    
    def apply_settings(self):
        """应用设置"""
        eye_interval = self.eye_spinbox.value()
        water_interval = self.water_spinbox.value()
        display_time = self.display_spinbox.value()
        startup_msg = self.startup_checkbox.isChecked()
        
        # 验证设置
        if eye_interval < 1 or water_interval < 1:
            QMessageBox.warning(self, "设置错误", "提醒间隔不能少于1分钟！")
            return
        
        # 发送设置更改信号
        self.settings_changed.emit(eye_interval, water_interval, display_time, startup_msg)
        
        QMessageBox.information(self, "设置成功", "设置已应用！")
    
    def ok_clicked(self):
        """确定按钮点击事件"""
        self.apply_settings()
        self.accept()
    
    def mousePressEvent(self, event):
        """鼠标按下事件，用于拖拽窗口"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件，用于拖拽窗口"""
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_position'):
            self.move(event.globalPos() - self.drag_position)
            event.accept()

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec_())
