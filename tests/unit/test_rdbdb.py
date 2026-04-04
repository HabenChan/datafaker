#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from unittest.mock import patch, MagicMock

from datafaker.dbs.rdbdb import RdbDB
from datafaker.constant import STR_TYPES


class TestRdbDB(unittest.TestCase):
    """测试 RdbDB 类"""

    def setUp(self):
        """设置测试环境"""
        # 创建模拟参数
        self.mock_args = MagicMock()
        self.mock_args.connect = 'mysql://localhost:3306/test_db'
        self.mock_args.table = 'test_table'
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
            {'name': 'id', 'type': 'int', 'comment': '[:inc]', 'cmd': 'inc', 'args': [], 'ctype': 'int'},
            {'name': 'name', 'type': 'varchar', 'comment': '[:name]', 'cmd': 'name', 'args': [], 'ctype': 'varchar'}
        ]

    def test_init(self):
        """测试初始化方法"""
        # 创建一个 RdbDB 子类实例
        class TestDB(RdbDB):
            def construct_self_rows(self):
                return []
        
        # 模拟 parse_schema 方法和 load_sqlalchemy 方法
        with patch('datafaker.dbs.rdbdb.BaseDB.parse_schema', return_value=self.mock_schema):
            with patch('datafaker.dbs.rdbdb.load_sqlalchemy', return_value=MagicMock()):
                db = TestDB(self.mock_args)
                # 验证 session 属性被设置
                self.assertIsNotNone(db.session)

    def test_save_data(self):
        """测试 save_data 方法"""
        # 创建一个 RdbDB 子类实例
        class TestDB(RdbDB):
            def construct_self_rows(self):
                return []
        
        # 模拟 parse_schema 方法和 load_sqlalchemy 方法
        with patch('datafaker.dbs.rdbdb.BaseDB.parse_schema', return_value=self.mock_schema):
            with patch('datafaker.dbs.rdbdb.load_sqlalchemy', return_value=MagicMock()):
                db = TestDB(self.mock_args)
                # 模拟 save_other_rdb 方法
                db.save_other_rdb = MagicMock()
                
                # 测试数据
                lines = [[1, 'test'], [2, 'test2']]
                
                # 执行方法
                db.save_data(lines)
                
                # 验证 save_other_rdb 被调用
                db.save_other_rdb.assert_called_once()

    def test_save_data_oracle(self):
        """测试 save_data 方法（Oracle 数据库）"""
        # 创建一个 RdbDB 子类实例
        class TestDB(RdbDB):
            def construct_self_rows(self):
                return []
        
        # 设置为 Oracle 连接
        self.mock_args.connect = 'oracle://localhost:1521/test_db'
        
        # 模拟 parse_schema 方法和 load_sqlalchemy 方法
        with patch('datafaker.dbs.rdbdb.BaseDB.parse_schema', return_value=self.mock_schema):
            with patch('datafaker.dbs.rdbdb.load_sqlalchemy', return_value=MagicMock()):
                db = TestDB(self.mock_args)
                # 模拟 save_oracle 方法
                db.save_oracle = MagicMock()
                
                # 测试数据
                lines = [[1, 'test'], [2, 'test2']]
                
                # 执行方法
                db.save_data(lines)
                
                # 验证 save_oracle 被调用
                db.save_oracle.assert_called_once()

    def test_save_other_rdb(self):
        """测试 save_other_rdb 方法"""
        # 创建一个 RdbDB 子类实例
        class TestDB(RdbDB):
            def construct_self_rows(self):
                return []
        
        # 模拟 parse_schema 方法和 load_sqlalchemy 方法
        mock_session = MagicMock()
        with patch('datafaker.dbs.rdbdb.BaseDB.parse_schema', return_value=self.mock_schema):
            with patch('datafaker.dbs.rdbdb.load_sqlalchemy', return_value=mock_session):
                db = TestDB(self.mock_args)
                
                # 测试数据
                lines = [[1, 'test'], [2, 'test2']]
                names_format = "(%s,'%s')"
                column_names = 'id,name'
                
                # 执行方法
                db.save_other_rdb(lines, names_format, column_names)
                
                # 验证 session.execute 被调用
                expected_sql = "insert into test_table (id,name) values (1,'test'),(2,'test2')"
                mock_session.execute.assert_called_once_with(expected_sql)
                # 验证 session.commit 被调用
                mock_session.commit.assert_called_once()

    def test_save_oracle(self):
        """测试 save_oracle 方法"""
        # 创建一个 RdbDB 子类实例
        class TestDB(RdbDB):
            def construct_self_rows(self):
                return []
        
        # 模拟 parse_schema 方法和 load_sqlalchemy 方法
        mock_session = MagicMock()
        with patch('datafaker.dbs.rdbdb.BaseDB.parse_schema', return_value=self.mock_schema):
            with patch('datafaker.dbs.rdbdb.load_sqlalchemy', return_value=mock_session):
                db = TestDB(self.mock_args)
                
                # 测试数据
                lines = [[1, 'test'], [2, 'test2']]
                names_format = "(%s,'%s')"
                column_names = 'id,name'
                
                # 执行方法
                db.save_oracle(lines, names_format, column_names)
                
                # 验证 session.execute 被调用两次（每条数据一次）
                expected_sql1 = "insert into test_table (id,name) values (1,'test')"
                expected_sql2 = "insert into test_table (id,name) values (2,'test2')"
                expected_calls = [
                    unittest.mock.call(expected_sql1),
                    unittest.mock.call(expected_sql2)
                ]
                mock_session.execute.assert_has_calls(expected_calls)
                # 验证 session.commit 被调用
                mock_session.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()