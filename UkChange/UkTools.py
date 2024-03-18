#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time ： 2024/3/4 23:07
@Auth ： Xq
@File ：UkTools.py
@IDE ：PyCharm
"""
import time

import cv2
import numpy as np
import mss
from loguru import logger
from Config import ConfigHenanOmsUk
import os
import pyautogui
from ProcessInfo.ProcessTools import ProcessCure
import pygetwindow

father_path = os.path.dirname(os.getcwd())


class UkChangeCurd(object):
    """
    uk操作
    """

    def __init__(self):
        self.com_usb_index = 0

    def select_comports(self):
        """
        选择uk串口号
        """
        import serial.tools.list_ports
        num_device = 0
        index = 0
        ls_com = serial.tools.list_ports.comports()
        res = []
        for i in ls_com:
            res.append(str(i))
        # res = [str(i) for i in ls_com]

        # 使用正则表达式提取COM口号码
        import re
        # 提取每个元素中的COM口号码
        com_numbers = [re.search(r'\((COM\d+)\)', item).group(1) for item in res]

        # 根据COM口号码排序并重新构建列表
        sorted_res = ['{} - {}'.format('COM{}'.format(num), item)
                      for num, item in sorted(zip(com_numbers, res))]

        for i in sorted_res:
            i = str(i)
            index += 1
            if 'USB' in i:
                num_device = i[-2]
                self.com_usb_index = index
        if num_device == 0:
            return
        logger.info(F'选择串口号:{num_device}')
        return num_device

    def find_icon_coordinates(self, image):
        # 加载要识别的图片
        # icon = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        icon = cv2.imdecode(np.fromfile(image, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

        # 创建 MSS (Media Source) 对象
        with mss.mss() as sct:
            # 获取屏幕分辨率
            monitor = sct.monitors[1]  # 通常使用 monitor 1，根据你的设置而定

            # 截取整个屏幕
            screenshot = sct.shot(output="screenshot.png")

        # 加载要搜索的图像
        screenshot = cv2.imread('screenshot.png', cv2.IMREAD_GRAYSCALE)

        # 使用模板匹配来查找图片位置
        result = cv2.matchTemplate(screenshot, icon, cv2.TM_CCOEFF_NORMED)

        # 设置阈值，找到匹配的位置
        threshold = 0.99
        locations = np.where(result >= threshold)

        # 提取匹配位置的坐标
        icon_height, icon_width = icon.shape
        coordinates = list(zip(*locations[::-1]))  # 反转坐标

        # 在原始截图上绘制矩形框显示匹配位置
        for (x, y) in coordinates:
            cv2.rectangle(screenshot, (x, y), (x + icon_width, y + icon_height), (0, 255, 0), 2)

        # 保存包含标记的结果图像
        cv2.imwrite('result.png', screenshot)
        if len(coordinates) > 3:
            return coordinates[-1]
        else:
            return coordinates[0]

    def kill_uk(self):
        process_name = F"HUB_Control通用版.exe"

        PT = ProcessCure()
        PT.admin_kill_process(process_name)

        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 计算exe文件的绝对路径（假设你的.py文件和.exe文件在同一级目录的上两级）
        exe_path = os.path.join(current_dir, '..', 'ExeSoft', 'HUB_Control通用版', 'HUB_Control通用版.exe')
        import subprocess
        subprocess.Popen(exe_path)
        time.sleep(3)

    def open(self):
        self.kill_uk()
        self.choose_device()
        self.double_click(ConfigHenanOmsUk.open_button)
        self.double_click(ConfigHenanOmsUk.confirm)
        self.double_click(ConfigHenanOmsUk.off_all_uk)
        return pygetwindow.getWindowsWithTitle('HUB_Control通用版 示例程序')[0]

    def double_click(self, image):
        x, y = self.find_icon_coordinates(image)
        pyautogui.moveTo(x, y)
        pyautogui.doubleClick()
        time.sleep(2)

    def once_click_num(self,num):
        filename_prefix = str(num)
        filename = f"{filename_prefix}.png"

        import os
        current_path = os.path.abspath(__file__)  # 获取当前脚本的绝对路径
        parent_path = os.path.dirname(current_path)  # 获取当前脚本所在目录的父目录
        parent_path = os.path.dirname(parent_path)  # 获取当前脚本所在目录的父目录
        full_path = os.path.join(parent_path, 'Image', 'HenanOmsUkButton', F'{filename}')



        # directory = os.path.abspath(os.path.join('..', 'Image', 'HenanOmsUkButton'))
        # full_path = os.path.join(directory, filename)
        self.once_click(full_path)
        time.sleep(2)


    def once_click(self, image):
        x, y = self.find_icon_coordinates(image)
        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(3)

    def choose_device(self):
        x, y = self.find_icon_coordinates(ConfigHenanOmsUk.arrow)
        from pynput.mouse import Controller
        # 创建鼠标控制器
        mouse = Controller()
        mouse.position = (x, y)
        num = self.select_comports()
        mouse.scroll(0, -int(num))

# if __name__ == '__main__':
# pass
# UkChangeCurd().select_comports()
# UkChangeCurd().open()
# UkChangeCurd().once_click(R"D:\install_soft\code\auto\Image\uk_button\1.png")
