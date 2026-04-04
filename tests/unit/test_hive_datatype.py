#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datafaker.constant import DEFAULT_LOCALE
from datafaker.datatypes.hive import HiveDataType

hive_fakedata = HiveDataType(DEFAULT_LOCALE)


def test_hive_number():
    """测试Hive NUMBER类型"""
    # 测试默认参数
    number_val1 = hive_fakedata.fake_number()
    assert isinstance(number_val1, int)
    
    # 测试指定位数
    number_val2 = hive_fakedata.fake_number(5)
    assert isinstance(number_val2, int)
    assert len(str(abs(number_val2))) <= 5
    
    # 测试固定长度
    number_val3 = hive_fakedata.fake_number(3, 1)
    assert isinstance(number_val3, int)
    assert len(str(abs(number_val3))) == 3
    
    # 测试正数
    number_val4 = hive_fakedata.fake_number(3, 0, 1)
    assert isinstance(number_val4, int)
    assert number_val4 >= 0
    
    # 测试负数
    number_val5 = hive_fakedata.fake_number(3, 0, -1)
    assert isinstance(number_val5, int)
    assert number_val5 <= 0


def test_hive_string():
    """测试Hive STRING类型"""
    string_val = hive_fakedata.fake_string()
    assert isinstance(string_val, str)


def test_hive_age():
    """测试Hive AGE类型"""
    # 测试默认参数
    age_val1 = hive_fakedata.fake_age()
    assert isinstance(age_val1, int)
    assert 0 <= age_val1 <= 120
    
    # 测试指定范围
    age_val2 = hive_fakedata.fake_age(18, 60)
    assert isinstance(age_val2, int)
    assert 18 <= age_val2 <= 60
