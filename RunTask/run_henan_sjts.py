#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time ： 2024/3/18 17:57
@Auth ： Xq
@File ：run_henan_sjts.py
@IDE ：PyCharm
"""

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from BrowserOperate.EdgeChromeTools import EdgeChromeCurd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
import psycopg2
import datetime
import pandas as pd
from loguru import logger
import schedule
from DingInfo.DingtalkBot import DingapiTools
# from Config.ConfigHenanOmsMysql import henan_oms_config_sjts_select_wfname
from Config.ConfigHenanOmsPgsql import henan_oms_config_pgsql_sjts_select
from DataBaseInfo.MysqlTools import MysqlCurd
from Config.ConfigHenanOmsMysql import new_south
from Config.ConfigHenanOmsFanRuanOmsBeiFen import henan_fanruan_oms_beifen_url

logger.info('oms河南区域每日发送')

save_data = datetime.datetime.now().strftime("%Y-%m-%d")


class HeNanReportData():

    def __init__(self):
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
        self.wfname =''

    def send_ding_henan_sjts(self, table0, message):
        time.sleep(3)
        save_wind_wfname = self.save_pic_sjts(table0)
        logger.warning(F'数据推送地址:{save_wind_wfname}')
        from DingInfo.DingBotMix import DingApiTools
        # # 天润
        DAT = DingApiTools(appkey_value=self.appkey, appsecret_value=self.appsecret, chatid_value=self.chatid)
        DAT.push_message(self.jf_token, message)
        DAT.send_file(F'{save_wind_wfname}', 0)

        # 奈卢斯
        DATNLS = DingApiTools(appkey_value=self.nls_appkey, appsecret_value=self.nls_appsecret,
                              chatid_value=self.nls_chatid)
        DATNLS.push_message(self.nls_token, message)
        DATNLS.send_file(F'{save_wind_wfname}', 0)

    def save_pic_sjts(self, table0):
        import os
        # from pathlib import Path
        # img_path = Path(f"..{os.sep}Image{os.sep}save_wind{os.sep}{self.previous_time_d()}{os.sep}")
        # directory = img_path.parent

        current_path = os.path.abspath(__file__)  # 获取当前脚本的绝对路径
        parent_path = os.path.dirname(current_path)  # 获取当前脚本所在目录的父目录
        # parent_path = os.path.dirname(parent_path)  # 获取当前脚本所在目录的父目录
        directory = os.path.join(parent_path, 'Image', 'sjts')
        save_wind_wfname = os.path.join(parent_path, 'Image', 'sjts', F'{self.wfname}_数据推送.png')

        if not os.path.exists(directory):
            os.makedirs(directory)

        # 对整页截图并保存
        # save_wind_wfname = F"{img_path}{os.sep}{self.wfname}_程序_储能.png"

        table0.get_screenshot(path=save_wind_wfname, full_page=True)

        return save_wind_wfname

    def report_data(self):
        hh3 = datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')
        hh4 = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')

        conn = psycopg2.connect(database="v5", user="tradmin", password="trxn@2019", host="16.3.1.22", port="8101")
        logger.warning(F"连接V5数据库成功")
        cursor = conn.cursor()
        cursor.execute(henan_oms_config_pgsql_sjts_select, (hh4, hh3))
        daily_data = cursor.fetchall()
        logger.warning(F'v5获取数据总数为:{len(daily_data)}')
        cols = cursor.description
        cursor.close()
        conn.close()
        col = []
        for i in cols:
            col.append(i[0])

        df = pd.DataFrame(daily_data, columns=col)[['省份', '电场名称', '日期', '发电量', '上网电量']]

        new_data = pd.DataFrame([['河南省', '飞翔三期储能', 0, 0, 0]],
                                columns=['省份', '电场名称', '日期', '发电量', '上网电量'])

        # 将飞翔风电场的上网电量赋给飞翔风电场2
        try:
            new_data["日期"] = df.loc[df['电场名称'] == '飞翔风电场']['日期'].values[0]
            new_data["发电量"] = df.loc[df['电场名称'] == '飞翔风电场']['发电量'].values[0]
            new_data["上网电量"] = df.loc[df['电场名称'] == '飞翔风电场']['上网电量'].values[0]
        except:
            pass
        df3 = pd.concat([df, new_data], ignore_index=True)
        logger.warning(F'数据转化完成!')

        try:
            from DataBaseInfo.qdl import qdl_df
            newdf = qdl_df()
            try:
                new_data_qdl = pd.DataFrame(
                    [['飞翔三期储能', newdf[newdf['电场名称'] == '飞翔风电场']['弃电量'].values[0]]],
                    columns=['电场名称', '弃电量'])
                newdf = pd.concat([newdf, new_data_qdl], ignore_index=True)

            except:
                pass

            merged_df = pd.merge(df3, newdf, on='电场名称', how='left')
            merged_df["弃电量"] = merged_df["弃电量"].fillna(0)
            # merged_df["弃电量"] = merged_df["弃电量"].astype(int)
        except Exception as e:
            merged_df = df

        merged_df.to_excel('河南oms81.xlsx')
        logger.warning(F'xlsx已经保存到本机 ')

        try:

            NEWMC = MysqlCurd(new_south)
            for index, row in merged_df.iterrows():
                sf = row["省份"]
                dcmc = row["电场名称"]
                self.wfname = dcmc
                rq = row["日期"]
                fdl = row["发电量"]
                swdl = row["上网电量"]
                try:
                    qdl = row["弃电量"]
                except:
                    qdl = 0
                insert_sql = F"INSERT INTO data_oms (省份,电场名称,日期,发电量,上网电量,弃电量) VALUES ('{sf}','{dcmc}','{rq}','{fdl}','{swdl}','{qdl}')"
                update_sql = F" UPDATE data_oms SET 发电量= '{fdl}', 上网电量 = '{swdl}',  弃电量= '{qdl}' WHERE 电场名称= '{dcmc}' and 日期 ='{rq}' "
                check_sql = F"select count(*) from data_oms where 电场名称 ='{dcmc}' and  日期 = '{rq}' "
                print(insert_sql)
                print(update_sql)
                # continue
                result_oms_data1 = NEWMC.query(check_sql)
                result_oms_data = result_oms_data1.values.tolist()[0][0]
                if not result_oms_data:

                    NEWMC.update(insert_sql)
                    print(F'新sql更新----{insert_sql}')

                else:
                    print(F'新sql插入')
                    NEWMC.update(update_sql)
                try:
                    MC = MysqlCurd()
                    if MC.update(insert_sql):
                        print(F"插入成功--{insert_sql}")
                        logger.warning(F'{dcmc}数据添加成功')

                    else:
                        MC.update(update_sql)
                        print("更新成功" - ---{update_sql})
                        logger.warning(F'{dcmc}数据已经更新')
                except Exception as e:
                    print(F'{e}--老库失败！')
            # merged_df.to_sql('data_oms', engine, if_exists='append', index=False)
            # merged_df.to_sql('data_oms', engine, if_exists='replace', index=False)
            # 推动到钉钉
            # token = "c8eb8d7b8fe2a3c07843233bf225082126db09ab59506bd5631abef4304da29e"
            message = {
                "title": "推送-数据入库",
                "text": F"OMS数据已经入库,<br>入库时间为<br>{save_data}"}
            # DT = DingapiTools()
            # DT.SendMessageDing(token, markdown_true)
            # DT.SendMessageDing(token, markdown_true)
            page = EdgeChromeCurd().open_fanruan(henan_fanruan_oms_beifen_url)
            message = {
                    "msgtype": "markdown",
                    "markdown": {
                "title": "推送-数据入库",
                "text": F"OMS数据已经入库,<br>入库时间为<br>{save_data}"
                    },
                }

            self.send_ding_henan_sjts(page, message)

        except Exception as e:
            print(e)


def runtask():
    HeNanReportData().report_data()


if __name__ == '__main__':
    # print(F'数据推送程序运行中,请勿关闭')
    runtask()
    # print(F'数据推送程序运行中,请勿关闭')
    # schedule.every().day.at("00:01").do(runtask)
    # schedule.every().day.at("00:02").do(runtask)
    # print(F'有定时器！')
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
