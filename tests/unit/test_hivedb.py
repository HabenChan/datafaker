#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from unittest.mock import patch, MagicMock

from datafaker.dbs.hivedb import HiveDB


class TestHiveDB(unittest.TestCase):
    """测试 HiveDB 类"""

    def setUp(self):
        """设置测试环境"""
        # 创建一个模拟的 args 对象
        self.args = MagicMock()
        self.args.connect = 'hive://localhost:10000/default'
        self.args.table = 'test_table'
        self.args.locale = 'en_US'
        self.args.metaj = None

    @patch('datafaker.dbs.rdbdb.load_sqlalchemy')
    @patch('datafaker.dbs.hivedb.load_sqlalchemy')
    def test_construct_self_rows(self, mock_load_sqlalchemy_hive, mock_load_sqlalchemy_rdb):
        """测试 construct_self_rows 方法"""
        # 模拟 session 和 execute 方法
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.__iter__.return_value = [('id', 'int'), ('name', 'string'), ('age', 'int')]
        mock_session.execute.return_value = mock_result
        mock_load_sqlalchemy_hive.return_value = mock_session
        mock_load_sqlalchemy_rdb.return_value = mock_session
        
        # 创建 HiveDB 实例
        with patch('datafaker.dbs.rdbdb.load_sqlalchemy', return_value=mock_session):
            self.hivedb = HiveDB(self.args)
        
        # 执行方法
        rows = self.hivedb.construct_self_rows()
        
        # 验证 load_sqlalchemy 被正确调用
        mock_load_sqlalchemy_hive.assert_called_once_with('hive://localhost:10000/default')
        # 验证 execute 被正确调用
        mock_session.execute.assert_called_once_with('desc test_table')
        # 验证返回值
        expected_rows = [('id', 'int'), ('name', 'string'), ('age', 'int')]
        self.assertEqual(rows, expected_rows)


if __name__ == '__main__':
    unittest.main()