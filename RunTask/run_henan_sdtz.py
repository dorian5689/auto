#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time ： 2024/3/6 2:40
@Auth ： Xq
@File ：run_henan_sdtz.py
@IDE ：PyCharm
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import re
import time
import ddddocr
import schedule

from loguru import logger
from BrowserOperate.EdgeChromeTools import EdgeChromeCurd
from DataBaseInfo.MysqlTools import MysqlCurd
from SdkChange.SdkTools import SdkCurd
from UkChange.UkTools import UkChangeCurd
from Config.ConfigHenanOmsMysql import new_south
from Config.ConfigHenanOmsUk import off_all_uk
from Config.ConfigHenanOmsAttachUser import henan_wfname_dict_num_attach, get_henan_url
from Config.ConfigHenanOmsXpath import henan_ele_dict
from MacInfo.ChangeMAC import SetMac


class HenanOms(object):
    def __init__(self):
        self.page = EdgeChromeCurd().page
        self.UCC = UkChangeCurd()
        # 天润
        self.appkey = "dingtc3bwfk9fnqr4g7s"  # image测试
        self.appsecret = "C33oOe03_K5pitN_S2dUppBwgit2VnPW0yWnWYBM3GzogGKhdy2yFUGREl9fLICU"  # image测试
        self.chatid = "chatf3b32d9471c57b4a5a0979efdb06d087"  # image测试
        # 奈卢斯
        self.nls_appkey = "dingjk2duanbfvbywqzx"  # image测试
        self.nls_appsecret = "ICYb4-cvsvIk5DwuZY9zehc5UbpldqIClzS6uuIYFrhjU9z11guV6lold1qNqc2k"  # image测试
        self.nls_chatid = "chatf8ef1e955cf2c4e83a7e776e0011366c"  # image测试
        # 天润
        self.jf_token = F'c8eb8d7b8fe2a3c07843233bf225082126db09ab59506bd5631abef4304da29e'
        # 奈卢斯
        self.nls_token = F'acabcf918755694f2365051202cf3921a690594c1278e4b7fe960186dce58977'
        self.username = ""
        self.password = ""
        self.wfname = ""
        self.userid = ""
        self.wfname_id = ""
        self.start_run_time = ""

    def run_oms(self):
        self.login_soft()

    def now_time_hms(self):
        from datetime import datetime
        current_time = datetime.now()
        return current_time.strftime("%Y-%m-%d %H:%M:%S")

    def previous_time_d(self):
        import datetime
        current_date = datetime.date.today()
        previous_day = (current_date - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        return previous_day

    def set_mac_new(self, mac_address):
        set_mac = SetMac()
        new_mac = mac_address
        set_mac.run(new_mac)

    def login_soft(self):
        time.sleep(3)
        HC = self.UCC.open()

        report_li = []

        for i, uuid in henan_wfname_dict_num_attach.items():
            select_user_info = F"select  usb序号,UK密钥MAC地址,场站,外网oms账号,外网oms密码,wfname_id  from data_oms_uk  where usb序号='{i}' and uuid ='{uuid}'  "
            data_info = MysqlCurd(new_south).query_sql_return_header_and_data(select_user_info).values.tolist()[0]
            select_exit_true = F"SELECT 是否已完成 FROM data_oms where 电场名称='{data_info[2]}' AND 日期='{self.previous_time_d()}'"
            res_exit_ture = MysqlCurd(new_south).query_sql(select_exit_true)
            if res_exit_ture is None:
                break
            if res_exit_ture[0] == 1:
                print(F'已上报:{data_info[2]}')
                report_li.append(data_info[5])
                continue
            if HC:
                HC.maximize()
                time.sleep(2)
                try:
                    self.UCC.double_click(off_all_uk)
                except Exception as e:
                    logger.info(F'点击全部关闭--{e}')

                # HC.activate()
                self.UCC.once_click_num(i)
                logger.warning(F'选择第{i}个usb')
                HC.minimize()

            mac_address = data_info[1]
            userid = int(data_info[0])
            wfname = data_info[2]
            if wfname == '飞翔三期储能':
                return
            username = data_info[3]
            password = data_info[4]
            wfname_id = data_info[5]
            self.username = username
            self.password = password
            self.wfname = wfname
            self.userid = userid
            self.wfname_id = wfname_id
            self.start_run_time = self.now_time_hms()

            self.set_mac_new(mac_address)
            SC = SdkCurd().open()
            SC.minimize()
            logger.warning(F'SDK最小化')
            logger.warning(F'当前上报场站:{self.wfname}\n 用户名：{username}')

            self.login_web(username, password)

    def send_code(self):
        cap = self.page.ele(F'{henan_ele_dict.get("capture_img")}')
        cap.click()
        time.sleep(2)

        import os
        path = os.path.abspath(__file__)
        par_path = os.path.dirname(os.path.dirname(path))
        path = F"{par_path}{os.sep}Image{os.sep}CaptureImg"
        img_name = "验证码.png"
        img_path = F"{path}{os.sep}{img_name}"
        try:
            import shutil
            shutil.rmtree(path)
        except Exception as e:
            logger.warning(F'文件夹不存在:{path},{e}')
            pass
        cap.get_screenshot(path=img_path, name=img_name, )
        ocr = ddddocr.DdddOcr(beta=True)
        with open(img_path, 'rb') as f:
            img_bytes = f.read()
        cap_text = ocr.classification(img_bytes)
        logger.warning(f"验证码:{cap_text}")
        # 验证码长度不等于5或者包含中文字符或者不包含大写字母再次运行
        pattern = r'^\w{5}$'  # 匹配任意5位字母或数字
        if re.match(pattern, cap_text) and any(c.isdigit() for c in cap_text) and any(c.islower() for c in cap_text):
            # 确保字符串长度为5且同时包含小写字母和数字
            logger.warning(F'验证码正确:{cap_text}')
            return cap_text
        else:
            cap_text = self.send_code()
            logger.warning(F'再次验证:{cap_text}')
            return cap_text

    def login_web_again(self):
        if "欢迎登录" in self.page.html:
            cap_text = self.send_code()
            time.sleep(3)
            self.page.ele(F'{henan_ele_dict.get("capture_img_frame")}').input(cap_text)
            time.sleep(3)

            self.page.ele(F'{henan_ele_dict.get("login_button")}').click()
            time.sleep(3)
            self.page.wait

            # 登录按钮
        if "验证码" in self.page.html:
            time.sleep(3)

            cap_text = self.send_code()
            time.sleep(3)

            self.page.ele(F'{henan_ele_dict.get("capture_img_frame")}').input(cap_text)
            self.page.ele(F'{henan_ele_dict.get("login_button")}').click()  # 登录按钮
            self.page.wait

        if "解析密码错误" in self.page.html:
            time.sleep(3)

            cap_text = self.send_code()
            self.page.ele(F'{henan_ele_dict.get("capture_img_frame")}').input(cap_text)
            self.page.ele(F'{henan_ele_dict.get("login_button")}').click()  # 登录按钮
            self.page.wait

        if "风险防控系统" not in self.page.html:
            cap_text = self.send_code()
            time.sleep(3)

            self.page.ele(F'{henan_ele_dict.get("capture_img_frame")}').input(cap_text)
            self.page.ele(F'{henan_ele_dict.get("login_button")}').click()  # 登录按钮
            self.page.wait

        if "锁定" in self.page.html:
            return

    def exit_username_login(self):

        try:
            time.sleep(2)
            res = self.page.ele('x://*[@id="app"]/section/header/div/div[2]/div/div/span').click()
            self.page.ele('x:/html/body/ul/li[1]/span').click()
            self.page.ele('x:/html/body/div[2]/div/div[3]/button[2]').click()
            self.page.wait
            logger.info(F'退出用户成功')
        except Exception as e:
            logger.info(F'退出用户失败--{e}')

    def save_pic_attach(self, table0):
        import os
        from pathlib import Path
        img_path = Path(f"..{os.sep}Image{os.sep}attach{os.sep}{self.previous_time_d()}{os.sep}")
        directory = img_path.parent

        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)

        # 对整页截图并保存
        save_wind_wfname = F"{img_path}{os.sep}{self.wfname}附件.png"

        table0.get_screenshot(path=save_wind_wfname, full_page=True)

        return save_wind_wfname

    def send_ding_attach_message(self, table0, message, attach_file):
        time.sleep(2)
        from DingInfo.DingBotMix import DingApiTools
        # 天润
        DAT = DingApiTools(appkey_value=self.appkey, appsecret_value=self.appsecret, chatid_value=self.chatid)
        DAT.push_message(self.jf_token, message)
        DAT.send_file(F'{attach_file}', 1)

        # 奈卢斯
        DATNLS = DingApiTools(appkey_value=self.nls_appkey, appsecret_value=self.nls_appsecret,
                              chatid_value=self.nls_chatid)

        DATNLS.push_message(self.nls_token, message)
        DATNLS.send_file(F'{attach_file}', 1)

        # self.update_mysql()

    def login_web(self, username, password):
        self.page.get("https://www.baidu.com", retry=2)
        self.page.close_tabs(others='other')
        time.sleep(2)
        self.page.get(get_henan_url, retry=2)

        try:
            self.exit_username_login()
            time.sleep(2)

        except Exception as e:
            logger.info(F'退出用户登录！{e}')
        self.page.get(get_henan_url, retry=2)
        try:
            self.exit_username_login()
            time.sleep(2)

        except Exception as e:
            logger.info(F'退出用户登录！{e}')
        self.page(F'{henan_ele_dict.get("input_text")}').input(username)
        self.page(F'{henan_ele_dict.get("input_password")}').input(password)
        self.page.ele(F'{henan_ele_dict.get("capture_img_frame")}').input(self.send_code())
        self.page.ele(F'{henan_ele_dict.get("login_button")}').click()
        self.page.wait
        try:
            self.login_web_again()
        except Exception as e:
            logger.warning(F'二次登录--{e}')
        try:
            self.page.ele(F'{henan_ele_dict.get("oms_button")}').click()
        except:
            return
        time.sleep(1)
        table0 = self.page.get_tab(0)
        try:
            table0.ele(F'{henan_ele_dict.get("sditz")}').click()
            table0.ele(F'{henan_ele_dict.get("sdtz")}').click()

            DICT_ = {}
            for i in range(1, 3):
                henan_oms_attach_li = []
                for j in range(2, 10):
                    aa = table0.ele(F'x://*[@id="{i}$cell${j}"]/div').text
                    if j != 9:
                        henan_oms_attach_li.append(aa)

                    if j == 9:
                        table0.ele(F'x://*[@id="{i}$cell${j}"]/div').click()
                        from Config.ConfigHenanOmsDownLoad import henan_attach
                        down_load_folder_path = henan_attach
                        # down_load_folder_path = F'{henan_attach}{os.sep}henan_oms_attach'
                        table0.set.download_path(down_load_folder_path)

                        for num in range(1, 5):
                            try:
                                import shutil
                                folder_path = down_load_folder_path
                                if os.path.exists(folder_path):  # 检查路径是否存在
                                    shutil.rmtree(folder_path)  # 删除包括子文件和子文件夹在内的整个目录
                                else:
                                    logger.warning(F'文件夹不存在:{folder_path}')
                                try:
                                    attach_name = table0.ele(
                                        f'x://*[@id="app"]/div/div/div/table/tbody/tr[3]/td/a[{num}]').text
                                    table0.set.download_file_name(attach_name)

                                    table0.ele(f'x://*[@id="app"]/div/div/div/table/tbody/tr[3]/td/a[{num}]').click()
                                    logger.warning(F'正在下载:{attach_name}')
                                except:

                                    txt_name = F'{folder_path}{os.sep}{henan_oms_attach_li[0]}'
                                    attach_name = henan_oms_attach_li[0]
                                    txt_content = str(table0.html)
                                    with open(txt_name, 'w', encoding='utf-8') as f:
                                        f.write(str(txt_content))

                                table0.wait.download_begin()
                                # self.page.wait.all_download_done()
                                logger.warning(F'下载完成:{attach_name}')

                                henan_oms_attach_li.append(attach_name)
                                for root, dirs, files in os.walk(down_load_folder_path):
                                    for file in files:
                                        old_file_path = os.path.join(root, file)
                                        new_file_path = os.path.join(root, attach_name)
                                        os.rename(old_file_path, F'{new_file_path}')

                                fbsj_ = table0.ele(F'x://*[@id="{i}$cell${j - 1}"]/div').text
                                # fbsj_ = '2024-03-14 16:15'
                                from datetime import datetime
                                given_date = datetime.strptime(fbsj_, '%Y-%m-%d %H:%M')
                                now = datetime.now()
                                today = now.date()

                                # 比较日期是否相等
                                if given_date.date() == today:
                                    # 推送钉钉
                                    pass
                                    fkjzrq_ = henan_oms_attach_li[2].strip()
                                    if not fkjzrq_:
                                        fkjzrq_ = '空'
                                    fksj_ = henan_oms_attach_li[4].strip()
                                    if not fksj_:
                                        fksj_ = '空'
                                    message = {
                                        "msgtype": "markdown",
                                        "markdown": {
                                            "title": "附件信息推送",
                                            "text":
                                                F'省调通知<br>'
                                                F'主题：{henan_oms_attach_li[0]}<br>'
                                                F'是否需反馈：{henan_oms_attach_li[1]}<br>'
                                                F'反馈截至日期：{fkjzrq_}<br>'
                                                F'处理信息：{henan_oms_attach_li[3]}<br>'
                                                F'反馈时间：{fksj_}<br>'
                                                F'发布人：{henan_oms_attach_li[5]}<br>'
                                                F'发布时间：{henan_oms_attach_li[6]}<br>'
                                                F'详情见附件：{henan_oms_attach_li[7]}<br>'
                                        }
                                    }
                                    self.send_ding_attach_message(table0, message,
                                                                  attach_file=F'{folder_path}{os.sep}{attach_name}')

                                with open(F'{folder_path}{os.sep}{attach_name}', 'rb') as file:
                                    binary_data = file.read()
                                # 这里处理文件上传
                                henan_oms_attach_li.append(binary_data)
                                table_name = F'data_oms_notification_table'
                                field_name = ['subject', 'needs_feedback', 'feedback_deadline', 'processing_info',
                                              'feedback_time',
                                              'publisher', 'publish_time', 'attachment_name', 'attachment_data']
                                field_data = henan_oms_attach_li
                                MysqlCurd().insert_list(table_name, field_name, field_data)
                                logger.warning(F'添加数据成功')
                                import shutil

                                folder_path = down_load_folder_path
                                if os.path.exists(folder_path):  # 检查路径是否存在
                                    shutil.rmtree(folder_path)  # 删除包括子文件和子文件夹在内的整个目录
                                else:
                                    logger.warning(F'文件夹不存在:{folder_path}')
                                time.sleep(5)
                            except:
                                continue
                    table0.refresh()
                    logger.warning(F'当前数据:{henan_oms_attach_li}')
                DICT_[i] = henan_oms_attach_li

            try:
                self.exit_username_login()
                time.sleep(2)
            except Exception as e:
                logger.warning(F'退出oms登录页！--{e}')
                pass
        except:
            pass

    def exit_username_oms(self, table0):
        table0.ele('x://*[@id="app"]/section/header/div/div[2]/div[1]/div/span').click()
        table0.ele('x://html/body/ul/li[1]/span').click()

        table0.ele('x://*[@id="app"]/section/header/div/div[2]/div[1]/div/span').click()
        table0.ele('x://html/body/ul/li[4]/span').click()
        try:
            table0.ele('x://html/body/div[28]/div/div[3]/button[2]/span').click()
            time.sleep(1)
        except Exception as e:
            print(F'重新退出用户测试!--{e}')
            table0.ele('x://html/body/div[23]/div/div[3]/button[2]/span').click()
            time.sleep(1)

        time.sleep(1)


def run_henan_oms_attach():
    for _ in range(5):
        try:
            EdgeChromeCurd().open_baidu()
            HenanOms().run_oms()
        except Exception as e:
            logger.warning(F'主函数异常:{e}')


if __name__ == '__main__':

    run_henan_oms_attach()

    # schedule.every().day.at("14:00").do(run_henan_oms_attach)
    # # run_henan_oms()
    # # run_henan_sxz()
    # while True:
    #     schedule.run_pending()
    #
    #     time.sleep(1)
