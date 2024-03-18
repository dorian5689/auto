#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time ： 2024/3/4 23:18
@Auth ： Xq
@File ：ConfigUk.py
@IDE ：PyCharm
"""
import os

current_path = os.path.abspath(__file__)  # 获取当前脚本的绝对路径
parent_path = os.path.dirname(current_path)  # 获取当前脚本所在目录的父目录
parent_path = os.path.dirname(parent_path)  # 获取当前脚本所在目录的父目录


arrow =   os.path.join(parent_path,  'Image', 'uk_button', 'arrow.png')
confirm = os.path.join(parent_path, 'Image', 'uk_button', 'confirm.png')
open_button = os.path.join(parent_path,  'Image', 'uk_button', 'open_button.png')
off_all_uk = os.path.join(parent_path,  'Image', 'uk_button', 'off_all_uk.png')
use_device_name = os.path.join(parent_path,  'Image', 'uk_button', 'use_device_name.png')



