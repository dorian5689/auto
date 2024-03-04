#! /usr/bin/env python
# -*-coding:utf-8-*-

import ctypes
import platform
import re
import os
import subprocess
import sys
import winreg
from LogInfo.LogTools import Logger


class SetMac(object):
    """
    修改 本地连接 mac地址
    """

    def __init__(self):
        # regex to MAC address like 00-00-00-00-00-00 or 00:00:00:00:00:00 or 000000000000
        self.MAC_ADDRESS_RE = re.compile(r"""
            ([0-9A-F]{1,2})[:-]?
            ([0-9A-F]{1,2})[:-]?
            ([0-9A-F]{1,2})[:-]?
            ([0-9A-F]{1,2})[:-]?
            ([0-9A-F]{1,2})[:-]?
            ([0-9A-F]{1,2})
            """, re.I | re.VERBOSE)  # re.I: case-insensitive matching. re.VERBOSE: just look nicer.

        self.WIN_REGISTRY_PATH = "SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}"
        self.log = Logger()

    def is_admin(self):
        """
        is user an admin?
        :return:
        """
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            self.log.error(
                F'请使用管理员权限运行代码！')
            sys.exit()
        else:
            self.log.info('已使用管理员权限运行代码！')

    def get_macinfos(self):
        """
        查看所有mac信息
        :return:
        """
        print('=' * 50)
        mac_info = subprocess.check_output('GETMAC /v /FO list', stderr=subprocess.STDOUT)
        mac_info = mac_info.decode('gbk')
        # self.log.info(F' MAC 地址:{mac_info}')

    def get_target_device(self):
        """
        返回 本地连接 网络适配器
        :return:
        """
        mac_info = subprocess.check_output('GETMAC /v /FO list', stderr=subprocess.STDOUT)
        mac_info = mac_info.decode('gbk')
        # mac_info = mac_info.decode('gbk').replace("\r","").replace("\n","")
        search = re.search(r'(以太网)\s+网络适配器: (.+)\s+物理地址:', mac_info)
        # search = re.search(r'(以太网)网络适配器: (.+)+物理地址:', mac_info)
        target_name, target_device = (search.group(1), search.group(2).strip()) if search else ('', '')
        if not all([target_name, target_device]):
            self.log.error(F'没有找到网卡信息！')
            sys.exit()
            # try:
            #     pattern = re.compile(r'连接名: (.*?)\r\n网络适配器: (.*?)\n')  # 正则表达式模式
            #     match = pattern.search(mac_info)  # 执行正则表达式匹配
            #
            #     target_name, target_device = (match.group(1), match.group(2).strip()) if match else (
            #     '', '')  # 提取连接名和网络适配器名称
            #     print("连接名称:", target_name)
            #     print("网络适配器名称:", target_device)
            #     if  not target_device:
            #         self.log.error(F'没有找到网卡信息！')
            #         sys.exit()
            # except:
            #     self.log.error(F'没有找到网卡信息！')
            #     sys.exit()

        # self.log.info(F'=' * 50)
        # self.log.info(F'网卡名称"{target_name}')
        # self.log.info(F'网卡信息:{target_device}')

        return target_device

    def set_mac_address(self, target_device, new_mac):
        """
        设置新mac地址
        :param target_device: 本地连接 网络适配器
        :param new_mac: 新mac地址
        :return:
        """
        if not self.MAC_ADDRESS_RE.match(new_mac):
            self.log.error(F'请输入正确的MAC地址')

            return

        # Locate adapter's registry and update network address (mac)
        reg_hdl = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg_hdl, self.WIN_REGISTRY_PATH)
        info = winreg.QueryInfoKey(key)

        # Find adapter key based on sub keys
        adapter_key = None
        adapter_path = None
        target_index = -1

        for index in range(info[0]):
            subkey = winreg.EnumKey(key, index)
            path = self.WIN_REGISTRY_PATH + "\\" + subkey

            if subkey == 'Properties':
                break

            # Check for adapter match for appropriate interface
            new_key = winreg.OpenKey(reg_hdl, path)
            try:
                adapterDesc = winreg.QueryValueEx(new_key, "DriverDesc")
                if adapterDesc[0] == target_device:
                    adapter_path = path
                    target_index = index
                    break
                else:
                    winreg.CloseKey(new_key)
            except (WindowsError) as err:
                if err.errno == 2:  # register value not found, ok to ignore
                    pass
                else:
                    raise err

        if adapter_path is None:
            self.log.error(F'设备信息未找到!')

            winreg.CloseKey(key)
            winreg.CloseKey(reg_hdl)
            return

        # Registry path found update mac addr
        adapter_key = winreg.OpenKey(reg_hdl, adapter_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(adapter_key, "NetworkAddress", 0, winreg.REG_SZ, new_mac)
        winreg.CloseKey(adapter_key)
        winreg.CloseKey(key)
        winreg.CloseKey(reg_hdl)

        self.restart_adapter(target_index, target_device)

    def restart_adapter(self, target_index, target_device):
        """
        Disables and then re-enables device interface
        """
        # print(platform.release())
        if platform.release() == 'XP':
            # description, adapter_name, address, current_address = find_interface(device)
            cmd = "devcon hwids =net"
            try:
                result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            except FileNotFoundError:
                raise
            query = '(' + target_device + '\r\n\s*.*:\r\n\s*)PCI\\\\(([A-Z]|[0-9]|_|&)*)'
            query = query.encode('ascii')
            match = re.search(query, result)
            cmd = 'devcon restart "PCI\\' + str(match.group(2).decode('ascii')) + '"'
            subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        else:
            # cmd = "wmic path win32_networkadapter where index=" + str(target_index) + " call disable"
            # subprocess.check_output(cmd)
            # cmd = "wmic path win32_networkadapter where index=" + str(target_index) + " call enable"
            # subprocess.check_output(cmd)
            cmd = 'netsh interface set interface "以太网" admin=disable'
            subprocess.check_output(cmd)
            cmd = 'netsh interface set interface "以太网" admin=enable'
            subprocess.check_output(cmd)

    def run(self, new_mac):
        self.is_admin()
        self.get_macinfos()
        target_device = self.get_target_device()
        self.set_mac_address(target_device, new_mac)
        self.get_macinfos()
        self.log.info(F'网卡信息更换完成！')

    def test(self):
        self.is_admin()
        self.get_macinfos()
        target_device = self.get_target_device()
        # print(target_device)
#
# if __name__ == '__main__':
#     set_mac = SetMac() # 00FFAABBCCDD
#     # new_mac = '6C4B90B008C0'
#     new_mac = '6C4B90B00010'  #6C-4B-90-B0-08-C0
#     set_mac.run(new_mac)
#     # set_mac = SetMac()
#     # set_mac.test()
