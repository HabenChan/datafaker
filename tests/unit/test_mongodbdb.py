#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os

# 检查 pymongo 是否安装
pymongo_installed = False
try:
    import pymongo
    pymongo_installed = True
    from datafaker.dbs.mongodbdb import MongoDB
except ImportError:
    pass


@unittest.skipIf(not pymongo_installed, "pymongo not installed")
class TestMongoDB(unittest.TestCase):
    """测试 MongoDB 类"""

    def setUp(self):
        """设置测试环境"""
        # 创建模拟参数
        self.mock_args = MagicMock()
        self.mock_args.connect = 'mongodb://localhost:27017/test'
        self.mock_args.table = 'test_collection'
        self.mock_args.num = 10
        self.mock_args.workers = 1
        self.mock_args.batch = 10
        self.mock_args.interval = None
        self.mock_args.outprint = False
        self.mock_args.format = 'text'
        self.mock_args.outspliter = ','
        self.mock_args.locale = 'zh_CN'
        self.mock_args.meta = None
        self.mock_args.metaj = None
        self.mock_args.withheader = False
        
        # 模拟 schema
        self.mock_schema = [
            {'name': 'id', 'type': 'int', 'comment': '[:inc]', 'cmd': 'inc', 'args': []},
            {'name': 'name', 'type': 'varchar', 'comment': '[:name]', 'cmd': 'name', 'args': []}
        ]

    def test_init(self):
        """测试初始化方法"""
        # 模拟 parse_schema 方法和 pymongo.MongoClient
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
            with patch('pymongo.MongoClient') as mock_client:
                # 模拟 client 对象
                mock_db = MagicMock()
                mock_client.return_value.__getitem__.return_value = mock_db
                # 模拟 collection 对象
                mock_collection = MagicMock()
                mock_db.__getitem__.return_value = mock_collection
                
                # 创建 MongoDB 实例
                db = MongoDB(self.mock_args)
                
                # 验证初始化
                mock_client.assert_called_once_with('mongodb://localhost:27017/test')
                mock_db.__getitem__.assert_called_once_with('test_collection')
                self.assertEqual(db.collection, mock_collection)

    def test_construct_self_rows(self):
        """测试 construct_self_rows 方法"""
        # 模拟 parse_schema 方法和 pymongo.MongoClient
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
            with patch('pymongo.MongoClient') as mock_client:
                # 模拟 client 对象
                mock_db = MagicMock()
                mock_client.return_value.__getitem__.return_value = mock_db
                # 模拟 collection 对象
                mock_collection = MagicMock()
                mock_db.__getitem__.return_value = mock_collection
                
                # 创建 MongoDB 实例
                db = MongoDB(self.mock_args)
                
                # 测试 construct_self_rows 方法
                rows = db.construct_self_rows()
                self.assertEqual(rows, [])

    def test_save_data(self):
        """测试 save_data 方法"""
        # 模拟 parse_schema 方法和 pymongo.MongoClient
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
            with patch('pymongo.MongoClient') as mock_client:
                # 模拟 client 对象
                mock_db = MagicMock()
                mock_client.return_value.__getitem__.return_value = mock_db
                # 模拟 collection 对象
                mock_collection = MagicMock()
                mock_db.__getitem__.return_value = mock_collection
                
                # 创建 MongoDB 实例
                db = MongoDB(self.mock_args)
                
                # 测试 save_data 方法
                test_data = [[1, 'test1'], [2, 'test2']]
                db.save_data(test_data)
                
                # 验证 insert_many 被调用
                mock_collection.insert_many.assert_called_once()


if __name__ == '__main__':
    unittest.main()