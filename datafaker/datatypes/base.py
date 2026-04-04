#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
from typing import Any, List, Union, Optional
from faker import Faker, Factory
from datafaker import compat
from datafaker.compat import Dict
import json
import uuid

class BaseDataType(object):
    
    def __init__(self, locale: str):
        self.faker: Faker = Factory().create(locale)
        self.faker_funcs: List[str] = dir(self.faker)
        self.lock = compat.Lock()
        self.auto_inc: Dict = Dict()
        self.current_num: int = 0
    
    def fake_inc(self, mark: str, start: Union[int, str] = 0, step: Union[int, str] = 1) -> int:
        """
        用于实现整型变量自增
        :param mark: 自增标记
        :param start: 起始值
        :param step: 步长
        :return: 当前值
        """
        step_int = int(step)
        # 快速路径：如果mark已经存在，直接获取锁并自增
        if mark in self.auto_inc:
            with self.lock:
                ret = self.auto_inc[mark]
                self.auto_inc[mark] += step_int
            return ret
        # 慢速路径：如果mark不存在，需要初始化
        with self.lock:
            if mark not in self.auto_inc:
                self.auto_inc[mark] = int(start)
            ret = self.auto_inc[mark]
            self.auto_inc[mark] += step_int
        return ret
    
    def fake_enum(self, *args: Any) -> Any:
        """
        实现枚举类型，随机返回一个列表中值
        :param args: 枚举数组
        :return: 随机选择的值
        """
        return random.choice(list(args))
    
    def fake_order_enum(self, *args: Any) -> Any:
        """
        用于循环顺序产生枚举值。常用于多列关联产生值
        :param args: 数组值
        :return: 顺序选择的值
        """
        datas = list(args)
        num = len(datas)
        idx = (self.current_num % num) - 1
        return datas[idx]
    
    def fake_op(self, *args: Any) -> None:
        """
        实现多字段四项运算
        :param args:
        :return: None
        """
        return None
    
    def fake_str_pk(self, prefix: str = "ID", digits: Union[int, str] = 8) -> str:
        """
        生成带前缀的自增字符串主键（如：ID00000001）
        :param prefix: 主键前缀
        :param digits: 总长度
        :return: 字符串主键
        """
        mark = f"str_pk_{prefix}"
        # 计算数字部分的位数（无锁操作）
        prefix_len = len(prefix)
        number_len = int(digits) - prefix_len
        # 确保数字部分至少有1位
        if number_len < 1:
            number_len = 1
        
        # 快速路径：如果mark已经存在，直接获取锁并自增
        if mark in self.auto_inc:
            with self.lock:
                current_val = self.auto_inc[mark]
                self.auto_inc[mark] += 1
            return f"{prefix}{str(current_val).zfill(number_len)}"
        
        # 慢速路径：如果mark不存在，需要初始化
        with self.lock:
            if mark not in self.auto_inc:
                self.auto_inc[mark] = 0
            current_val = self.auto_inc[mark]
            self.auto_inc[mark] += 1
        return f"{prefix}{str(current_val).zfill(number_len)}"
    
    def fake_hash_pk(self, length: int = 32) -> str:
        """
        生成哈希字符串主键（如UUID的简化版）
        :param length: 哈希长度（16/32/64）
        :return: 哈希字符串
        """
        return self.faker.sha256(raw_output=False)[:length]
    
    def fake_composite_pk(self, *parts: Any) -> str:
        """
        生成组合主键（多个字段用分隔符合并）
        :param parts: 要组合的值列表
        :return: 组合后的字符串
        """
        separator = "_"
        return separator.join(str(part) for part in parts)
    
    def fake_random_str_pk(self, length: int = 16, chars: str = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789") -> str:
        """
        生成随机字符串主键（避免易混淆字符）
        :param length: 字符串长度
        :param chars: 允许的字符集
        :return: 随机字符串
        """
        return ''.join(random.choices(chars, k=length))
    
    def do_fake(self, keyword: str, args: List[Any], current_num: int) -> Optional[Any]:
        """
        首先查看是否在faker类的成员函数内，如果在则调用；
        否者调用FakeData类中自定义的成员函数
        :param keyword: 数据类型关键字
        :param args: 参数列表
        :param current_num: 当前记录数
        :return: 生成的数据
        """
        self.current_num = current_num
        try:
            method = getattr(self, 'fake_' + keyword, None)
            if callable(method):
                return method(*args)
            if keyword in self.faker_funcs:
                method = getattr(self.faker, keyword, None)
                if callable(method):
                    return method(*args)
        except Exception as e:
            # 记录错误但不中断流程，返回None
            print(f"Error generating {keyword} data: {str(e)}")
        return None
