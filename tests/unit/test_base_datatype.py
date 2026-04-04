#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from datafaker.datatypes.base import BaseDataType


class TestBaseDataType(unittest.TestCase):
    """测试 BaseDataType 类"""

    def setUp(self):
        """设置测试环境"""
        self.base_data_type = BaseDataType('zh_CN')

    def test_fake_inc(self):
        """测试 fake_inc 方法"""
        # 测试初始值
        result1 = self.base_data_type.fake_inc('test_mark', 10, 2)
        self.assertEqual(result1, 10)
        
        # 测试自增
        result2 = self.base_data_type.fake_inc('test_mark', 10, 2)
        self.assertEqual(result2, 12)
        
        # 测试不同标记
        result3 = self.base_data_type.fake_inc('another_mark')
        self.assertEqual(result3, 0)

    def test_fake_enum(self):
        """测试 fake_enum 方法"""
        # 测试枚举值
        result = self.base_data_type.fake_enum('a', 'b', 'c')
        self.assertIn(result, ['a', 'b', 'c'])

    def test_fake_order_enum(self):
        """测试 fake_order_enum 方法"""
        # 测试顺序枚举值
        result1 = self.base_data_type.fake_order_enum('a', 'b', 'c')
        self.assertEqual(result1, 'c')

    def test_fake_op(self):
        """测试 fake_op 方法"""
        # 测试操作方法
        result = self.base_data_type.fake_op('a', 'b', 'c')
        self.assertIsNone(result)

    def test_fake_str_pk(self):
        """测试 fake_str_pk 方法"""
        # 测试生成带前缀的自增字符串主键
        result1 = self.base_data_type.fake_str_pk('ID', 10)
        self.assertEqual(len(result1), 10)
        self.startswith(result1, 'ID')
        
        result2 = self.base_data_type.fake_str_pk('ID', 10)
        self.assertEqual(len(result2), 10)
        self.startswith(result2, 'ID')

    def test_fake_hash_pk(self):
        """测试 fake_hash_pk 方法"""
        # 测试生成哈希字符串主键
        result = self.base_data_type.fake_hash_pk(32)
        self.assertEqual(len(result), 32)

    def test_fake_composite_pk(self):
        """测试 fake_composite_pk 方法"""
        # 测试生成组合主键
        result = self.base_data_type.fake_composite_pk('a', 'b', 'c')
        self.assertEqual(result, 'a_b_c')

    def test_fake_random_str_pk(self):
        """测试 fake_random_str_pk 方法"""
        # 测试生成随机字符串主键
        result = self.base_data_type.fake_random_str_pk(16)
        self.assertEqual(len(result), 16)

    def test_do_fake(self):
        """测试 do_fake 方法"""
        # 测试调用自定义方法
        result1 = self.base_data_type.do_fake('inc', ['test_do_fake'], 1)
        self.assertEqual(result1, 0)
        
        # 测试调用 faker 方法
        result2 = self.base_data_type.do_fake('name', [], 1)
        self.assertIsInstance(result2, str)
        
        # 测试调用不存在的方法
        result3 = self.base_data_type.do_fake('nonexistent_method', [], 1)
        self.assertIsNone(result3)

    def startswith(self, string, prefix):
        """辅助方法：测试字符串是否以指定前缀开头"""
        self.assertTrue(string.startswith(prefix))


if __name__ == '__main__':
    unittest.main()