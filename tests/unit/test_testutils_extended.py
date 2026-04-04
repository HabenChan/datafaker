#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import tempfile
from datafaker.testutils import FileCreator, bytes_to_unitstr, unitstr_to_bytes, random_string


def test_random_string():
    """测试random_string函数"""
    s = random_string(8)
    assert len(s) == 8
    assert all(c.isalnum() for c in s)


def test_bytes_to_unitstr():
    """测试bytes_to_unitstr函数"""
    assert '1.0K' in bytes_to_unitstr(1024)
    assert '2.0M' in bytes_to_unitstr(2 * 1024 * 1024)
    assert '1.5G' in bytes_to_unitstr(int(1.5 * 1024 * 1024 * 1024))


def test_unitstr_to_bytes():
    """测试unitstr_to_bytes函数"""
    assert unitstr_to_bytes('1K') == 1024
    assert unitstr_to_bytes('2M') == 2 * 1024 * 1024
    assert unitstr_to_bytes('1.5G') == int(1.5 * 1024 * 1024 * 1024)


def test_file_creator():
    """测试FileCreator类"""
    fc = FileCreator()
    
    # 测试create_size_file方法
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, 'test.txt')
        created_path = fc.create_size_file(file_path, '1K')
        assert os.path.exists(created_path)
        assert os.path.getsize(created_path) == 1024
        
        # 测试不同大小
        created_path = fc.create_size_file(file_path, '2K')
        assert os.path.getsize(created_path) == 2048
        
        created_path = fc.create_size_file(file_path, '1M')
        assert os.path.getsize(created_path) == 1024 * 1024


def test_file_creator_with_dir():
    """测试FileCreator创建目录"""
    fc = FileCreator()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        sub_dir = os.path.join(temp_dir, 'subdir')
        file_path = os.path.join(sub_dir, 'test.txt')
        
        # 测试创建不存在的目录
        created_path = fc.create_file(file_path, 'test content')
        assert os.path.exists(created_path)
        assert os.path.exists(sub_dir)


def test_file_creator_create_file():
    """测试FileCreator.create_file方法"""
    fc = FileCreator()
    
    # 测试创建文件
    file_path = fc.create_file('test.txt', 'test content')
    assert os.path.exists(file_path)
    with open(file_path, 'r') as f:
        assert f.read() == 'test content'


def test_file_creator_append_file():
    """测试FileCreator.append_file方法"""
    fc = FileCreator()
    
    # 先创建文件
    file_path = fc.create_file('test.txt', 'initial content')
    # 追加内容
    fc.append_file('test.txt', ' appended content')
    # 验证内容
    with open(file_path, 'r') as f:
        assert f.read() == 'initial content appended content'


def test_file_creator_full_path():
    """测试FileCreator.full_path方法"""
    fc = FileCreator()
    full_path = fc.full_path('test.txt')
    assert isinstance(full_path, str)
    assert 'test.txt' in full_path
