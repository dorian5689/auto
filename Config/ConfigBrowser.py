#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time ： 2024/3/4 22:29
@Auth ： Xq
@File ：ConfigBrowser.py
@IDE ：PyCharm
"""
import os

user_name = os.getlogin()

browser_chrome = F'C:{os.sep}Users{os.sep}{user_name}{os.sep}AppData{os.sep}Local{os.sep}Google{os.sep}Chrome{os.sep}Application{os.sep}chrome.exe'
browser_edge = F'C:{os.sep}Program Files (x86){os.sep}Microsoft{os.sep}Edge{os.sep}Application{os.sep}msedge.exe'

