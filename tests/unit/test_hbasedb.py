#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from unittest.mock import patch, MagicMock

# 尝试导入 happybase 模块
try:
    import happybase
    HAPPYBASE_AVAILABLE = True
    from datafaker.dbs.hbasedb import HbaseDB
    from datafaker.exceptions import ParamError
    from datafaker.reg import reg_args
except ImportError:
    HAPPYBASE_AVAILABLE = False


@unittest.skipIf(not HAPPYBASE_AVAILABLE, "happybase not installed")
class TestHbaseDB(unittest.TestCase):
    """测试 HbaseDB 类"""

    def setUp(self):
        """设置测试环境"""
        # 创建一个模拟的 args 对象
        self.args = MagicMock()
        self.args.connect = 'localhost:9090'
        self.args.table = 'test_table'
        self.args.batch = 1000
        self.args.metaj = None
        
        # 创建 HbaseDB 实例
        self.hbasedb = HbaseDB(self.args)
        
        # 模拟列名
        self.hbasedb.column_names = ['id', 'name', 'age']

    @patch('datafaker.dbs.hbasedb.happybase.Connection')
    def test_init(self, mock_connection):
        """测试初始化方法"""
        # 模拟 table 对象
        mock_table = MagicMock()
        mock_connection.return_value.table.return_value = mock_table
        
        # 执行初始化
        self.hbasedb.init()
        
        # 验证 happybase.Connection 被正确调用
        mock_connection.assert_called_once_with(host='localhost', port=9090)
        # 验证 table 方法被正确调用
        mock_connection.return_value.table.assert_called_once_with('test_table')
        # 验证 table 属性被正确设置
        self.assertEqual(self.hbasedb.table, mock_table)

    def test_construct_self_rows(self):
        """测试 construct_self_rows 方法"""
        # 验证抛出 ParamError 异常
        with self.assertRaises(ParamError):
            self.hbasedb.construct_self_rows()

    def test_save_data_with_metaj(self):
        """测试带 metaj 参数的 save_data 方法"""
        # 设置 metaj 参数
        self.args.metaj = '{"name": "%s", "age": %s}'
        
        # 验证抛出 ParamError 异常
        with self.assertRaises(ParamError):
            self.hbasedb.save_data([['1', 'John', '25']])

    @patch('datafaker.dbs.hbasedb.happybase.Connection')
    def test_save_data_without_metaj(self, mock_connection):
        """测试不带 metaj 参数的 save_data 方法"""
        # 模拟 table 对象和 batch 方法
        mock_table = MagicMock()
        mock_batch = MagicMock()
        mock_table.batch.return_value.__enter__.return_value = mock_batch
        mock_connection.return_value.table.return_value = mock_table
        
        # 初始化 HbaseDB
        self.hbasedb.init()
        
        # 测试数据
        lines = [
            ['1', 'John', '25'],
            ['2', 'Jane', '30']
        ]
        
        # 执行方法
        self.hbasedb.save_data(lines)
        
        # 验证 batch 方法被正确调用
        mock_table.batch.assert_called_once_with(batch_size=1000)
        # 验证 put 方法被正确调用
        expected_calls = [
            unittest.mock.call('1', {'name': 'John', 'age': '25'}),
            unittest.mock.call('2', {'name': 'Jane', 'age': '30'})
        ]
        mock_batch.put.assert_has_calls(expected_calls)

    @patch('datafaker.dbs.hbasedb.happybase.Connection')
    def test_save_data_with_rowkey_args(self, mock_connection):
        """测试带行键参数的 save_data 方法"""
        # 模拟 table 对象和 batch 方法
        mock_table = MagicMock()
        mock_batch = MagicMock()
        mock_table.batch.return_value.__enter__.return_value = mock_batch
        mock_connection.return_value.table.return_value = mock_table
        
        # 初始化 HbaseDB
        self.hbasedb.init()
        
        # 修改列名，包含行键参数
        self.hbasedb.column_names = ['id{0}', 'name', 'age']
        
        # 测试数据
        lines = [
            ['1', 'John', '25'],
            ['2', 'Jane', '30']
        ]
        
        # 执行方法
        self.hbasedb.save_data(lines)
        
        # 验证 batch 方法被正确调用
        mock_table.batch.assert_called_once_with(batch_size=1000)
        # 验证 put 方法被正确调用
        expected_calls = [
            unittest.mock.call('1', {'name': 'John', 'age': '25'}),
            unittest.mock.call('2', {'name': 'Jane', 'age': '30'})
        ]
        mock_batch.put.assert_has_calls(expected_calls)


if __name__ == '__main__':
    unittest.main()