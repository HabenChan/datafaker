#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock

from datafaker.dbs.filedb import FileDB


class TestFileDB(unittest.TestCase):
    """测试 FileDB 类"""

    def setUp(self):
        """设置测试环境"""
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()
        
        # 创建模拟参数
        self.mock_args = MagicMock()
        self.mock_args.connect = self.temp_dir
        self.mock_args.table = 'test.txt'
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
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=[
            {'name': 'id', 'type': 'int', 'comment': '[:inc]', 'cmd': 'inc', 'args': []},
            {'name': 'name', 'type': 'varchar', 'comment': '[:name]', 'cmd': 'name', 'args': []}
        ]):
            self.file_db = FileDB(self.mock_args)

    def tearDown(self):
        """清理测试环境"""
        # 删除临时文件
        test_file = os.path.join(self.temp_dir, 'test.txt')
        if os.path.exists(test_file):
            os.unlink(test_file)
        # 删除临时目录
        os.rmdir(self.temp_dir)

    def test_construct_self_rows(self):
        """测试 construct_self_rows 方法"""
        result = self.file_db.construct_self_rows()
        self.assertEqual(result, [])

    def test_format_data(self):
        """测试 format_data 方法"""
        # 测试默认格式
        result1 = self.file_db.format_data([1, 'test'])
        self.assertEqual(result1, '1,test')
        
        # 测试 JSON 格式
        self.mock_args.format = 'json'
        self.file_db.column_names = ['id', 'name']
        result2 = self.file_db.format_data([1, 'test'])
        self.assertIn('"id": 1', result2)
        self.assertIn('"name": "test"', result2)

    @patch('datafaker.dbs.filedb.save2file')
    def test_save_data(self, mock_save2file):
        """测试 save_data 方法"""
        # 测试保存数据
        test_data = [[1, 'test1'], [2, 'test2']]
        self.file_db.save_data(test_data)
        
        # 验证 save2file 被调用
        mock_save2file.assert_called_once()

    @patch('datafaker.dbs.basedb.BaseDB.fake_data')
    @patch('datafaker.dbs.basedb.BaseDB.save')
    def test_do_fake(self, mock_save, mock_fake_data):
        """测试 do_fake 方法"""
        # 执行 do_fake 方法
        self.file_db.do_fake()
        
        # 验证方法被调用
        mock_fake_data.assert_called()
        mock_save.assert_called()


if __name__ == '__main__':
    unittest.main()