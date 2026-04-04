#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datafaker.reg import (
    reg_keyword, reg_all_keywords, reg_replace_keywords, reg_args, 
    reg_cmd, reg_float, reg_integer, reg_int, reg_all_int, reg_int_first, 
    reg_date, reg_start, reg_all_chinese, reg_match, reg_search
)


def test_reg_keyword():
    """测试reg_keyword函数"""
    assert reg_keyword('[:test]') == 'test'
    assert reg_keyword('prefix[:test]suffix') == 'test'
    assert reg_keyword('no keyword') is None


def test_reg_all_keywords():
    """测试reg_all_keywords函数"""
    assert reg_all_keywords('[:test1] [:test2]') == ['test1', 'test2']
    assert reg_all_keywords('no keywords') is None


def test_reg_replace_keywords():
    """测试reg_replace_keywords函数"""
    assert reg_replace_keywords('[:test]', '%s') == '%s'
    assert reg_replace_keywords('prefix[:test]suffix', '%s') == 'prefix%ssuffix'


def test_reg_args():
    """测试reg_args函数"""
    assert reg_args('test()') == ['']
    assert reg_args('test(1,2,3)') == ['1', '2', '3']
    assert reg_args('test') == []


def test_reg_cmd():
    """测试reg_cmd函数"""
    assert reg_cmd('test()') == 'test'
    assert reg_cmd('test') == 'test'


def test_reg_float():
    """测试reg_float函数"""
    assert reg_float('123.45') == 123.45
    assert reg_float('no float') == 0


def test_reg_integer():
    """测试reg_integer函数"""
    assert reg_integer('123abc456') == ['123', '456']


def test_reg_int():
    """测试reg_int函数"""
    assert reg_int('123abc') == 123
    assert reg_int('no int') == 0


def test_reg_all_int():
    """测试reg_all_int函数"""
    assert reg_all_int('123abc456') == [123, 456]


def test_reg_int_first():
    """测试reg_int_first函数"""
    assert reg_int_first('123abc456') == 123
    assert reg_int_first('no int') is None


def test_reg_date():
    """测试reg_date函数"""
    assert reg_date('2023-01-01') == '2023-01-01'
    assert reg_date('2023年01月01日') == '2023年01月01日'
    assert reg_date('no date') == ''


def test_reg_start():
    """测试reg_start函数"""
    assert reg_start('prefix test suffix', 'prefix') == 'test'
    assert reg_start('no match', 'prefix') == ''


def test_reg_all_chinese():
    """测试reg_all_chinese函数"""
    assert reg_all_chinese('hello 你好 world 世界') == ['你', '好', '世', '界']


def test_reg_match():
    """测试reg_match函数"""
    assert reg_match(r'^test', 'test123') is not None
    assert reg_match(r'^test', '123test') is None


def test_reg_search():
    """测试reg_search函数"""
    assert reg_search(r'test', '123test456') is not None
    assert reg_search(r'test', 'no match') is None
