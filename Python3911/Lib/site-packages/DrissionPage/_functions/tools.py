# -*- coding:utf-8 -*-
"""
@Author   : g1879
@Contact  : g1879@qq.com
@Copyright: (c) 2024 by g1879, Inc. All Rights Reserved.
@License  : BSD 3-Clause.
"""
from pathlib import Path
from platform import system
from shutil import rmtree
from time import perf_counter, sleep

from psutil import process_iter, AccessDenied, NoSuchProcess, ZombieProcess

from .._configs.options_manage import OptionsManager
from ..errors import (ContextLostError, ElementLostError, CDPError, PageDisconnectedError, NoRectError,
                      AlertExistsError, WrongURLError, StorageError, CookieFormatError, JavaScriptError)


def port_is_using(ip, port):
    """检查端口是否被占用
    :param ip: 浏览器地址
    :param port: 浏览器端口
    :return: bool
    """
    from socket import socket, AF_INET, SOCK_STREAM
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(.1)
    result = s.connect_ex((ip, int(port)))
    s.close()
    return result == 0


def clean_folder(folder_path, ignore=None):
    """清空一个文件夹，除了ignore里的文件和文件夹
    :param folder_path: 要清空的文件夹路径
    :param ignore: 忽略列表
    :return: None
    """
    ignore = [] if not ignore else ignore
    p = Path(folder_path)

    for f in p.iterdir():
        if f.name not in ignore:
            if f.is_file():
                f.unlink()
            elif f.is_dir():
                rmtree(f, True)


def show_or_hide_browser(page, hide=True):
    """执行显示或隐藏浏览器窗口
    :param page: ChromePage对象
    :param hide: 是否隐藏
    :return: None
    """
    if not page.address.startswith(('127.0.0.1', 'localhost')):
        return

    if system().lower() != 'windows':
        raise OSError('该方法只能在Windows系统使用。')

    try:
        from win32gui import ShowWindow
        from win32con import SW_HIDE, SW_SHOW
    except ImportError:
        raise ImportError('请先安装：pip install pypiwin32')

    pid = page.process_id
    if not pid:
        return None
    hds = get_chrome_hwnds_from_pid(pid, page.title)
    sw = SW_HIDE if hide else SW_SHOW
    for hd in hds:
        ShowWindow(hd, sw)


def get_browser_progress_id(progress, address):
    """获取浏览器进程id
    :param progress: 已知的进程对象，没有时传入None
    :param address: 浏览器管理地址，含端口
    :return: 进程id或None
    """
    if progress:
        return progress.pid

    from os import popen
    port = address.split(':')[-1]
    txt = ''
    progresses = popen(f'netstat -nao | findstr :{port}').read().split('\n')
    for progress in progresses:
        if 'LISTENING' in progress:
            txt = progress
            break
    if not txt:
        return None

    return txt.split(' ')[-1]


def get_chrome_hwnds_from_pid(pid, title):
    """通过PID查询句柄ID
    :param pid: 进程id
    :param title: 窗口标题
    :return: 进程句柄组成的列表
    """
    try:
        from win32gui import IsWindow, GetWindowText, EnumWindows
        from win32process import GetWindowThreadProcessId
    except ImportError:
        raise ImportError('请先安装win32gui，pip install pypiwin32')

    def callback(hwnd, hds):
        if IsWindow(hwnd) and title in GetWindowText(hwnd):
            _, found_pid = GetWindowThreadProcessId(hwnd)
            if str(found_pid) == str(pid):
                hds.append(hwnd)
            return True

    hwnds = []
    EnumWindows(callback, hwnds)
    return hwnds


def wait_until(page, condition, timeout=10, poll=0.1, raise_err=True):
    """等待返回值不为False或空，直到超时
    :param page: DrissionPage对象
    :param condition: 等待条件，返回值不为False则停止等待
    :param timeout: 超时时间（秒）
    :param poll: 轮询间隔
    :param raise_err: 是否抛出异常
    :return: DP Element or bool
    """
    end_time = perf_counter() + timeout
    if isinstance(condition, str) or isinstance(condition, tuple):
        if not callable(getattr(page, 's_ele', None)):
            raise AttributeError('page对象缺少s_ele方法')
        condition_method = lambda page: page.s_ele(condition)
    elif callable(condition):
        condition_method = condition
    else:
        raise ValueError('condition必须是函数或者字符串或者元组')
    while perf_counter() < end_time:
        try:
            value = condition_method(page)
            if value:
                return value
        except Exception:
            pass

        sleep(poll)
        if perf_counter() > end_time:
            break

    if raise_err:
        raise TimeoutError(f'等待超时（等待{timeout}秒）。')
    else:
        return False


def stop_process_on_port(port):
    """强制关闭某个端口内的进程
    :param port: 端口号
    :return: None
    """
    for proc in process_iter(['pid', 'connections']):
        try:
            connections = proc.connections()
        except (AccessDenied, NoSuchProcess):
            continue
        for conn in connections:
            if conn.laddr.port == int(port):
                try:
                    proc.terminate()
                except (NoSuchProcess, AccessDenied, ZombieProcess):
                    pass
                except Exception as e:
                    print(f"{proc.pid} {port}: {e}")


def configs_to_here(save_name=None):
    """把默认ini文件复制到当前目录
    :param save_name: 指定文件名，为None则命名为'dp_configs.ini'
    :return: None
    """
    om = OptionsManager('default')
    save_name = f'{save_name}.ini' if save_name is not None else 'dp_configs.ini'
    om.save(save_name)


def raise_error(result, ignore=None):
    """抛出error对应报错
    :param result: 包含error的dict
    :param ignore: 要忽略的错误
    :return: None
    """
    error = result['error']
    if error in ('Cannot find context with specified id', 'Inspected target navigated or closed'):
        r = ContextLostError()
    elif error in ('Could not find node with given id', 'Could not find object with given id',
                   'No node with given id found', 'Node with given id does not belong to the document',
                   'No node found for given backend id'):
        r = ElementLostError()
    elif error in ('connection disconnected', 'No target with given id found'):
        r = PageDisconnectedError()
    elif error == 'alert exists.':
        r = AlertExistsError()
    elif error in ('Node does not have a layout object', 'Could not compute box model.'):
        r = NoRectError()
    elif error == 'Cannot navigate to invalid URL':
        r = WrongURLError(f'无效的url：{result["args"]["url"]}。也许要加上"http://"？')
    elif error == 'Frame corresponds to an opaque origin and its storage key cannot be serialized':
        r = StorageError()
    elif error == 'Sanitizing cookie failed':
        r = CookieFormatError(f'cookie格式不正确：{result["args"]}')
    elif error == 'Given expression does not evaluate to a function':
        r = JavaScriptError(f'传入的js无法解析成函数：\n{result["args"]["functionDeclaration"]}')
    elif result['type'] in ('call_method_error', 'timeout'):
        from DrissionPage import __version__
        from time import process_time
        txt = f'\n错误：{result["error"]}\nmethod：{result["method"]}\nargs：{result["args"]}\n' \
              f'版本：{__version__}\n运行时间：{process_time()}\n出现这个错误可能意味着程序有bug，请把错误信息和重现方法' \
              '告知作者，谢谢。\n报告网站：https://gitee.com/g1879/DrissionPage/issues'
        r = TimeoutError(txt) if result['type'] == 'timeout' else CDPError(txt)
    else:
        r = RuntimeError(result)

    if not ignore or not isinstance(r, ignore):
        raise r
