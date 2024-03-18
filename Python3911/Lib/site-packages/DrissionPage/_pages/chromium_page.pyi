# -*- coding:utf-8 -*-
"""
@Author   : g1879
@Contact  : g1879@qq.com
@Copyright: (c) 2024 by g1879, Inc. All Rights Reserved.
@License  : BSD 3-Clause.
"""
from pathlib import Path
from typing import Union, Tuple, List, Optional

from .._base.browser import Browser
from .._configs.chromium_options import ChromiumOptions
from .._pages.chromium_base import ChromiumBase
from .._pages.chromium_tab import ChromiumTab
from .._units.rect import TabRect
from .._units.setter import ChromiumPageSetter
from .._units.waiter import PageWaiter


class ChromiumPage(ChromiumBase):

    def __init__(self,
                 addr_or_opts: Union[str, int, ChromiumOptions] = None,
                 tab_id: str = None,
                 timeout: float = None):
        self._chromium_options: ChromiumOptions = ...
        self._browser: Browser = ...
        self._rect: Optional[TabRect] = ...

    def _handle_options(self, addr_or_opts: Union[str, ChromiumOptions]) -> str: ...

    def _run_browser(self) -> None: ...

    def _page_init(self) -> None: ...

    @property
    def browser(self) -> Browser: ...

    @property
    def tabs_count(self) -> int: ...

    @property
    def tabs(self) -> List[str]: ...

    @property
    def wait(self) -> PageWaiter: ...

    @property
    def main_tab(self) -> str: ...

    @property
    def latest_tab(self) -> str: ...

    @property
    def process_id(self) -> Optional[int]: ...

    @property
    def set(self) -> ChromiumPageSetter: ...

    def save(self,
             path: Union[str, Path] = None,
             name: str = None,
             as_pdf: bool = False,
             landscape: bool = ...,
             displayHeaderFooter: bool = ...,
             printBackground: bool = ...,
             scale: float = ...,
             paperWidth: float = ...,
             paperHeight: float = ...,
             marginTop: float = ...,
             marginBottom: float = ...,
             marginLeft: float = ...,
             marginRight: float = ...,
             pageRanges: str = ...,
             headerTemplate: str = ...,
             footerTemplate: str = ...,
             preferCSSPageSize: bool = ...,
             generateTaggedPDF: bool = ...,
             generateDocumentOutline: bool = ...) -> Union[bytes, str]: ...

    def get_tab(self, tab_id: Union[str, ChromiumTab, int] = None) -> ChromiumTab: ...

    def find_tabs(self, title: str = None, url: str = None,
                  tab_type: Union[str, list, tuple] = None, single: bool = True) -> Union[str, List[str]]: ...

    def new_tab(self, url: str = None, new_window: bool = False, background: bool = False,
                new_context: bool = False) -> ChromiumTab: ...

    def _new_tab(self, new_window: bool = False, background: bool = False, new_context: bool = False) -> str: ...

    def close(self) -> None: ...

    def close_tabs(self, tabs_or_ids: Union[str, ChromiumTab, List[Union[str, ChromiumTab]],
    Tuple[Union[str, ChromiumTab]]] = None, others: bool = False) -> None: ...

    def quit(self, timeout: float = 5, force: bool = True) -> None: ...


def get_rename(original: str, rename: str) -> str: ...
