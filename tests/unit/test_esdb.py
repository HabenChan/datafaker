#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from unittest.mock import patch, MagicMock
import json

# 尝试导入 elasticsearch 模块
try:
    from elasticsearch import Elasticsearch
    ELASTICSEARCH_AVAILABLE = True
    from datafaker.dbs.esdb import EsDB
    from datafaker.exceptions import ParamError
except ImportError:
    ELASTICSEARCH_AVAILABLE = False


@unittest.skipIf(not ELASTICSEARCH_AVAILABLE, "elasticsearch not installed")
class TestEsDB(unittest.TestCase):
    """测试 EsDB 类"""

    def setUp(self):
        """设置测试环境"""
        # 创建一个模拟的 args 对象
        self.args = MagicMock()
        self.args.connect = 'localhost:9200'
        self.args.table = 'test_index/test_type'
        self.args.auth = None
        self.args.metaj = None
        
        # 创建 EsDB 实例
        self.esdb = EsDB(self.args)
        
        # 模拟列名
        self.esdb.column_names = ['name', 'age']

    @patch('datafaker.dbs.esdb.Elasticsearch')
    def test_init(self, mock_elasticsearch):
        """测试初始化方法"""
        # 执行初始化
        self.esdb.init()
        
        # 验证 Elasticsearch 被正确初始化
        mock_elasticsearch.assert_called_once_with(['localhost:9200'], http_auth=None)
        
        # 验证 index 和 type 被正确设置
        self.assertEqual(self.esdb.index, 'test_index')
        self.assertEqual(self.esdb.type, 'test_type')

    @patch('datafaker.dbs.esdb.Elasticsearch')
    def test_init_with_auth(self, mock_elasticsearch):
        """测试带认证的初始化方法"""
        # 设置认证信息
        self.args.auth = 'user:pass'
        
        # 执行初始化
        self.esdb.init()
        
        # 验证 Elasticsearch 被正确初始化
        mock_elasticsearch.assert_called_once_with(['localhost:9200'], http_auth=['user', 'pass'])

    def test_construct_self_rows(self):
        """测试 construct_self_rows 方法"""
        # 验证抛出 ParamError 异常
        with self.assertRaises(ParamError):
            self.esdb.construct_self_rows()

    def test_format_data_without_metaj(self):
        """测试不带 metaj 参数的 format_data 方法"""
        # 测试数据
        columns = ['John', 25]
        
        # 执行方法
        result = self.esdb.format_data(columns)
        
        # 验证结果
        expected = {'name': 'John', 'age': 25}
        self.assertEqual(result, expected)

    def test_format_data_with_metaj(self):
        """测试带 metaj 参数的 format_data 方法"""
        # 设置 metaj 参数
        self.args.metaj = '{"name": "%s", "age": %s}'
        
        # 测试数据
        columns = ['John', 25]
        
        # 执行方法
        result = self.esdb.format_data(columns)
        
        # 验证结果
        expected = {'name': 'John', 'age': 25}
        self.assertEqual(result, expected)

    @patch('datafaker.dbs.esdb.bulk')
    @patch('datafaker.dbs.esdb.Elasticsearch')
    def test_save_data(self, mock_elasticsearch, mock_bulk):
        """测试 save_data 方法"""
        # 初始化 ES 连接
        self.esdb.init()
        
        # 设置 mock_bulk 的返回值
        mock_bulk.return_value = (2, [])
        
        # 测试数据
        lines = [
            ['John', 25],
            ['Jane', 30]
        ]
        
        # 执行方法
        self.esdb.save_data(lines)
        
        # 验证 bulk 被正确调用
        expected_actions = [
            {
                "_index": "test_index",
                "_type": "test_type",
                "_source": {"name": "John", "age": 25}
            },
            {
                "_index": "test_index",
                "_type": "test_type",
                "_source": {"name": "Jane", "age": 30}
            }
        ]
        mock_bulk.assert_called_once_with(
            self.esdb.es, 
            expected_actions, 
            index='test_index/test_type', 
            raise_on_error=True
        )


if __name__ == '__main__':
    unittest.main()