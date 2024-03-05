#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time ： 2024/3/5 1:01
@Auth ： Xq
@File ：SdkTools.py
@IDE ：PyCharm
"""
import pygetwindow

# ! /usr/bin/env python
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
from Config import ConfigHenanOmsSdk
import os
import pyautogui
from ProcessInfo.ProcessTools import ProcessCure

father_path = os.path.dirname(os.getcwd())


class SdkCurd(object):
    """
    uk操作
    """

    def __init__(self):
        pass

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

    def kill_sdk(self):
        process_name = F"iscpclient.exe"

        PT = ProcessCure()
        PT.admin_kill_process(process_name)


        # 计算exe文件的绝对路径（假设你的.py文件和.exe文件在同一级目录的上两级）
        process_name = F'C:{os.sep}Program Files{os.sep}iscpclient{os.sep}bin{os.sep}iscpclient.exe'
        if not os.path.isfile(process_name):
            process_name = F'..{os.sep}ExeSoft{os.sep}iscpclient{os.sep}bin{os.sep}iscpclient.exe'
        import subprocess
        subprocess.Popen(process_name)
        time.sleep(3)

    def open(self):
        self.kill_sdk()
        self.double_click(ConfigHenanOmsSdk.dianxin)
        self.double_click(ConfigHenanOmsSdk.link)
        self.double_click(ConfigHenanOmsSdk.confirm)
        return pygetwindow.getWindowsWithTitle('安全接入网关SDK')[0]


    def double_click(self, image):
        # x, y = self.find_icon_coordinates(image)
        # pyautogui.moveTo(x, y)
        # print(x,y)
        # pyautogui.doubleClick()
        # time.sleep(2)
        import pyautogui as pag
        location = pag.locateOnScreen(image=image, confidence=0.7)
        pag.doubleClick(location)
        time.sleep(2)


    def once_click(self, image):
        x, y = self.find_icon_coordinates(image)
        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(3)




# if __name__ == '__main__':
#     # pass
#     # SdkCurd().select_comports()
#     SdkCurd().open()
    # SdkCurd().once_click(R"D:\install_soft\code\auto\Image\uk_button\1.png")
