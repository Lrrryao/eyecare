#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置管理器 - 用于保存和加载用户设置
"""

import json
import os

class SettingsManager:
    def __init__(self, config_file="user_settings.json"):
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_file)
        self.default_settings = {
            "eye_interval": 40,
            "water_interval": 30,
            "display_time": 5,
            "startup_message": True
        }
    
    def load_settings(self):
        """加载用户设置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    # 确保所有必要的键都存在
                    for key, default_value in self.default_settings.items():
                        if key not in settings:
                            settings[key] = default_value
                    return settings
            else:
                return self.default_settings.copy()
        except Exception as e:
            print(f"加载设置时出错: {e}")
            return self.default_settings.copy()
    
    def save_settings(self, settings):
        """保存用户设置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            print(f"设置已保存到: {self.config_file}")
            return True
        except Exception as e:
            print(f"保存设置时出错: {e}")
            return False
    
    def get_setting(self, key, default=None):
        """获取单个设置值"""
        settings = self.load_settings()
        return settings.get(key, default if default is not None else self.default_settings.get(key))
    
    def set_setting(self, key, value):
        """设置单个设置值"""
        settings = self.load_settings()
        settings[key] = value
        return self.save_settings(settings)
    
    def reset_to_default(self):
        """重置为默认设置"""
        return self.save_settings(self.default_settings.copy())

if __name__ == '__main__':
    # 测试设置管理器
    manager = SettingsManager()
    
    # 测试加载
    settings = manager.load_settings()
    print("当前设置:", settings)
    
    # 测试保存
    test_settings = {
        "eye_interval": 45,
        "water_interval": 25,
        "display_time": 8,
        "startup_message": False
    }
    
    if manager.save_settings(test_settings):
        print("设置保存成功")
    
    # 测试加载
    loaded_settings = manager.load_settings()
    print("加载的设置:", loaded_settings)
