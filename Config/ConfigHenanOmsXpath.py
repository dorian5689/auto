#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time ： 2024/3/5 2:39
@Auth ： Xq
@File ：ConfigHenanOmsXpath.py
@IDE ：PyCharm
"""

henan_ele_dict = {
    # 重新建在
    'again_post':'//*[@id="reload-button"]',
    # 点击更多
    'details-button': 'x://*[@id="details-button"]',
    # 点击详情页
    'proceed-link': 'x://*[@id="proceed-link"]',
    # 输入账号
    'input_text': 'x://input[@type="text"]',
    # 输入密码
    'input_password': 'x://input[@type="password"]',
    # 点击验证码
    'capture_img': 'x://*[@id="app"]/div/div/form/div[5]/div/div/div[2]/img',
    #  输入验证码
    'capture_img_frame': 'x://*[@id="app"]/div/div/form/div[5]/div/div/div[1]/div/input',
    # 点击登录按钮
    'login_button': 'x://*[@id="app"]/div/div/form/div[6]/div/button',
    # 点击oms按钮
    'oms_button': 'x://*[@id="app"]/section/section/div/div/div/div/div[4]/div[2]/div/div/div/div/div/div[1]',


    # 收报负荷
    'report_load': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[2]/li/div/span',
    # 点击收报负荷-机组日实际发电量
    'report_load_button_dl': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[2]/li/ul/div[1]/a/li/span',
    # 上报日期
    'upload_date': 'x://*[@id="1$cell$2"]/div',

    # 发电量
    'send_battery': 'x://*[@id="formtable"]/tbody/tr[2]/td[2]/span[1]/span/input',
    # 上网电量
    'upload_battery': 'x://*[@id="formtable"]/tbody/tr[3]/td[2]/span[1]/span/input',
    # 弃电量
    'abandoned_battery': 'x://*[@id="formtable"]/tbody/tr[4]/td[2]/span[1]/span/input',
    # 上报按钮
    'upload_battery_button': 'x://*[@id="mbtns"]/div',

    # 点击收报负荷-储能
    'report_load_button_cn': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[2]/li/ul/div[position()=last()]/a/li/span',

    # 储能日最大充电电力
    'store_energy_max_charge_power_day': 'x://*[@id="formtable"]/tbody/tr[4]/td[2]/span[1]/span/input',
    # 储能日最大放电电力
    'store_energy_max_discharge_power_day': 'x://*[@id="formtable"]/tbody/tr[5]/td[2]/span[1]/span/input',
    # 储能日充电量
    'store_energy_day_charge_power': 'x://*[@id="formtable"]/tbody/tr[6]/td[2]/span[1]/span/input',
    # 储能日放电量
    'store_energy_day_discharge_power': 'x://*[@id="formtable"]/tbody/tr[7]/td[2]/span[1]/span/input',
    # 储能日充电次数
    'store_energy_day_charge_power_times': 'x://*[@id="formtable"]/tbody/tr[8]/td[2]/span[1]/span/input',
    # 储能日放电次数
    'store_energy_day_discharge_power_times': 'x://*[@id="formtable"]/tbody/tr[9]/td[2]/span[1]/span/input',

    # 飞翔储能三期
    # 储能日最大充电电力
    'store_energy_max_charge_power_day3': 'x://*[@id="formtable"]/tbody/tr[12]/td[2]/span[1]/span/input',
    # 储能日最大放电电力
    'store_energy_max_discharge_power_day3': 'x://*[@id="formtable"]/tbody/tr[13]/td[2]/span[1]/span/input',
    # 储能日充电量
    'store_energy_day_charge_power3': 'x://*[@id="formtable"]/tbody/tr[14]/td[2]/span[1]/span[1]/input',
    # 储能日放电量
    'store_energy_day_discharge_power3': 'x://*[@id="formtable"]/tbody/tr[15]/td[2]/span[1]/span/input',
    # 储能日充电次数
    'store_energy_day_charge_power_times3': 'x://*[@id="formtable"]/tbody/tr[16]/td[2]/span[1]/span/input',
    # 储能日放电次数
    'store_energy_day_discharge_power_times3': 'x://*[@id="formtable"]/tbody/tr[17]/td[2]/span[1]/span/input',
    # 上报日期
    'report_date': 'x://*[@id="1$cell$2"]/div',
    # 上报状态
    'report_status': 'x://*[@id="1$cell$3"]/div',

    #

    # 点击双细则按钮
    'sxz_button': 'x://*[@id="app"]/section/section/div/div/div/div/div[4]/div[2]/div/div/div/div/div/div[4]/p',

    # 调度考核管理 3
    'ddglkh_button3': 'x://*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[4]/li/div/span',

    # 风光功率预测考核日考核数据汇总 3-8
    'ddglkh_button3_8': 'x://*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[4]/li/ul/div[8]/a/li/span',
    # 点击风电场
    'ddglkh_button3_8_L111': 'x://*[@id="app"]/div/div[2]/section/div/div/form/div[1]/div/div[1]/div[2]/div[1]/div[2]/div/div[1]/span[2]',
    # 点击开始时间
    'ddglkh_button3_8_L111_st': 'x://*[@id="app"]/div/div[2]/section/div/div/form/div[2]/div[1]/div/div/input',
    # 点击结束时间
    'ddglkh_button3_8_L111_et': 'x://*[@id="app"]/div/div[2]/section/div/div/form/div[2]/div[2]/div/div/input',
    # 点击搜索按钮
    'ddglkh_button3_8_L111_search': 'x://*[@id="app"]/div/div[2]/section/div/div/form/div[2]/div[2]/div/button/span',
    # 点击日期
    'ddglkh_button3_8_L111_data': 'x://*[@id="app"]/div/div[2]/section/div/div/form/div[2]/div[3]/div[2]/div/div[3]/table/tbody/tr',

    # 有功功率变化日考核结果 3-11
    'ddglkh_button3_11': 'x://*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[4]/li/ul/div[11]/a/li/span',
    # 点击风电场
    'ddglkh_button3_11_L111': 'x://*[@id="app"]/div/div[2]/section/div/div/form/div[1]/div/div[1]/div[2]/div[1]/div[2]/div/div[1]/span[2]',
    # 点击开始时间
    'ddglkh_button3_11_L111_st': 'x://*[@id="app"]/div/div[2]/section/div/div/form/div[2]/div[1]/div[1]/div/div/div/input',
    # 点击结束时间
    'ddglkh_button3_11_L111_et': 'x://*[@id="app"]/div/div[2]/section/div/div/form/div[2]/div[1]/div[2]/div/div/div/input',
    # 点击日期
    'ddglkh_button3_11_L111_data': 'x://*[@id="app"]/div/div[2]/section/div/div/form/div[2]/div[2]/div/div[2]/div/div[3]/table/tbody/tr',

    # 技术考核管理 4
    'jsglkh_button4': 'x://*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/div/span',
    # 动态无功装置补偿可用率 4-1
    'jsglkh_button4_1': 'x://*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/ul/div[1]/a/li/span',
    # 点击风电场
    'jsglkh_button4_1_L111': 'x://*[@id="pane-first"]/div/div/form/div[1]/div/div[1]/div[2]/div[1]/div[2]/div/div[1]/span[2]',
    # 点击开始时间
    'jsglkh_button4_1_L111_st': 'x://*[@id="pane-first"]/div/div/form/div[2]/div[1]/div/div/input',
    # 点击结束时间
    'jsglkh_button4_1_L111_et': 'x://*[@id="pane-first"]/div/div/form/div[2]/div[2]/div/div/input',
    # 点击搜索按钮
    'jsglkh_button4_1_L111_search': 'x://*[@id="pane-first"]/div/div/form/div[2]/div[2]/div/button/span',
    # 点击日期
    'jsglkh_button4_1_L111_data': 'x://*[@id="pane-first"]/div/div/form/div[2]/div[3]/div[2]/div/div[3]/table/tbody/tr',

    # 有功调节能力考核 4-3
    'jsglkh_button4_3': 'x://*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/ul/div[3]/li/div/span',
    # acg 投运率
    'jsglkh_button4_3_1': 'x://*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/ul/div[3]/li/ul/div[1]/a/li/span',
    # 点击风场
    'jsglkh_button4_3_1_L1': 'x://*[@id="app"]/div/div[2]/section/div/div/div[1]/div/div[2]/div/div[1]/div[1]/label/span/span',
    # 日投运率
    'jsglkh_button4_3_1_R2': 'x://*[@id="tab-1"]/span/i',
    # 点击开始时间

    'jsglkh_button4_3_1_R2_st': 'x://*[@id="pane-1"]/div[1]/div[1]/input',
    # 点击结束时间
    'jsglkh_button4_3_1_R2_et': 'x://*[@id="pane-1"]/div[1]/div[2]/input',
    # 点击搜索按钮
    'jsglkh_button4_3_1_R2_search': 'x://*[@id="pane-1"]/div[1]/button/span',
    # 点击日期
    'jsglkh_button4_3_1_R2_data': 'x://*[@id="pane-1"]/div[2]/div[3]/table/tbody/tr',

    # 并网电压曲线考核结果 4-4
    'jsglkh_button4_4': 'x://*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/ul/div[4]/a/li/span',
    # 日合格率结果
    'jsglkh_button4_4_T3': 'x://*[@id="tab-2"]/span/i',
    # 点击开始时间
    'jsglkh_button4_4_T3_st': 'x://*[@id="pane-2"]/div[1]/div[1]/input',
    # 点击结束时间
    'jsglkh_button4_4_T3_et': 'x://*[@id="pane-2"]/div[1]/div[2]/input',
    # 点击搜索按钮
    'jsglkh_button4_4_T3_search': 'x://*[@id="pane-2"]/div[1]/button',
    # 点击日期
    'jsglkh_button4_4_T3_data': 'x://*[@id="pane-2"]/div[2]/div[3]/table/tbody/tr',

    # 点击退出用户
    'exit_username_button': 'x://*[@id="dropdown-menu-3427"]/li[1]/span',
    # 确认退出用户
    'exit_username_button_exit': 'x://*[@id="dropdown-menu-2414"]',

    'shoubaofuhe_button': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[2]/li/div',
    'shoubaofuhe_button_1': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[2]/li/ul/div[1]/a/li/span',

    # 省地通知

    'sditz':'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[8]/li/div/i',
    # 省调通知
    'sdtz':'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[8]/li/ul/div[1]/a/li/span',


    # Oms一次性检修计划
    'oms_ycxjxjh':'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[3]/li/div/span',
    # 一次性检修计划_月计划
    'oms_ycxjxjh_yjh':'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[3]/li/ul/div[2]/li/div/span',
    # 一次性检修计划_月计划_发电检修
    'oms_ycxjxjh_yjh_fdjx':'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[3]/li/ul/div[2]/li/ul/div[1]/li/div/span',
    # 一次性检修计划_月计划_发电检修_发电月计划视图
    'oms_ycxjxjh_yjh_fdjx_fdyjhst':'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[3]/li/ul/div[2]/li/ul/div[1]/li/ul/div/a/li/span',
    'oms_ycxjxjh_zdhjxjh_yjh_fdjx_fdyjhst_nian':'x://*[@id="app"]/section/section/main/section/div/div/div[1]/div/div[1]/form[1]/div/div[1]/div/div/div[2]/div/div/input',
    'oms_ycxjxjh_zdhjxjh_yjh_fdjx_fdyjhst_yue':'x://*[@id="app"]/section/section/main/section/div/div/div[1]/div/div[1]/form[1]/div/div[2]/div/div/div[2]/div/div/input',
    'oms_ycxjxjh_zdhjxjh_yjh_fdjx_fdyjhst_cx':'x://*[@id="app"]/section/section/main/section/div/div/div[1]/div/div[1]/form[2]/div/div/button/span',
    # 一次性检修计划_周计划
    'oms_ycxjxjh_zjh': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[3]/li/ul/div[3]/li/div/span',
    # 一次性检修计划_周计划_发电检修
    'oms_ycxjxjh_zdhjxjh_zjh_fdjx': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[3]/li/ul/div[3]/li/ul/div[2]/li/div/span',
    # 一次性检修计划_周计划_发电检修_发电周计划视图
    'oms_ycxjxjh_zdhjxjh_zjh_fdjx_fdzjhst': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[3]/li/ul/div[3]/li/ul/div[2]/li/ul/div/a/li/span',
    'oms_ycxjxjh_zdhjxjh_zjh_fdjx_fdzjhst_cx': 'x://*[@id="app"]/section/section/main/section/div/div/div[1]/div/div[1]/form[2]/div/div/button/span',
    # 一次性检修计划_日计划
    'oms_ycxjxjh_rjh': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[3]/li/ul/div[4]/li/div/span',
    # 一次性检修计划_日计划_发电检修
    'oms_ycxjxjh_rjh_fdjx': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[3]/li/ul/div[4]/li/ul/div[2]/li/div/span',
    # 一次性检修计划_日计划_发电检修_发电日计划视图
    'oms_ycxjxjh_rjh_fdjx_fdrjhst': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[3]/li/ul/div[4]/li/ul/div[2]/li/ul/div[3]/a/li/span',
    'oms_ycxjxjh_rjh_fdjx_fdrjhst_cx': 'x://*[@id="app"]/section/section/main/section/div/div/div[1]/div/div[1]/form[2]/div/div/button/span',

    # 二次检修计划
    'oms_ecjxjh': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[4]/li/div/span',
    # 二次检修计划_自动化检修计划
    'oms_ecjxjh_zdhjxjh': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[4]/li/ul/div[1]/li/div/span',
    # 二次检修计划_自动化检修计划_自动化周计划
    'oms_ecjxjh_zdjxjh_zdhzjh': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[4]/li/ul/div[1]/li/ul/div[1]/a/li/span',
    # 二次性检修计划__自动检修计划__自动化紧急检修
    'oms_ecjxjh_zdjxjh_zdhjjjx': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[4]/li/ul/div[1]/li/ul/div[2]/a/li/span',
    # 二次性检修计划__自动检修计划__自动化日计划
    'oms_ecjxjh_zdjxjh_zdhrjh': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[4]/li/ul/div[1]/li/ul/div[3]/a/li/span',
    # 二次检修计划__自动化检修计划__自动化日计划流程
    'oms_ecjxjh_zdjxjh_zdhrjhlc': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[4]/li/ul/div[1]/li/ul/div[4]/a/li/span',
    # 二次检修计划_网安检修计划
    'oms_ecjxjh_wajxjh': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[4]/li/ul/div[2]/li/div/span',
    # 二次检修计划_网安检修计划_网安周计划管理
    'oms_ecjxjh_wajxjh_wazjhgl': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[4]/li/ul/div[2]/li/ul/div[1]/a/li/span',
    # 二次检修计划_网安检修计划_网安日计划流程管理
    'oms_ecjxjh_wajxjh_warlhlcgl': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[4]/li/ul/div[2]/li/ul/div[2]/a/li/span',

    # 缺陷管理
    'oms_qxgl': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[11]/li/div/span',
    # 缺陷管理_场站设备缺陷(老)
    'oms_qxgl_czsbqxl': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[11]/li/ul/div[1]/li/div/span',
    #缺陷管理_场站设备缺陷(老)_缺陷流程管理
    'oms_qxgl_czsbqxl_qxlcgl': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[11]/li/ul/div[1]/li/ul/div/a/li/span',


}