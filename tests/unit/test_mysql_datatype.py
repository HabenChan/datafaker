#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from datafaker.datatypes.mysql import MySQLDataType
from datafaker.constant import DEFAULT_LOCALE


class TestMySQLDataType(unittest.TestCase):
    """测试 MySQL 数据类型类"""

    def setUp(self):
        """设置测试环境"""
        self.mysql_data_type = MySQLDataType(DEFAULT_LOCALE)

    def test_fake_tinyint(self):
        """测试 fake_tinyint 方法"""
        # 测试有符号 tinyint
        result = self.mysql_data_type.fake_tinyint()
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, -128)
        self.assertLessEqual(result, 127)
        
        # 测试无符号 tinyint
        result = self.mysql_data_type.fake_tinyint(unsigned=True)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 255)

    def test_fake_smallint(self):
        """测试 fake_smallint 方法"""
        # 测试有符号 smallint
        result = self.mysql_data_type.fake_smallint()
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, -32768)
        self.assertLessEqual(result, 32767)
        
        # 测试无符号 smallint
        result = self.mysql_data_type.fake_smallint(unsigned=True)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 65535)

    def test_fake_mediumint(self):
        """测试 fake_mediumint 方法"""
        # 测试有符号 mediumint
        result = self.mysql_data_type.fake_mediumint()
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, -8388608)
        self.assertLessEqual(result, 8388607)
        
        # 测试无符号 mediumint
        result = self.mysql_data_type.fake_mediumint(unsigned=True)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 16777215)

    def test_fake_int(self):
        """测试 fake_int 方法"""
        # 测试有符号 int
        result = self.mysql_data_type.fake_int()
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, -2147483648)
        self.assertLessEqual(result, 2147483647)
        
        # 测试无符号 int
        result = self.mysql_data_type.fake_int(unsigned=True)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 4294967295)
        
        # 测试指定范围的 int
        result = self.mysql_data_type.fake_int(min=10, max=20)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 10)
        self.assertLessEqual(result, 20)

    def test_fake_integer(self):
        """测试 fake_integer 方法"""
        result = self.mysql_data_type.fake_integer()
        self.assertIsInstance(result, int)

    def test_fake_bigint(self):
        """测试 fake_bigint 方法"""
        # 测试有符号 bigint
        result = self.mysql_data_type.fake_bigint()
        self.assertIsInstance(result, int)
        
        # 测试无符号 bigint
        result = self.mysql_data_type.fake_bigint(unsigned=True)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)

    def test_fake_float(self):
        """测试 fake_float 方法"""
        result = self.mysql_data_type.fake_float()
        self.assertIsInstance(result, float)

    def test_fake_double(self):
        """测试 fake_double 方法"""
        result = self.mysql_data_type.fake_double()
        self.assertIsInstance(result, float)

    def test_fake_time(self):
        """测试 fake_time 方法"""
        result = self.mysql_data_type.fake_time()
        self.assertIsInstance(result, str)

    def test_fake_year(self):
        """测试 fake_year 方法"""
        result = self.mysql_data_type.fake_year()
        self.assertIsInstance(result, str)

    def test_fake_datetime(self):
        """测试 fake_datetime 方法"""
        # 测试默认情况
        result = self.mysql_data_type.fake_datetime()
        self.assertIsInstance(result, str)
        
        # 测试使用当前时间
        result = self.mysql_data_type.fake_datetime(now=1)
        self.assertIsInstance(result, str)

    def test_fake_timestamp(self):
        """测试 fake_timestamp 方法"""
        # 测试默认情况
        result = self.mysql_data_type.fake_timestamp()
        # 可以是整数或浮点数
        self.assertIsInstance(result, (int, float))
        
        # 测试使用当前时间
        result = self.mysql_data_type.fake_timestamp(now=1)
        self.assertIsInstance(result, int)

    def test_fake_varchar(self):
        """测试 fake_varchar 方法"""
        # 测试默认情况
        result = self.mysql_data_type.fake_varchar()
        self.assertIsInstance(result, str)
        self.assertGreaterEqual(len(result), 1)
        self.assertLessEqual(len(result), 255)
        
        # 测试指定最大长度
        result = self.mysql_data_type.fake_varchar(max_chars=50)
        self.assertIsInstance(result, str)
        self.assertGreaterEqual(len(result), 1)
        self.assertLessEqual(len(result), 50)

    def test_fake_text(self):
        """测试 fake_text 方法"""
        # 测试默认情况
        result = self.mysql_data_type.fake_text()
        self.assertIsInstance(result, str)
        self.assertLessEqual(len(result), 65535)
        
        # 测试指定最大长度
        result = self.mysql_data_type.fake_text(1000)
        self.assertIsInstance(result, str)
        self.assertLessEqual(len(result), 1000)


if __name__ == '__main__':
    unittest.main()