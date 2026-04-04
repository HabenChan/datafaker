#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from typing import Any, Optional
from datafaker.datatypes.base import BaseDataType

class HiveDataType(BaseDataType):
    
    ############ hive 基本数据类型 #############
    
    def fake_number(self, digits: Optional[int] = None, fix_len: int = 0, positive: int = 0) -> int:
        """
        digits=None, fix_len=0, positive=0
        
        :param digits: 数字位数
        :param fix_len: 是否固定长度
        :param positive: 是否为正数
        :return: 生成的数字
        """
        fixlen = (fix_len == 1)
        val = self.faker.random_number(digits=digits, fix_len=fixlen)
        if positive > 0:
            val = val if val >= 0 else -val
        if positive < 0:
            val = val if val <= 0 else -val
        return val
    
    def fake_string(self, *args: Any) -> str:
        return self.faker.pystr(*args)
    
    ####### 定制函数 ##########
    def fake_age(self, *args: Any) -> int:
        if not args:
            args = [0, 120]
        return self.faker.random_int(*args)
