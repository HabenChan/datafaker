#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import unittest
from unittest.mock import patch, MagicMock

from datafaker.cli import parse_args, load_db_class, main
from datafaker.exceptions import ParamError


class TestCLI(unittest.TestCase):
    """测试 cli.py 文件"""

    def test_parse_args_with_all_params(self):
        """测试解析所有参数"""
        with patch.object(sys, 'argv', ['datafaker', 'file', './test.txt', 'test_table', '10']):
            args = parse_args()
            self.assertEqual(args.dbtype, 'file')
            self.assertEqual(args.connect, './test.txt')
            self.assertEqual(args.table, 'test_table')
            self.assertEqual(args.num, 10)

    def test_parse_args_with_missing_dbtype(self):
        """测试缺少 dbtype 参数"""
        with patch.object(sys, 'argv', ['datafaker']):
            with self.assertRaises(SystemExit):
                parse_args()

    def test_parse_args_with_missing_connect(self):
        """测试缺少 connect 参数"""
        with patch.object(sys, 'argv', ['datafaker', 'file']):
            with self.assertRaises(SystemExit):
                parse_args()

    def test_parse_args_with_missing_table(self):
        """测试缺少 table 参数"""
        with patch.object(sys, 'argv', ['datafaker', 'file', './test.txt']):
            with self.assertRaises(SystemExit):
                parse_args()

    def test_parse_args_with_missing_num(self):
        """测试缺少 num 参数"""
        with patch.object(sys, 'argv', ['datafaker', 'file', './test.txt', 'test_table']):
            with patch('builtins.print') as mock_print:
                with patch('argparse.ArgumentParser.print_help') as mock_print_help:
                    try:
                        parse_args()
                    except SystemExit:
                        pass
                    mock_print.assert_called_with('You must supply number of records\n')
                    mock_print_help.assert_called_once()

    def test_parse_args_with_json_format_error(self):
        """测试 JSON 格式错误"""
        with patch.object(sys, 'argv', ['datafaker', 'mysql', 'localhost:3306/test', 'test_table', '10', '--format', 'json']):
            with self.assertRaises(ParamError):
                parse_args()

    def test_parse_args_with_metaj_error(self):
        """测试 metaj 错误"""
        with patch.object(sys, 'argv', ['datafaker', 'mysql', 'localhost:3306/test', 'test_table', '10', '--metaj', 'meta.json']):
            with self.assertRaises(ParamError):
                parse_args()

    def test_load_db_class(self):
        """测试加载数据库类"""
        # 测试加载 file 数据库类
        file_db_class = load_db_class('file')
        self.assertIsNotNone(file_db_class)
        
        # 测试加载 mysql 数据库类
        mysql_db_class = load_db_class('mysql')
        self.assertIsNotNone(mysql_db_class)

    @patch('datafaker.cli.parse_args')
    @patch('datafaker.cli.load_db_class')
    @patch('sys.exit')
    def test_main_successful(self, mock_exit, mock_load_db_class, mock_parse_args):
        """测试 main 函数成功执行"""
        # 设置 mock
        mock_args = MagicMock()
        mock_args.dbtype = 'file'
        mock_parse_args.return_value = mock_args
        
        mock_db_instance = MagicMock()
        mock_db_class = MagicMock(return_value=mock_db_instance)
        mock_load_db_class.return_value = mock_db_class
        
        # 执行 main 函数
        main()
        
        # 验证调用
        mock_parse_args.assert_called_once()
        mock_load_db_class.assert_called_once_with('file')
        mock_db_class.assert_called_once_with(mock_args)
        mock_db_instance.do_fake.assert_called_once()
        mock_exit.assert_not_called()

    @patch('datafaker.cli.parse_args')
    @patch('sys.exit')
    def test_main_with_param_error(self, mock_exit, mock_parse_args):
        """测试 main 函数参数错误"""
        # 设置 mock 抛出 ParamError
        mock_parse_args.side_effect = ParamError('Test param error')
        
        # 执行 main 函数
        main()
        
        # 验证调用
        mock_parse_args.assert_called_once()
        mock_exit.assert_called_once_with(1)

    @patch('datafaker.cli.parse_args')
    @patch('sys.exit')
    def test_main_with_general_error(self, mock_exit, mock_parse_args):
        """测试 main 函数一般错误"""
        # 设置 mock 抛出一般异常
        mock_parse_args.side_effect = Exception('Test general error')
        
        # 执行 main 函数
        main()
        
        # 验证调用
        mock_parse_args.assert_called_once()
        mock_exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()