#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time ： 2024/3/4 22:07
@Auth ： Xq
@File ：EdgeChrome.py
@IDE ：PyCharm
"""
import time

import os
from loguru import logger
from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage._pages.chromium_page import ChromiumPage
from Config import ConfigBrowser


class EdgeChromeCurd(object):
    """
    处理浏览器
    """

    def __init__(self):
        self.page = self.get_page()

    def get_page(self):
        """
        初始化浏览器
        """
        try:
            page = self.default_browser(ConfigBrowser.browser_chrome)
            logger.info(F"使用默认浏览器chrome")

        except Exception as e:
            page = self.default_browser(ConfigBrowser.browser_edge)
            logger.warning(F'使用默认浏览器edge{e}')
        return page

    def default_browser(self, browser_path):
        """
        默认浏览器
        """
        co = ChromiumOptions().set_paths(browser_path=browser_path).ignore_certificate_errors()
        co.set_argument("--start-maximized")
        return ChromiumPage(co)

    def open_baidu(self):
        ECT = EdgeChromeCurd()
        page = ECT.page
        page.get("https://www.baidu.com")
        time.sleep(3)

        page.quit()

# if __name__ == '__main__':
#     ECT = EdgeChromeCurd()
#     ECT.page.get("https://www.baidu.com")