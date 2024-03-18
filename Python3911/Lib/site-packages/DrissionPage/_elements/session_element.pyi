# -*- coding:utf-8 -*-
"""
@Author   : g1879
@Contact  : g1879@qq.com
@Copyright: (c) 2024 by g1879, Inc. All Rights Reserved.
@License  : BSD 3-Clause.
"""
from typing import Union, List, Tuple, Optional

from lxml.html import HtmlElement

from .none_element import NoneElement
from .._base.base import DrissionElement, BaseElement
from .._elements.chromium_element import ChromiumElement
from .._pages.chromium_base import ChromiumBase
from .._pages.chromium_frame import ChromiumFrame
from .._pages.session_page import SessionPage


class SessionElement(DrissionElement):

    def __init__(self, ele: HtmlElement, page: Union[SessionPage, None] = None):
        self._inner_ele: HtmlElement = ...
        self.page: SessionPage = ...

    @property
    def inner_ele(self) -> HtmlElement: ...

    def __repr__(self) -> str: ...

    def __call__(self,
                 loc_or_str: Union[Tuple[str, str], str],
                 timeout: float = None) -> Union[SessionElement, NoneElement]: ...

    def __eq__(self, other: SessionElement) -> bool: ...

    @property
    def tag(self) -> str: ...

    @property
    def html(self) -> str: ...

    @property
    def inner_html(self) -> str: ...

    @property
    def attrs(self) -> dict: ...

    @property
    def text(self) -> str: ...

    @property
    def raw_text(self) -> str: ...

    def parent(self,
               level_or_loc: Union[tuple, str, int] = 1,
               index: int = 1) -> Union[SessionElement, NoneElement]: ...

    def child(self,
              filter_loc: Union[tuple, str, int] = '',
              index: int = 1,
              timeout: float = None,
              ele_only: bool = True) -> Union[SessionElement, str, NoneElement]: ...

    def prev(self,
             filter_loc: Union[tuple, str, int] = '',
             index: int = 1,
             timeout: float = None,
             ele_only: bool = True) -> Union[SessionElement, str, NoneElement]: ...

    def next(self,
             filter_loc: Union[tuple, str, int] = '',
             index: int = 1,
             timeout: float = None,
             ele_only: bool = True) -> Union[SessionElement, str, NoneElement]: ...

    def before(self,
               filter_loc: Union[tuple, str, int] = '',
               index: int = 1,
               timeout: float = None,
               ele_only: bool = True) -> Union[SessionElement, str, NoneElement]: ...

    def after(self,
              filter_loc: Union[tuple, str, int] = '',
              index: int = 1,
              timeout: float = None,
              ele_only: bool = True) -> Union[SessionElement, str, NoneElement]: ...

    def children(self,
                 filter_loc: Union[tuple, str] = '',
                 timeout: float = None,
                 ele_only: bool = True) -> List[Union[SessionElement, str]]: ...

    def prevs(self,
              filter_loc: Union[tuple, str] = '',
              timeout: float = None,
              ele_only: bool = True) -> List[Union[SessionElement, str]]: ...

    def nexts(self,
              filter_loc: Union[tuple, str] = '',
              timeout: float = None,
              ele_only: bool = True) -> List[Union[SessionElement, str]]: ...

    def befores(self,
                filter_loc: Union[tuple, str] = '',
                timeout: float = None,
                ele_only: bool = True) -> List[Union[SessionElement, str]]: ...

    def afters(self,
               filter_loc: Union[tuple, str] = '',
               timeout: float = None,
               ele_only: bool = True) -> List[Union[SessionElement, str]]: ...

    def attr(self, attr: str) -> Optional[str]: ...

    def ele(self,
            loc_or_str: Union[Tuple[str, str], str],
            timeout: float = None) -> Union[SessionElement, NoneElement]: ...

    def eles(self,
             loc_or_str: Union[Tuple[str, str], str],
             timeout: float = None) -> List[SessionElement]: ...

    def s_ele(self,
              loc_or_str: Union[Tuple[str, str], str] = None) -> Union[SessionElement, NoneElement]: ...

    def s_eles(self,
               loc_or_str: Union[Tuple[str, str], str]) -> List[SessionElement]: ...

    def _find_elements(self,
                       loc_or_str: Union[Tuple[str, str], str],
                       timeout: float = None,
                       single: bool = True,
                       relative: bool = False,
                       raise_err: bool = None) \
            -> Union[SessionElement, NoneElement, List[SessionElement]]: ...

    def _get_ele_path(self, mode: str) -> str: ...


def make_session_ele(html_or_ele: Union[str, SessionElement, SessionPage, ChromiumElement, BaseElement, ChromiumFrame,
ChromiumBase],
                     loc: Union[str, Tuple[str, str]] = None,
                     single: bool = True) -> Union[
    SessionElement, NoneElement, List[SessionElement]]: ...
