#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time ： 2024/3/14 0:37
@Auth ： Xq
@File ：run_henan_qxjc.py
@IDE ：PyCharm
"""

# 河南缺陷检测

import os
import re
import time
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ddddocr
import schedule
from loguru import logger
from BrowserOperate.EdgeChromeTools import EdgeChromeCurd
from DataBaseInfo.HenanOmsMysql.henan_oms_config_new import henan_oms_config_new_sql
from DataBaseInfo.MysqlTools import MysqlCurd
from SdkChange.SdkTools import SdkCurd
from UkChange.UkTools import UkChangeCurd
from Config.ConfigHenanOmsMysql import new_south
from Config.ConfigHenanOmsUk import off_all_uk
from Config.ConfigHenanOmsUser import henan_wfname_dict_num, get_henan_url
from Config.ConfigHenanOmsXpath import henan_ele_dict
from MacInfo.ChangeMAC import SetMac
from Config.ConfigHenanOmsMarkDown import henan_oms_dict_num_qxjc


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
        self.message_dl = {}
        self.message_cn = {}
        self.message_cn3 = {}
        self.message_oms_ycxjx_yjh, self.message_oms_ycxjx_zjh, self.message_oms_ycxjx_rjh = {}, {}, {}
        self.message_oms_ecxjx_zdhzjh, self.message_oms_ecxjx_wnjxjh, self.message_oms_qxgl_czsbqxl = {}, {}, {}

        self.start_run_time = ""

    def run_oms(self):
        for i in range(5):
            try:
                self.login_soft()
            except Exception as e:
                logger.warning(F"{e}")
                pass
            logger.warning(F"循环上报5次数,第{i + 1}次上报完成")

        logger.warning(F'当日上报完成@！')

    def run_oms_qxjc(self):
        for i in range(5):
            try:
                self.login_soft_qxjc()
            except Exception as e:
                logger.warning(F"{e}")
                pass
            logger.warning(F"循环上报5次数,第{i + 1}次上报完成")

        logger.warning(F'当日上报完成@！')

    def run_sxz(self):
        self.login_soft()

    def now_time_hms(self):
        """
        年-月-日 时:分:秒
        """
        from datetime import datetime
        current_time = datetime.now()
        return current_time.strftime("%Y-%m-%d %H:%M:%S")

    def now_time_ymd(self):
        """
        年-月-日
        """
        from datetime import datetime
        current_time = datetime.now()
        return current_time.strftime("%Y-%m-%d")

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

        HC = self.UCC.open()

        report_li = []

        for i, uuid in henan_wfname_dict_num.items():
            select_user_info = F"select  usb序号,UK密钥MAC地址,场站,外网oms账号,外网oms密码,wfname_id  from data_oms_uk  where usb序号='{i}' and uuid ='{uuid}'  "
            data_info = MysqlCurd(new_south).query_sql_return_header_and_data(select_user_info).values.tolist()[0]
            select_exit_true = F"SELECT 是否已完成 FROM data_oms where 电场名称='{data_info[2]}' AND 日期='{self.previous_time_d()}'"
            res_exit_ture = MysqlCurd(new_south).query_sql(select_exit_true)
            if res_exit_ture is None:
                break
            if res_exit_ture[0][0] == 1:
                report_li.append(data_info[5])
                logger.warning(F'已经上报第{data_info[0]}个场站:{data_info[2]}')
                continue
            if HC:
                HC.maximize()
                time.sleep(2)
                try:
                    self.UCC.double_click(off_all_uk)
                except Exception as e:
                    logger.info(F'点击全部关闭__{e}')

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

    def login_soft_qxjc(self):

        HC = self.UCC.open()

        report_li = []

        for i, uuid in henan_wfname_dict_num.items():
            select_user_info = F"select  usb序号,UK密钥MAC地址,场站,外网oms账号,外网oms密码,wfname_id  from data_oms_uk  where usb序号='{i}' and uuid ='{uuid}'  "
            data_info = MysqlCurd(new_south).query_sql_return_header_and_data(select_user_info).values.tolist()[0]
            select_exit_true = F"SELECT 是否已完成 FROM data_oms where 电场名称='{data_info[2]}' AND 日期='{self.previous_time_d()}'"
            res_exit_ture = MysqlCurd(new_south).query_sql(select_exit_true)
            if res_exit_ture is None:
                break
            if res_exit_ture[0][0] == 1:
                report_li.append(data_info[5])
                logger.warning(F'已经上报第{data_info[0]}个场站:{data_info[2]}')
                # continue
                pass
            if HC:
                HC.maximize()
                time.sleep(2)
                try:
                    self.UCC.double_click(off_all_uk)
                except Exception as e:
                    logger.info(F'点击全部关闭__{e}')

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

            self.login_web_qxjc(username, password)

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
            print(f'文件夹删除失败:{e}')
            pass
        cap.get_screenshot(path=img_path, name=img_name, )
        ocr = ddddocr.DdddOcr(beta=True)
        with open(img_path, 'rb') as f:
            img_bytes = f.read()
        cap_text = ocr.classification(img_bytes)
        print(f"验证码:{cap_text}")
        # 验证码长度不等于5或者包含中文字符或者不包含大写字母再次运行
        pattern = r'^\w{5}$'  # 匹配任意5位字母或数字
        if re.match(pattern, cap_text) and any(c.isdigit() for c in cap_text) and any(c.islower() for c in cap_text):
            # 确保字符串长度为5且同时包含小写字母和数字
            print(F'验证码正确:{cap_text}')
            return cap_text

        # if len(cap_text) == 5 and cap_text.isalnum() and cap_text.islower():
        #     print(F'验证码正确:{cap_text}')
        #     return cap_text
        else:
            cap_text = self.send_code()
            print(F'再次验证:{cap_text}')
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
            res = self.page.ele('x://*[@id="app"]/section/header/div/div[2]/div/div/span').click()
            self.page.ele('x:/html/body/ul/li[1]/span').click()
            self.page.ele('x:/html/body/div[2]/div/div[3]/button[2]').click()
            self.page.wait
            logger.info(F'退出用户成功')
        except Exception as e:
            logger.info(F'退出用户失败__{e}')

    def login_web(self, username, password):
        self.page.get("https://www.baidu.com", retry=2)
        self.page.close_tabs(others='other')
        time.sleep(2)
        # self.page.set.window.fullscreen()
        self.page.get(get_henan_url, retry=2)

        try:
            self.exit_username_login()
            time.sleep(2)

        except Exception as e:
            logger.info(F'退出用户登录！{e}')
        self.page.get(get_henan_url, retry=2)
        # self.page.wait
        self.page(F'{henan_ele_dict.get("input_text")}').input(username)
        self.page(F'{henan_ele_dict.get("input_password")}').input(password)
        self.page.ele(F'{henan_ele_dict.get("capture_img_frame")}').input(self.send_code())
        self.page.ele(F'{henan_ele_dict.get("login_button")}').click()
        self.page.wait
        try:
            self.login_web_again()
        except Exception as e:
            logger.warning(F'二次登录__{e}')
        henan_oms_data = self.get_henan_data()
        try:
            self.page.ele(F'{henan_ele_dict.get("oms_button")}').click()
        except:
            return
        time.sleep(1)
        table0 = self.page.get_tab(0)
        try:
            self.report_load_dl(table0, henan_oms_data)
            try:
                self.exit_username_login()
                time.sleep(2)
            except Exception as e:
                logger.warning(F'退出oms登录页！__{e}')
                pass
        except:
            pass
        try:
            if self.userid in [6, 8, 11]:
                self.report_load_cn(table0, henan_oms_data)
        except Exception as e:
            print(F'6810 __-{e}')
            pass
        try:
            if self.userid in [10]:
                henan_oms_data3 = self.henan_data3()
                self.report_load_cn3(table0, henan_oms_data, henan_oms_data3)
        except Exception as e:
            print(F'第{self.userid}有问题:{e}')
            pass

    def login_web_qxjc(self, username, password):
        self.page.get("https://www.baidu.com", retry=2)
        time.sleep(2)

        self.page.close_tabs(others='other')
        time.sleep(2)
        # self.page.set.window.fullscreen()
        self.page.get(get_henan_url, retry=2)
        time.sleep(2)

        try:
            self.exit_username_login()
            time.sleep(2)

        except Exception as e:
            logger.info(F'退出用户登录！{e}')
        self.page.get(get_henan_url, retry=2)
        # self.page.wait
        self.page(F'{henan_ele_dict.get("input_text")}').input(username)
        self.page(F'{henan_ele_dict.get("input_password")}').input(password)
        self.page.ele(F'{henan_ele_dict.get("capture_img_frame")}').input(self.send_code())
        self.page.ele(F'{henan_ele_dict.get("login_button")}').click()
        self.page.wait
        try:
            self.login_web_again()
        except Exception as e:
            logger.warning(F'二次登录__{e}')
        try:
            self.page.ele(F'{henan_ele_dict.get("oms_button")}').click()
        except:
            return
        time.sleep(1)
        table0 = self.page.get_tab(0)
        try:
            self.report_ycxjxjh(table0)
            try:
                self.exit_username_login()
                time.sleep(2)
            except Exception as e:
                logger.warning(F'退出oms登录页！__{e}')
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
            print(F'重新退出用户测试!__{e}')
            table0.ele('x://html/body/div[23]/div/div[3]/button[2]/span').click()
            time.sleep(1)

        time.sleep(1)

    def get_henan_data(self):

        data_info = MysqlCurd(new_south).query_sql_return_header_and_data(henan_oms_config_new_sql)
        henan_oms_data1 = data_info.loc[
            (data_info['电场名称'] == self.wfname) & (data_info['日期'] == self.previous_time_d()), ['发电量',
                                                                                                     '上网电量',
                                                                                                     '弃电量',
                                                                                                     '储能最大充电电力',
                                                                                                     '储能最大放电电力',
                                                                                                     '储能日充电',
                                                                                                     '储能日放电',
                                                                                                     '充电次数',
                                                                                                     '放电次数']]

        # data_info = MysqlCurd(new_south).query_sql(henan_oms_config_new_sql)

        import numpy as np
        henan_oms_data = np.nan_to_num(henan_oms_data1.values.tolist()[0])
        logger.info(f'{henan_oms_data}')
        return henan_oms_data

    def report_load_dl(self, table0, henan_oms_data):
        table0.ele(F'{henan_ele_dict.get("report_load")}').click()
        print(F'点击了收报负荷！')
        table0.ele(F'{henan_ele_dict.get("report_load_button_dl")}').click()
        self.page.wait
        # todo 这里是测试数据是否准确
        fdl = henan_oms_data[0]
        swdl = henan_oms_data[1]
        qdl = henan_oms_data[2]
        message_dl = {
            "msgtype": "markdown",
            "markdown": {
                "title": "OMS推送",
                "text":
                    F'第{self.wfname_id}个场站:{self.wfname}__已上报__电量__郑州集控<br>'
                    F'发电量:{fdl}<br>上网电量:{swdl}<br>弃电量:{qdl}<br>',
            }
        }
        self.message_dl = message_dl
        # 测试电量专用
        # self.send_ding_dl_true_or_false(table0, message_dl=message_dl)
        # pass

        if self.previous_time_d() == table0.ele(F'{henan_ele_dict.get("upload_date")}').text:
            self.send_ding_dl(table0)
        else:
            table0.ele(F'{henan_ele_dict.get("send_battery")}').input(F'{henan_oms_data[0]}\ue007')
            table0.ele(F'{henan_ele_dict.get("upload_battery")}').input(F'{henan_oms_data[1]}\ue007')
            table0.ele(F'{henan_ele_dict.get("abandoned_battery")}').input(F'{henan_oms_data[2]}\ue007')
            self.upload_button_dl(table0)
        try:
            if self.userid in [6, 8, 11]:
                self.report_load_cn(table0, henan_oms_data)
        except Exception as e:
            print(F'6810 __-{e}')
            pass

        try:
            if self.userid in [10]:
                henan_oms_data3 = self.henan_data3()
                self.report_load_cn3(table0, henan_oms_data, henan_oms_data3)
        except Exception as e:
            print(F'第{self.userid}有问题:{e}')
            pass
        table0.close()

    def report_ycxjxjh(self, table0):

        """
        一次性检修计划__月计划
        """

        table0.ele(F'{henan_ele_dict.get("oms_ycxjxjh")}').click()
        logger.warning(F'点击了一次性检修计划')
        # 一次性检修计划_月计划
        self.report_ycxjxjh_yjh(table0)
        table0.wait
        # 一次性检修计划_周检修
        self.report_ycxjxjh_zjh(table0)
        table0.wait

        # 一次性检修计划_日检修
        self.report_ycxjxjh_rjh(table0)
        table0.wait

        table0.ele(F'{henan_ele_dict.get("oms_ecjxjh")}').click()
        table0.wait

        logger.warning(F'点击了二次性检修计划')
        # 二次性检修计划_自动化检修计划
        self.report_ecxjxjh_zdjxjh_zdzjh(table0)
        table0.wait

        self.report_ecxjxjh_zdjxjh_zdhjjjx(table0)
        table0.wait

        self.report_ecxjxjh_zdjxjh_zdrjh(table0)
        table0.wait
        self.report_ecxjxjh_zdjxjh_zdrjhlc(table0)
        table0.wait

        table0.ele(F'{henan_ele_dict.get("oms_ecjxjh_wajxjh")}').click()
        table0.wait

        logger.warning(F'点击了二次性检修计划_网安检修计划')
        # 二次性检修计划_网安检修计划
        self.report_ecxjxjh_wajcjh_wazjhgl(table0)
        table0.wait

        self.report_ecxjxjh_wajcjh_warjhlc(table0)
        table0.wait

        # 缺陷管理
        table0.ele(F'{henan_ele_dict.get("oms_qxgl")}').click()
        table0.wait
        logger.warning(F'点击了缺陷管理')
        # 缺陷管理_场站设备缺陷
        table0.ele(F'{henan_ele_dict.get("oms_qxgl_czsbqxl")}').click()
        logger.warning(F'点击了缺陷管理_场站设备缺陷')
        self.report_oms_qxgl_czsbqxl_qxlcgl(table0)

        # 退出当前用户
        try:
            self.exit_username_oms(table0)
        except:
            pass
        try:
            self.exit_username_login()
        except:
            pass

    def report_ycxjxjh_yjh(self, table0):

        table0.ele(F'{henan_ele_dict.get("oms_ycxjxjh_yjh")}').click()
        table0.wait

        logger.warning(F'点击了一次性检修计划_月计划')
        table0.ele(F'{henan_ele_dict.get("oms_ycxjxjh_yjh_fdjx")}').click()
        table0.wait

        logger.warning(F'点击了一次性检修计划_月计划_发电检修')
        table0.ele(F'{henan_ele_dict.get("oms_ycxjxjh_yjh_fdjx_fdyjhst")}').click()
        table0.wait

        logger.warning(F'点击了一次性检修计划_月计划_发电检修_发电月计划视图')

        table0.ele(F'{henan_ele_dict.get("oms_ycxjxjh_zdhjxjh_yjh_fdjx_fdyjhst_nian")}').input(F'{2024}\ue007')
        table0.wait

        logger.warning(F'点击了一次性检修计划__月计划__发电检修__发电月计划视图__年')
        table0.ele(F'{henan_ele_dict.get("oms_ycxjxjh_zdhjxjh_yjh_fdjx_fdyjhst_yue")}').input(F'{3}\ue007')
        table0.wait

        logger.warning(F'点击了一次性检修计划__月计划__发电检修__发电月计划视图__月')
        table0.ele(F'{henan_ele_dict.get("oms_ycxjxjh_zdhjxjh_yjh_fdjx_fdyjhst_cx")}').click()
        table0.wait

        logger.warning(F'点击了一次性检修计划__月计划__发电检修__发电月计划视图__查询')
        # 推送到定性

        if 1 == 1:
            henan_oms_dict_num_qxjc.get("message_oms_ycxjx_yjh")["markdown"][
                "text"] = F'第{self.wfname_id}个场站__{self.wfname}_{henan_oms_dict_num_qxjc.get("message_oms_ycxjx_yjh")["markdown"]["text"]}'
            self.oms_ycxjx_yjh = henan_oms_dict_num_qxjc.get("message_oms_ycxjx_yjh")
            self.send_ding_qxjc_message(table0, self.oms_ycxjx_yjh)
            henan_oms_dict_num_qxjc.get("message_oms_ycxjx_yjh")["markdown"][
                "text"] = henan_oms_dict_num_qxjc.get("message_oms_ycxjx_yjh")["markdown"]["text"].replace(
                F"第{self.wfname_id}个场站__{self.wfname}_", "")
            logger.warning(F'一次性检修计划__月计划__发电检修__发电月计划视图,已上报')

    def report_ycxjxjh_zjh(self, table0):

        table0.ele(F'{henan_ele_dict.get("oms_ycxjxjh_zjh")}').click()
        table0.wait

        logger.warning(F'点击了一次性检修计划__周计划')
        table0.ele(F'{henan_ele_dict.get("oms_ycxjxjh_zdhjxjh_zjh_fdjx")}').click()
        table0.wait
        logger.warning(F'点击了一次性检修计划__周计划__发电检修')

        table0.ele(F'{henan_ele_dict.get("oms_ycxjxjh_zdhjxjh_zjh_fdjx_fdzjhst")}').click()
        table0.wait
        logger.warning(F'点击了一次性检修计划__周计划__发电检修__发电周计划视图')
        time.sleep(3)
        table0.ele(F'{henan_ele_dict.get("oms_ycxjxjh_zdhjxjh_zjh_fdjx_fdzjhst_cx")}').click()
        table0.wait
        logger.warning(F'点击了一次性检修计划__周计划__发电检修__发电周计划视图__查询')
        # 推送到定性

        if 1 == 1:
            henan_oms_dict_num_qxjc.get("message_oms_ycxjx_zjh")["markdown"][
                "text"] = F'第{self.wfname_id}个场站__{self.wfname}_{henan_oms_dict_num_qxjc.get("message_oms_ycxjx_zjh")["markdown"]["text"]}'

            self.message_oms_ycxjx_zjh = henan_oms_dict_num_qxjc.get("message_oms_ycxjx_zjh")
            self.send_ding_qxjc_message(table0, self.message_oms_ycxjx_zjh)
            henan_oms_dict_num_qxjc.get("message_oms_ycxjx_zjh")["markdown"]["text"] = \
                henan_oms_dict_num_qxjc.get("message_oms_ycxjx_zjh")["markdown"]["text"].replace(
                    F"第{self.wfname_id}个场站__{self.wfname}_", "")
            logger.warning(F'一次性检修计划__周计划__发电检修__发电周计划视图,已上报')
        time.sleep(3)

    def report_ycxjxjh_rjh(self, table0):

        table0.ele(F'{henan_ele_dict.get("oms_ycxjxjh_rjh")}').click()
        table0.wait

        logger.warning(F'点击了一次性检修计划__日计划')
        table0.ele(F'{henan_ele_dict.get("oms_ycxjxjh_rjh_fdjx")}').click()
        table0.wait

        logger.warning(F'点击了一次性检修计划__日计划__发电检修')
        table0.ele(F'{henan_ele_dict.get("oms_ycxjxjh_rjh_fdjx_fdrjhst")}').click()
        table0.wait

        logger.warning(F'点击了一次性检修计划__日计划__发电检修__发电日计划视图')
        time.sleep(3)
        # table0.ele(F'{henan_ele_dict.get("oms_ycxjxjh_rjh_fdjx_fdrjhst_cx")}').click()
        table0.wait
        logger.warning(F'点击了一次性检修计划__日计划__发电检修__发电日计划视图__查询')

        if 1 == 1:
            henan_oms_dict_num_qxjc.get("message_oms_ycxjx_rjh")["markdown"][
                "text"] = F'第{self.wfname_id}个场站__{self.wfname}_{henan_oms_dict_num_qxjc.get("message_oms_ycxjx_rjh")["markdown"]["text"]}'

            self.message_oms_ycxjx_rjh = henan_oms_dict_num_qxjc.get("message_oms_ycxjx_rjh")
            self.send_ding_qxjc_message(table0, self.message_oms_ycxjx_rjh)
            henan_oms_dict_num_qxjc.get("message_oms_ycxjx_rjh")["markdown"][
                "text"] = henan_oms_dict_num_qxjc.get("message_oms_ycxjx_rjh")["markdown"][
                "text"].replace(F"第{self.wfname_id}个场站__{self.wfname}_", "")
            logger.warning(F'一次性检修计划__日计划__发电检修__发电日计划视图,已上报')
        time.sleep(3)

    def report_ecxjxjh_zdjxjh_zdzjh(self, table0):

        table0.ele(F'{henan_ele_dict.get("oms_ecjxjh_zdhjxjh")}').click()
        table0.wait

        logger.warning(F'点击了二次性检修计划__自动检修计划')
        table0.ele(F'{henan_ele_dict.get("oms_ecjxjh_zdjxjh_zdhzjh")}').click()
        table0.wait

        logger.warning(F'点击了二次性检修计划__自动检修计划__自动化周计划')
        time.sleep(3)
        # table0.ele(F'已上报').click()
        table0.wait

        if 1 == 1:
            # todo  表格待做
            henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhzjh")["markdown"][
                "text"] = F'第{self.wfname_id}个场站__{self.wfname}_{henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhzjh")["markdown"]["text"]}'

            self.message_oms_ecxjx_zdhzjh = henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhzjh")
            self.send_ding_qxjc_message(table0, self.message_oms_ecxjx_zdhzjh)
            henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhzjh")["markdown"][
                "text"] = henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhzjh")["markdown"][
                "text"].replace(F"第{self.wfname_id}个场站__{self.wfname}_", "")
            logger.warning(F'二次性检修计划__自动检修计划__自动化周计划已上报')
        time.sleep(3)

    def report_ecxjxjh_zdjxjh_zdhjjjx(self, table0):

        table0.ele(F'{henan_ele_dict.get("oms_ecjxjh_zdjxjh_zdhjjjx")}').click()
        table0.wait

        logger.warning(F'点击了二次性检修计划__自动检修计划__自动化紧急检修')
        time.sleep(3)
        # table0.ele(F'已上报').click()
        table0.wait

        if 1 == 1:
            # todo  表格待做
            henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhjjjx")["markdown"][
                "text"] = F'第{self.wfname_id}个场站__{self.wfname}_{henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhjjjx")["markdown"]["text"]}'

            self.message_oms_ecxjx_zdhzjh = henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhjjjx")
            self.send_ding_qxjc_message(table0, self.message_oms_ecxjx_zdhzjh)
            henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhjjjx")["markdown"][
                "text"] = henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhjjjx")["markdown"][
                "text"].replace(F"第{self.wfname_id}个场站__{self.wfname}_", "")
            logger.warning(F'二次性检修计划__自动检修计划__自动化紧急检修已上报')
        time.sleep(3)

    def report_ecxjxjh_zdjxjh_zdrjh(self, table0):

        table0.ele(F'{henan_ele_dict.get("oms_ecjxjh_zdjxjh_zdhrjh")}').click()
        table0.wait

        logger.warning(F'点击了二次性检修计划__自动检修计划__自动化日计划')
        time.sleep(3)
        # table0.ele(F'已上报').click()
        table0.wait

        if 1 == 1:
            # todo  表格待做
            henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhrjh")["markdown"][
                "text"] = F'第{self.wfname_id}个场站__{self.wfname}_{henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhrjh")["markdown"]["text"]}'

            self.message_oms_ecxjx_zdhzjh = henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhrjh")
            self.send_ding_qxjc_message(table0, self.message_oms_ecxjx_zdhzjh)
            henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhrjh")["markdown"][
                "text"] = henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhrjh")["markdown"][
                "text"].replace(F"第{self.wfname_id}个场站__{self.wfname}_", "")
            logger.warning(F'二次性检修计划__自动检修计划__自动化日计划已上报')
        time.sleep(3)

    def report_ecxjxjh_zdjxjh_zdrjhlc(self, table0):

        table0.ele(F'{henan_ele_dict.get("oms_ecjxjh_zdjxjh_zdhrjhlc")}').click()
        table0.wait

        logger.warning(F'点击了二次检修计划_自动化检修计划_自动化日计划流程')
        time.sleep(3)

        # table0.ele(F'流转中').click()
        table0.wait

        if 1 == 1:
            # todo  表格待做
            henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhrjhlc")["markdown"][
                "text"] = F'第{self.wfname_id}个场站__{self.wfname}_{henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhrjhlc")["markdown"]["text"]}'

            self.message_oms_ecxjx_wnjxjh = henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhrjhlc")
            self.send_ding_qxjc_message(table0, self.message_oms_ecxjx_wnjxjh)
            henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhrjhlc")["markdown"][
                "text"] = henan_oms_dict_num_qxjc.get("message_oms_ecxjx_zdhzjh_zdhrjhlc")["markdown"][
                "text"].replace(F"第{self.wfname_id}个场站__{self.wfname}_", "")
            logger.warning(F'二次检修计划_自动化检修计划_自动化日计划流程已上报')
        time.sleep(3)

    def report_ecxjxjh_wajcjh_wazjhgl(self, table0):

        table0.ele(F'{henan_ele_dict.get("oms_ecjxjh_wajxjh_wazjhgl")}').click()
        table0.wait

        logger.warning(F'点击了二次检修计划_网安检修计划_网安周计划管理')
        time.sleep(3)

        # table0.ele(F'已上报').click()
        table0.wait

        if 1 == 1:
            # todo  表格待做
            henan_oms_dict_num_qxjc.get("message_oms_ecxjx_wajxjh_wazjggl")["markdown"][
                "text"] = F'第{self.wfname_id}个场站__{self.wfname}_{henan_oms_dict_num_qxjc.get("message_oms_ecxjx_wajxjh_wazjggl")["markdown"]["text"]}'

            self.message_oms_ecxjx_wnjxjh = henan_oms_dict_num_qxjc.get("message_oms_ecxjx_wajxjh_wazjggl")
            self.send_ding_qxjc_message(table0, self.message_oms_ecxjx_wnjxjh)
            henan_oms_dict_num_qxjc.get("message_oms_ecxjx_wajxjh_wazjggl")["markdown"][
                "text"] = henan_oms_dict_num_qxjc.get("message_oms_ecxjx_wajxjh_wazjggl")["markdown"][
                "text"].replace(F"第{self.wfname_id}个场站__{self.wfname}_", "")
            logger.warning(F'二次检修计划_网安检修计划_网安周计划管理已上报')
        time.sleep(3)

    def report_ecxjxjh_wajcjh_warjhlc(self, table0):

        table0.ele(F'{henan_ele_dict.get("oms_ecjxjh_wajxjh_warlhlcgl")}').click()
        table0.wait

        logger.warning(F'点击了二次检修计划_网安检修计划_网安日计划流程管理')
        time.sleep(3)

        # table0.ele(F'已上报').click()
        table0.wait

        if 1 == 1:
            # todo  表格待做
            henan_oms_dict_num_qxjc.get("message_oms_ecxjx_wajxjh_wazrjhlcgl")["markdown"][
                "text"] = F'第{self.wfname_id}个场站__{self.wfname}_{henan_oms_dict_num_qxjc.get("message_oms_ecxjx_wajxjh_wazrjhlcgl")["markdown"]["text"]}'

            self.message_oms_ecxjx_wnjxjh = henan_oms_dict_num_qxjc.get("message_oms_ecxjx_wajxjh_wazrjhlcgl")
            self.send_ding_qxjc_message(table0, self.message_oms_ecxjx_wnjxjh)
            henan_oms_dict_num_qxjc.get("message_oms_ecxjx_wajxjh_wazrjhlcgl")["markdown"][
                "text"] = henan_oms_dict_num_qxjc.get("message_oms_ecxjx_wajxjh_wazrjhlcgl")["markdown"][
                "text"].replace(F"第{self.wfname_id}个场站__{self.wfname}_", "")
            logger.warning(F'二次检修计划_网安检修计划_网安日计划流程管理已上报')
        time.sleep(3)

    def report_oms_qxgl_czsbqxl_qxlcgl(self, table0):

        table0.ele(F'{henan_ele_dict.get("oms_qxgl_czsbqxl_qxlcgl")}').click()
        table0.wait

        logger.warning(F'点击了缺陷管理_场站设备缺陷(老)')
        time.sleep(3)

        # table0.ele(f'流转中').click()
        table0.wait

        if 1 == 1:
            # todo  表格待做
            henan_oms_dict_num_qxjc.get("message_oms_qxgl_czsbqxl")["markdown"][
                "text"] = F'第{self.wfname_id}个场站__{self.wfname}_{henan_oms_dict_num_qxjc.get("message_oms_qxgl_czsbqxl")["markdown"]["text"]}'

            self.message_oms_qxgl_czsbqxl = henan_oms_dict_num_qxjc.get("message_oms_qxgl_czsbqxl")
            self.send_ding_qxjc_message(table0, self.message_oms_qxgl_czsbqxl)
            henan_oms_dict_num_qxjc.get("message_oms_qxgl_czsbqxl")["markdown"][
                "text"] = henan_oms_dict_num_qxjc.get("message_oms_qxgl_czsbqxl")["markdown"][
                "text"].replace(F"第{self.wfname_id}个场站__{self.wfname}_", "")
            logger.warning(F'缺陷管理__场站设备缺陷(老)__产站设备缺陷__已上报')

    def report_load_cn3(self, table0, henan_oms_data, henan_oms_data3):
        time.sleep(2)

        table0.ele(F'{henan_ele_dict.get("report_load_button_cn")}').click()

        # todo 这里是测试储能数据是否准确
        cnrzdcddl = henan_oms_data[3]  # 储能日最大充电电力
        cnrzdfddl = henan_oms_data[4]  # 储能日最大放电电力
        cnrcdl = henan_oms_data[5]  # 储能日充电量
        cnrfdl = henan_oms_data[6]  # 储能日放电量
        cnrcdcs = henan_oms_data[7]  # 储能日充电次数
        cnrfdcs = henan_oms_data[8]  # 储能日放电次数

        # todo 这里是测试储能3期数数据是否准确
        cnrzdcddl3 = henan_oms_data3[3]  # 储能日最大充电电力
        cnrzdfddl3 = henan_oms_data3[4]  # 储能日最大放电电力
        cnrcdl3 = henan_oms_data3[5]  # 储能日充电量
        cnrfdl3 = henan_oms_data3[6]  # 储能日放电量
        cnrcdcs3 = henan_oms_data3[7]  # 储能日充电次数
        cnrfdcs3 = henan_oms_data3[8]  # 储能日放电次数
        self.message_cn3 = {
            "msgtype": "markdown",
            "markdown": {
                "title": "OMS推送",
                "text":
                    F'第{self.wfname_id}个场站:{self.wfname}__已上报__储能__郑州集控<br>'
                    F'储能日最大充电电力:{cnrzdcddl}<br>储能日最大放电电力:{cnrzdfddl}<br>'
                    F'储能日充电量:{cnrcdl}<br>储能日放电量:{cnrfdl}<br>'
                    F'储能日充电次数:{cnrcdcs}<br>储能日放电次数:{cnrfdcs}<br>'
                    F'第二行数据<br>'
                    F'储能日最大充电电力:{cnrzdcddl3}<br>储能日最大放电电力:{cnrzdfddl3}<br>'
                    F'储能日充电量:{cnrcdl3}<br>储能日放电量:{cnrfdl3}<br>'
                    F'储能日充电次数:{cnrcdcs3}<br>储能日放电次数:{cnrfdcs3}<br>'

            }
        }

        # #  测试三期储能专用
        # self.send_ding_cn3_true_or_false(table0, message_cn3=message_cn3)
        # pass

        if self.previous_time_d() == table0.ele(F'{henan_ele_dict.get("upload_date")}').text:
            time.sleep(5)
            self.send_ding_cn3(table0)
        else:
            # 飞翔储能
            table0.ele(F'{henan_ele_dict.get("store_energy_max_charge_power_day")}').input(
                F'{float(henan_oms_data[3])}\ue007')
            table0.ele(F'{henan_ele_dict.get("store_energy_max_discharge_power_day")}').input(
                F'{henan_oms_data[4]}\ue007')
            table0.ele(F'{henan_ele_dict.get("store_energy_day_charge_power")}').input(
                F'{henan_oms_data[5]}\ue007')
            table0.ele(F'{henan_ele_dict.get("store_energy_day_discharge_power")}').input(
                F'{henan_oms_data[6]}\ue007')
            table0.ele(F'{henan_ele_dict.get("store_energy_day_charge_power_times")}').input(
                F'{int(henan_oms_data[7])}\ue007')
            table0.ele(F'{henan_ele_dict.get("store_energy_day_discharge_power_times")}').input(
                F'{int(henan_oms_data[8])}\ue007')
            #
            # 飞翔储能三期

            table0.ele(F'{henan_ele_dict.get("store_energy_max_charge_power_day3")}').input(
                F'{float(henan_oms_data3[3])}\ue007')
            table0.ele(F'{henan_ele_dict.get("store_energy_max_discharge_power_day3")}').input(
                F'{henan_oms_data3[4]}\ue007')
            table0.ele(F'{henan_ele_dict.get("store_energy_day_charge_power3")}').input(
                F'{henan_oms_data3[5]}\ue007')
            table0.ele(F'{henan_ele_dict.get("store_energy_day_discharge_power3")}').input(
                F'{henan_oms_data3[6]}\ue007')
            table0.ele(F'{henan_ele_dict.get("store_energy_day_charge_power_times3")}').input(
                F'{int(henan_oms_data3[7])}\ue007')
            table0.ele(F'{henan_ele_dict.get("store_energy_day_discharge_power_times3")}').input(
                F'{int(henan_oms_data3[8])}\ue007')
            time.sleep(3)
            self.upload_button_cn3(table0)

    def upload_button_cn3(self, table0):
        self.upload_button(table0)
        time.sleep(5)
        self.send_ding_cn3(table0)
        try:
            self.send_ding_cn3(table0)
        except Exception as e:
            pass

    def send_ding_cn3(self, table0):
        time.sleep(3)
        save_wind_wfname = self.save_pic_cn(table0)
        from DingInfo.DingBotMix import DingApiTools
        # 天润
        DAT = DingApiTools(appkey_value=self.appkey, appsecret_value=self.appsecret, chatid_value=self.chatid)
        DAT.push_message(self.jf_token, self.message_cn3)
        DAT.send_file(F'{save_wind_wfname}', 0)

        # 奈卢斯
        DATNLS = DingApiTools(appkey_value=self.nls_appkey, appsecret_value=self.nls_appsecret,
                              chatid_value=self.nls_chatid)
        DATNLS.push_message(self.nls_token, self.message_cn3)
        DATNLS.send_file(F'{save_wind_wfname}', 0)

        self.update_mysql3()

    def update_mysql3(self):

        update_sql_success = F"update   data_oms  set  是否已完成 =1 ,填报开始时间 = '{self.start_run_time}',填报结束时间 = '{self.now_time_hms()}' where   日期='{self.previous_time_d()}' and 电场名称='{self.wfname}'"

        NEWMC = MysqlCurd(new_south)
        NEWMC.update(update_sql_success)
        try:
            fxsqcn = F'飞翔三期储能'
            update_sql_success3 = F"update   data_oms  set  是否已完成 =1 ,填报开始时间 = '{self.start_run_time}',填报结束时间 = '{self.now_time_hms()}' where   日期='{self.previous_time_d()}' and 电场名称='{fxsqcn}'"
            NEWMC.update(update_sql_success3)
        except:
            pass

    def henan_data3(self):

        data_info = MysqlCurd(new_south).query_sql_return_header_and_data(henan_oms_config_new_sql)

        time.sleep(1)
        henan_oms_data1 = data_info.loc[
            (data_info['电场名称'] == "飞翔三期储能") & (data_info['日期'] == self.previous_time_d()), ['发电量',
                                                                                                        '上网电量',
                                                                                                        '弃电量',
                                                                                                        '储能最大充电电力',
                                                                                                        '储能最大放电电力',
                                                                                                        '储能日充电',
                                                                                                        '储能日放电',
                                                                                                        '充电次数',
                                                                                                        '放电次数']]

        import numpy as np
        henan_oms_data = np.nan_to_num(henan_oms_data1.values.tolist()[0])
        return henan_oms_data

    def report_load_cn(self, table0, henan_oms_data):
        time.sleep(4)

        # table0.ele(F'{henan_ele_dict.get("report_load")}').click()
        table0.ele(F'{henan_ele_dict.get("report_load_button_cn")}').click()
        time.sleep(2)
        # todo 这里是测试储能数据是否准确
        cnrzdcddl = henan_oms_data[3]  # 储能日最大充电电力
        cnrzdfddl = henan_oms_data[4]  # 储能日最大放电电力
        cnrcdl = henan_oms_data[5]  # 储能日充电量
        cnrfdl = henan_oms_data[6]  # 储能日放电量
        cnrcdcs = henan_oms_data[7]  # 储能日充电次数
        cnrfdcs = henan_oms_data[8]  # 储能日放电次数
        self.message_cn = {
            "msgtype": "markdown",
            "markdown": {
                "title": "OMS推送",
                "text":
                    F'第{self.wfname_id}个场站:{self.wfname}__已上报__储能__郑州集控<br>'
                    F'储能日最大充电电力:{cnrzdcddl}<br>储能日最大放电电力:{cnrzdfddl}<br>'
                    F'储能日充电量:{cnrcdl}<br>储能日放电量:{cnrfdl}<br>'
                    F'储能日充电次数:{cnrcdcs}<br>储能日放电次数:{cnrfdcs}<br>'

            }
        }
        if self.previous_time_d() == table0.ele(F'{henan_ele_dict.get("upload_date")}').text:
            self.send_ding_cn(table0)

        # #  测试储能专用
        # self.send_ding_cn_true_or_false(table0, message_cn=message_cn)
        # pass

        # #
        cnrzdcddl = henan_oms_data[3]  # 储能日最大充电电力
        cnrzdfddl = henan_oms_data[4]  # 储能日最大放电电力
        cnrcdl = henan_oms_data[5]  # 储能日充电量
        cnrfdl = henan_oms_data[6]  # 储能日放电量
        cnrcdcs = henan_oms_data[7]  # 储能日充电次数
        cnrfdcs = henan_oms_data[8]  # 储能日放电次数
        table0.ele(F'{henan_ele_dict.get("store_energy_max_charge_power_day")}').input(
            F'{float(henan_oms_data[3])}\ue007')
        table0.ele(F'{henan_ele_dict.get("store_energy_max_discharge_power_day")}').input(
            F'{henan_oms_data[4]}\ue007')
        table0.ele(F'{henan_ele_dict.get("store_energy_day_charge_power")}').input(
            F'{henan_oms_data[5]}\ue007')

        table0.ele(F'{henan_ele_dict.get("store_energy_day_discharge_power")}').input(
            F'{henan_oms_data[6]}\ue007')

        table0.ele(F'{henan_ele_dict.get("store_energy_day_charge_power_times")}').input(
            F'{int(henan_oms_data[7])}\ue007')
        table0.ele(F'{henan_ele_dict.get("store_energy_day_discharge_power_times")}').input(
            F'{int(henan_oms_data[8])}\ue007')
        time.sleep(3)
        self.upload_button_cn(table0)

    def upload_button_cn(self, table0):
        self.upload_button(table0)
        time.sleep(5)
        self.send_ding_cn(table0)

    def send_ding_cn(self, table0):
        time.sleep(3)
        save_wind_wfname = self.save_pic_cn(table0)
        from DingInfo.DingBotMix import DingApiTools
        # 天润
        DAT = DingApiTools(appkey_value=self.appkey, appsecret_value=self.appsecret, chatid_value=self.chatid)
        DAT.push_message(self.jf_token, self.message_cn)
        DAT.send_file(F'{save_wind_wfname}', 0)

        # 奈卢斯
        DATNLS = DingApiTools(appkey_value=self.nls_appkey, appsecret_value=self.nls_appsecret,
                              chatid_value=self.nls_chatid)
        DATNLS.push_message(self.nls_token, self.message_cn)
        DATNLS.send_file(F'{save_wind_wfname}', 0)

        self.update_mysql()

    def upload_button_dl(self, table0):
        self.upload_button(table0)
        self.send_ding_dl(table0)

    def send_ding_dl(self, table0):
        time.sleep(2)
        save_wind_wfname = self.save_pic(table0)
        from DingInfo.DingBotMix import DingApiTools
        # 天润
        DAT = DingApiTools(appkey_value=self.appkey, appsecret_value=self.appsecret, chatid_value=self.chatid)
        DAT.push_message(self.jf_token, self.message_dl)
        DAT.send_file(F'{save_wind_wfname}', 0)

        # 奈卢斯
        DATNLS = DingApiTools(appkey_value=self.nls_appkey, appsecret_value=self.nls_appsecret,
                              chatid_value=self.nls_chatid)

        DATNLS.push_message(self.nls_token, self.message_dl)
        DATNLS.send_file(F'{save_wind_wfname}', 0)

        self.update_mysql()

    def send_ding_qxjc_message(self, table0, message):
        time.sleep(2)
        save_wind_wfname = self.save_pic_qxjc(table0)
        from DingInfo.DingBotMix import DingApiTools
        # 天润
        # DAT = DingApiTools(appkey_value=self.appkey, appsecret_value=self.appsecret, chatid_value=self.chatid)
        # DAT.push_message(self.jf_token, self.message_dl)
        # DAT.send_file(F'{save_wind_wfname}', 0)

        # 奈卢斯
        DATNLS = DingApiTools(appkey_value=self.nls_appkey, appsecret_value=self.nls_appsecret,
                              chatid_value=self.nls_chatid)

        DATNLS.push_message(self.nls_token, message)
        DATNLS.send_file(F'{save_wind_wfname}', 0)

        self.update_mysql()

    def update_mysql(self):

        update_sql_success = F"update   data_oms  set  是否已完成 =1 ,填报开始时间 = '{self.start_run_time}',填报结束时间 = '{self.now_time_hms()}' where   日期='{self.previous_time_d()}' and 电场名称='{self.wfname}'"
        MysqlCurd(new_south).update(update_sql_success)

    def save_pic(self, table0):
        import os
        from pathlib import Path
        img_path = Path(f"..{os.sep}Image{os.sep}save_wind{os.sep}{self.previous_time_d()}{os.sep}")
        directory = img_path.parent

        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)

        # 对整页截图并保存
        save_wind_wfname = F"{img_path}{os.sep}{self.wfname}_程序.png"

        table0.get_screenshot(path=save_wind_wfname, full_page=True)

        return save_wind_wfname

    def save_pic_qxjc(self, table0):
        import os
        from pathlib import Path
        img_path = Path(f"..{os.sep}Image{os.sep}qxjc{os.sep}{self.previous_time_d()}{os.sep}")
        directory = img_path.parent

        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)

        # 对整页截图并保存
        save_wind_wfname = F"{img_path}{os.sep}{self.wfname}缺陷检测.png"

        table0.get_screenshot(path=save_wind_wfname, full_page=True)

        return save_wind_wfname

    def save_pic_cn(self, table0):
        import os
        from pathlib import Path
        img_path = Path(f"..{os.sep}Image{os.sep}save_wind{os.sep}{self.previous_time_d()}{os.sep}")
        directory = img_path.parent

        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)

        # 对整页截图并保存
        save_wind_wfname = F"{img_path}{os.sep}{self.wfname}_程序_储能.png"

        table0.get_screenshot(path=save_wind_wfname, full_page=True)

        return save_wind_wfname

    def upload_button(self, table0):
        try:
            table0.ele(F'{henan_ele_dict.get("upload_battery_button")}').click()
            hadle_alert_true = table0.handle_alert(accept=True)
            logger.warning(F'这里是点击确定后的返回值！__{hadle_alert_true}')
        except Exception as e:
            table0.ele(F'{henan_ele_dict.get("upload_battery_button")}').click()
            hadle_alert_true = table0.handle_alert(accept=True)
            logger.warning(F'这里是点击确定后的返回值！__{hadle_alert_true}')
            pass

    def report_sxz(self):
        self.page.ele(F'{henan_ele_dict.get("sxz_button")}').click()
        table0 = self.page.get_tab(0)


def run_henan_oms():
    # EdgeChromeCurd().open_baidu()
    HenanOms().run_oms()
    # HenanOms().get_henan_data()


def run_henan_qxjc():
    # EdgeChromeCurd().open_baidu()
    HenanOms().run_oms_qxjc()
    # HenanOms().get_henan_data()


def run_henan_sxz():
    # EdgeChromeCurd().open_baidu()
    HenanOms().run_sxz()
    # HenanOms().get_henan_data()


if __name__ == '__main__':
    print(F"正常运行!")

    run_henan_qxjc()

    # schedule.every().day.at("00:12").do(run_henan_qxjc)
    # schedule.every().day.at("00:40").do(run_henan_oms)
    # # run_henan_oms()
    # # run_henan_sxz()
    # while True:
    #     schedule.run_pending()
    #
    #     time.sleep(1)
