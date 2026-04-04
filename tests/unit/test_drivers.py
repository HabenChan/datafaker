#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from unittest.mock import patch, MagicMock

from datafaker.drivers import load_sqlalchemy, load_conn


class TestDrivers(unittest.TestCase):
    """测试 drivers.py 文件"""

    @patch('datafaker.drivers.create_engine')
    @patch('datafaker.drivers.sessionmaker')
    def test_load_sqlalchemy(self, mock_sessionmaker, mock_create_engine):
        """测试 load_sqlalchemy 函数"""
        # 设置 mock
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        
        mock_dbsession = MagicMock()
        mock_sessionmaker.return_value = mock_dbsession
        
        mock_session = MagicMock()
        mock_dbsession.return_value = mock_session
        
        # 执行函数
        result = load_sqlalchemy('sqlite:///:memory:')
        
        # 验证调用
        mock_create_engine.assert_called_once_with('sqlite:///:memory:', pool_recycle=1800)
        mock_sessionmaker.assert_called_once_with(mock_engine)
        mock_dbsession.assert_called_once()
        self.assertEqual(result, mock_session)

    @patch('datafaker.drivers.create_engine')
    def test_load_conn(self, mock_create_engine):
        """测试 load_conn 函数"""
        # 设置 mock
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        
        mock_connection = MagicMock()
        mock_engine.connect.return_value = mock_connection
        
        # 执行函数
        result = load_conn('sqlite:///:memory:')
        
        # 验证调用
        mock_create_engine.assert_called_once_with('sqlite:///:memory:', pool_recycle=1800)
        mock_engine.connect.assert_called_once()
        self.assertEqual(result, mock_connection)


if __name__ == '__main__':
    unittest.main()