#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time ： 2024/3/6 17:19
@Auth ： Xq
@File ：HenanOmsDownLoad.py.py
@IDE ：PyCharm
"""
import os
current_path = os.path.abspath(__file__)  # 获取当前脚本的绝对路径
parent_path = os.path.dirname(current_path)  # 获取当前脚本所在目录的父目录
parent_path = os.path.dirname(parent_path)  # 获取当前脚本所在目录的父目录

henan_attach =   os.path.join(parent_path,  'Image', 'henan_oms_attach')

