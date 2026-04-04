#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import tempfile
import json
from datafaker.utils import (
    read_file, read_file_lines, process_op_args, 
    save2file, json_item, diffdate, count_time
)


def test_process_op_args():
    """测试process_op_args函数"""
    assert process_op_args('c12*c2+c22', 'columns') == 'columns[12]*columns[2]+columns[22]'
    assert process_op_args('c0', 'data') == 'data[0]'
    assert process_op_args('c100', 'items') == 'items[100]'


def test_read_file():
    """测试read_file函数"""
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write('test content')
        temp_file = f.name
    
    try:
        content = read_file(temp_file)
        assert content == 'test content'
    finally:
        os.unlink(temp_file)


def test_read_file_lines():
    """测试read_file_lines函数"""
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write('line1\nline2\nline3')
        temp_file = f.name
    
    try:
        lines = read_file_lines(temp_file)
        assert len(lines) == 3
        assert lines[0] == 'line1'
        assert lines[1] == 'line2'
        assert lines[2] == 'line3'
    finally:
        os.unlink(temp_file)


def test_save2file():
    """测试save2file函数"""
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        temp_file = f.name
    
    try:
        items = ['line1\n', 'line2\n']
        save2file(items, temp_file)
        with open(temp_file, 'r', encoding='utf-8') as f:
            content = f.read()
        assert content == 'line1\nline2\n'
    finally:
        os.unlink(temp_file)


def test_json_item():
    """测试json_item函数"""
    column_names = ['id', 'name', 'age']
    item = [1, 'test', 20]
    json_str = json_item(column_names, item)
    data = json.loads(json_str)
    assert data['id'] == 1
    assert data['name'] == 'test'
    assert data['age'] == 20


def test_diffdate():
    """测试diffdate函数"""
    assert diffdate('2023-01-01', '2023-01-02') == 1
    assert diffdate('2023-01-02', '2023-01-01') == -1
    assert diffdate('2023-01-01', '2023-01-01') == 0


def test_count_time():
    """测试count_time装饰器"""
    @count_time
    def test_func():
        pass
    
    # 只需测试装饰器不抛出异常
    test_func()

