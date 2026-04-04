#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from unittest.mock import patch, MagicMock

from datafaker.dbs.postgresqldb import PostgresqlDB


class TestPostgresqlDB(unittest.TestCase):
    """测试 PostgresqlDB 类"""

    def setUp(self):
        """设置测试环境"""
        # 创建一个模拟的 args 对象
        self.args = MagicMock()
        self.args.connect = 'postgresql://localhost:5432/test_db'
        self.args.table = 'test_table'
        self.args.locale = 'en_US'
        self.args.metaj = None

    @patch('datafaker.dbs.postgresqldb.load_sqlalchemy')
    @patch('datafaker.dbs.rdbdb.load_sqlalchemy')
    def test_construct_self_rows(self, mock_load_sqlalchemy_rdb, mock_load_sqlalchemy_postgres):
        """测试 construct_self_rows 方法（普通表名）"""
        # 模拟 session 和 execute 方法
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.__iter__.return_value = [('id', 'integer'), ('name', 'character varying'), ('age', 'integer')]
        mock_session.execute.return_value = mock_result
        mock_load_sqlalchemy_postgres.return_value = mock_session
        mock_load_sqlalchemy_rdb.return_value = mock_session
        
        # 创建 PostgresqlDB 实例
        with patch('datafaker.dbs.rdbdb.load_sqlalchemy', return_value=mock_session):
            self.postgresqldb = PostgresqlDB(self.args)
        
        # 执行方法
        rows = self.postgresqldb.construct_self_rows()
        
        # 验证 load_sqlalchemy 被正确调用
        mock_load_sqlalchemy_postgres.assert_called_once_with('postgresql://localhost:5432/test_db')
        # 验证 execute 被正确调用，使用普通表名的 SQL
        expected_sql = '''SELECT 
    a.attname AS "字段名",
    pg_catalog.format_type(a.atttypid, a.atttypmod) AS "数据类型",
    col_description(a.attrelid, a.attnum) AS "字段注释"
FROM 
    pg_catalog.pg_attribute a
WHERE 
    a.attrelid = 'test_table'::regclass  -- 替换为你的表名
    AND a.attnum > 0  -- 排除系统列
    AND NOT a.attisdropped;  -- 排除已删除的列'''
        mock_session.execute.assert_called_once_with(expected_sql)
        # 验证返回值
        expected_rows = [('id', 'integer'), ('name', 'character varying'), ('age', 'integer')]
        self.assertEqual(list(rows), expected_rows)

    @patch('datafaker.dbs.postgresqldb.load_sqlalchemy')
    @patch('datafaker.dbs.rdbdb.load_sqlalchemy')
    def test_construct_self_rows_with_schema(self, mock_load_sqlalchemy_rdb, mock_load_sqlalchemy_postgres):
        """测试 construct_self_rows 方法（带 schema 的表名）"""
        # 模拟 session 和 execute 方法
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.__iter__.return_value = [('id', 'integer'), ('name', 'character varying'), ('age', 'integer')]
        mock_session.execute.return_value = mock_result
        mock_load_sqlalchemy_postgres.return_value = mock_session
        mock_load_sqlalchemy_rdb.return_value = mock_session
        
        # 设置带 schema 的表名
        self.args.table = 'public.test_table'
        
        # 创建 PostgresqlDB 实例
        with patch('datafaker.dbs.rdbdb.load_sqlalchemy', return_value=mock_session):
            self.postgresqldb = PostgresqlDB(self.args)
        
        # 执行方法
        rows = self.postgresqldb.construct_self_rows()
        
        # 验证 load_sqlalchemy 被正确调用
        mock_load_sqlalchemy_postgres.assert_called_once_with('postgresql://localhost:5432/test_db')
        # 验证 execute 被正确调用，使用带 schema 的表名的 SQL
        expected_sql = '''SELECT 
    a.attname AS "字段名",
    pg_catalog.format_type(a.atttypid, a.atttypmod) AS "数据类型",
    col_description(a.attrelid, a.attnum) AS "字段注释"
FROM 
    pg_catalog.pg_attribute a
WHERE 
    a.attrelid = ('public.test_table')::regclass  -- 替换为你的表名
    AND a.attnum > 0  -- 排除系统列
    AND NOT a.attisdropped;  -- 排除已删除的列'''
        mock_session.execute.assert_called_once_with(expected_sql)
        # 验证返回值
        expected_rows = [('id', 'integer'), ('name', 'character varying'), ('age', 'integer')]
        self.assertEqual(list(rows), expected_rows)


if __name__ == '__main__':
    unittest.main()