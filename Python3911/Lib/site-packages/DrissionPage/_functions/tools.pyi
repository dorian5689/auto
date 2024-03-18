# -*- coding:utf-8 -*-
"""
@Author   : g1879
@Contact  : g1879@qq.com
@Copyright: (c) 2024 by g1879, Inc. All Rights Reserved.
@License  : BSD 3-Clause.
"""
from os import popen
from pathlib import Path
from typing import Union
from types import FunctionType

from .._pages.chromium_page import ChromiumPage


def port_is_using(ip: str, port: Union[str, int]) -> bool: ...


def clean_folder(folder_path: Union[str, Path], ignore: Union[tuple, list] = None) -> None: ...


def show_or_hide_browser(page: ChromiumPage, hide: bool = True) -> None: ...


def get_browser_progress_id(progress: Union[popen, None], address: str) -> Union[str, None]: ...


def get_chrome_hwnds_from_pid(pid: Union[str, int], title: str) -> list: ...


def wait_until(page, condition: Union[FunctionType, str, tuple], timeout: float, poll: float, raise_err: bool): ...


def stop_process_on_port(port: Union[int, str]) -> None: ...


def configs_to_here(file_name: Union[Path, str] = None) -> None: ...


def raise_error(result: dict, ignore=None) -> None: ...
