#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from unittest.mock import patch, MagicMock
import json

# 尝试导入 kafka 模块
try:
    from kafka import KafkaProducer
    KAFKA_AVAILABLE = True
    from datafaker.dbs.kafkadb import KafkaDB
    from datafaker.utils import json_item
except ImportError:
    KAFKA_AVAILABLE = False


@unittest.skipIf(not KAFKA_AVAILABLE, "kafka not installed")
class TestKafkaDB(unittest.TestCase):
    """测试 KafkaDB 类"""

    def setUp(self):
        """设置测试环境"""
        # 创建一个模拟的 args 对象
        self.args = MagicMock()
        self.args.connect = 'localhost:9092'
        self.args.table = 'test_topic'
        self.args.num = 10
        self.args.interval = None
        self.args.outprint = False
        self.args.locale = 'en_US'
        self.args.metaj = None
        
        # 创建 KafkaDB 实例
        self.kafkadb = KafkaDB(self.args)
        
        # 模拟列名
        self.kafkadb.column_names = ['id', 'name', 'age']
        # 模拟 fake_column 方法
        self.kafkadb.fake_column = MagicMock(return_value=['1', 'John', '25'])

    @patch('datafaker.dbs.kafkadb.KafkaProducer')
    def test_init(self, mock_kafka_producer):
        """测试初始化方法"""
        # 执行初始化
        self.kafkadb.init()
        
        # 验证 KafkaProducer 被正确初始化
        mock_kafka_producer.assert_called_once_with(bootstrap_servers='localhost:9092')
        # 验证 producer 属性被正确设置
        self.assertEqual(self.kafkadb.producer, mock_kafka_producer.return_value)

    def test_construct_self_rows(self):
        """测试 construct_self_rows 方法"""
        # 执行方法
        rows = self.kafkadb.construct_self_rows()
        
        # 验证返回值
        self.assertEqual(rows, [])

    def test_format_data_without_metaj(self):
        """测试不带 metaj 参数的 format_data 方法"""
        # 测试数据
        columns = ['1', 'John', '25']
        
        # 执行方法
        result = self.kafkadb.format_data(columns)
        
        # 验证结果
        expected = json.dumps({'id': '1', 'name': 'John', 'age': '25'})
        self.assertEqual(result, expected)

    def test_format_data_with_metaj(self):
        """测试带 metaj 参数的 format_data 方法"""
        # 设置 metaj 参数
        self.args.metaj = '{"id": "%s", "name": "%s", "age": "%s"}'
        # 重新创建 KafkaDB 实例以应用 metaj 参数
        self.kafkadb = KafkaDB(self.args)
        # 重新设置列名
        self.kafkadb.column_names = ['id', 'name', 'age']
        
        # 测试数据
        columns = ['1', 'John', '25']
        
        # 执行方法
        result = self.kafkadb.format_data(columns)
        
        # 验证结果
        expected = '{"id": "1", "name": "John", "age": "25"}'
        self.assertEqual(result, expected)

    @patch('datafaker.dbs.kafkadb.KafkaProducer')
    def test_save_data(self, mock_kafka_producer):
        """测试 save_data 方法"""
        # 初始化 KafkaDB
        self.kafkadb.init()
        
        # 测试数据
        content = '{"id": "1", "name": "John", "age": "25"}'
        
        # 执行方法
        self.kafkadb.save_data(content)
        
        # 验证 send 方法被正确调用
        mock_kafka_producer.return_value.send.assert_called_once_with('test_topic', bytes(content.encode('utf-8')))

    @patch('datafaker.dbs.kafkadb.KafkaProducer')
    @patch('time.sleep')
    def test_do_fake(self, mock_sleep, mock_kafka_producer):
        """测试 do_fake 方法"""
        # 初始化 KafkaDB
        self.kafkadb.init()
        # 设置 num 为 1，只生成一条数据
        self.args.num = 1
        
        # 执行方法
        self.kafkadb.do_fake()
        
        # 验证 fake_column 被调用
        self.kafkadb.fake_column.assert_called_once_with(1)
        # 验证 send 方法被调用
        mock_kafka_producer.return_value.send.assert_called_once()

    @patch('datafaker.dbs.kafkadb.KafkaProducer')
    @patch('time.sleep')
    def test_do_fake_with_interval(self, mock_sleep, mock_kafka_producer):
        """测试带 interval 参数的 do_fake 方法"""
        # 初始化 KafkaDB
        self.kafkadb.init()
        # 设置 num 为 1，只生成一条数据
        self.args.num = 1
        # 设置 interval 为 0.1
        self.args.interval = 0.1
        
        # 执行方法
        self.kafkadb.do_fake()
        
        # 验证 fake_column 被调用
        self.kafkadb.fake_column.assert_called_once_with(1)
        # 验证 send 方法被调用
        mock_kafka_producer.return_value.send.assert_called_once()
        # 验证 sleep 被调用
        mock_sleep.assert_called_once_with(0.1)


if __name__ == '__main__':
    unittest.main()