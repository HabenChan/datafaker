#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
import queue

from datafaker.dbs.basedb import BaseDB
from datafaker.exceptions import ParseSchemaError


class TestBaseDB(unittest.TestCase):
    """测试 BaseDB 类"""

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
        self.mock_schema = [
            {'name': 'id', 'type': 'int', 'comment': '[:inc]', 'cmd': 'inc', 'args': []},
            {'name': 'name', 'type': 'varchar', 'comment': '[:name]', 'cmd': 'name', 'args': []}
        ]

    def tearDown(self):
        """清理测试环境"""
        # 删除临时目录
        os.rmdir(self.temp_dir)

    def test_init(self):
        """测试初始化方法"""
        # 创建一个 BaseDB 子类实例
        class TestDB(BaseDB):
            def construct_self_rows(self):
                return []
            def save_data(self, lines):
                pass
        
        # 模拟 parse_schema 方法
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
            db = TestDB(self.mock_args)
            self.assertEqual(db.args, self.mock_args)
            self.assertEqual(db.schema, self.mock_schema)
            self.assertEqual(db.column_names, ['id', 'name'])

    def test_get_cur_num(self):
        """测试 get_cur_num 方法"""
        # 创建一个 BaseDB 子类实例
        class TestDB(BaseDB):
            def construct_self_rows(self):
                return []
            def save_data(self, lines):
                pass
        
        # 模拟 parse_schema 方法
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
            db = TestDB(self.mock_args)
            # 测试自增功能
            result1 = db.get_cur_num()
            self.assertEqual(result1, 0)
            result2 = db.get_cur_num()
            self.assertEqual(result2, 1)

    def test_format_data(self):
        """测试 format_data 方法"""
        # 创建一个 BaseDB 子类实例
        class TestDB(BaseDB):
            def construct_self_rows(self):
                return []
            def save_data(self, lines):
                pass
        
        # 模拟 parse_schema 方法
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
            db = TestDB(self.mock_args)
            # 测试默认格式
            result1 = db.format_data([1, 'test'])
            self.assertEqual(result1, [1, 'test'])
            
            # 测试 JSON 格式
            self.mock_args.format = 'json'
            result2 = db.format_data([1, 'test'])
            self.assertIn('"id": 1', result2)
            self.assertIn('"name": "test"', result2)

    def test_fake_column(self):
        """测试 fake_column 方法"""
        # 创建一个 BaseDB 子类实例
        class TestDB(BaseDB):
            def construct_self_rows(self):
                return []
            def save_data(self, lines):
                pass
        
        # 模拟 parse_schema 方法和 fakedata.do_fake 方法
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
            with patch('datafaker.fakedata.FackData.do_fake', side_effect=[1, 'test']):
                db = TestDB(self.mock_args)
                result = db.fake_column(1)
                self.assertEqual(result, [1, 'test'])

    def test_construct_meta_rows(self):
        """测试 construct_meta_rows 方法"""
        # 创建一个 BaseDB 子类实例
        class TestDB(BaseDB):
            def construct_self_rows(self):
                return []
            def save_data(self, lines):
                pass
        
        # 创建临时 meta 文件
        meta_content = "id||int||[:inc]\nname||varchar||[:name]"
        meta_file = os.path.join(self.temp_dir, 'meta.txt')
        with open(meta_file, 'w') as f:
            f.write(meta_content)
        
        # 模拟 parse_schema 方法
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
            db = TestDB(self.mock_args)
            # 测试 construct_meta_rows 方法
            self.mock_args.meta = meta_file
            rows = db.construct_meta_rows()
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0], ['id', 'int', '[:inc]'])
            self.assertEqual(rows[1], ['name', 'varchar', '[:name]'])

        # 删除临时文件
        os.unlink(meta_file)

    def test_parse_schema(self):
        """测试 parse_schema 方法"""
        # 创建一个 BaseDB 子类实例
        class TestDB(BaseDB):
            def construct_self_rows(self):
                return []
            def save_data(self, lines):
                pass
        
        # 模拟 parse_schema_from_rows 方法
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
            db = TestDB(self.mock_args)
            schema = db.parse_schema()
            self.assertEqual(schema, self.mock_schema)

    def test_parse_self_schema(self):
        """测试 parse_self_schema 方法"""
        # 创建一个 BaseDB 子类实例
        class TestDB(BaseDB):
            def construct_self_rows(self):
                return [['id', 'int', '[:inc]'], ['name', 'varchar', '[:name]']]
            def save_data(self, lines):
                pass
        
        # 模拟 parse_schema_from_rows 方法
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema_from_rows', return_value=self.mock_schema):
            with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
                db = TestDB(self.mock_args)
                schema = db.parse_self_schema()
                self.assertEqual(schema, self.mock_schema)

    def test_parse_meta_schema(self):
        """测试 parse_meta_schema 方法"""
        # 创建一个 BaseDB 子类实例
        class TestDB(BaseDB):
            def construct_self_rows(self):
                return []
            def save_data(self, lines):
                pass
        
        # 模拟 construct_meta_rows 方法和 parse_schema_from_rows 方法
        with patch('datafaker.dbs.basedb.BaseDB.construct_meta_rows', return_value=[['id', 'int', '[:inc]'], ['name', 'varchar', '[:name]']]):
            with patch('datafaker.dbs.basedb.BaseDB.parse_schema_from_rows', return_value=self.mock_schema):
                with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
                    db = TestDB(self.mock_args)
                    schema = db.parse_meta_schema()
                    self.assertEqual(schema, self.mock_schema)

    def test_parse_metaj_schema(self):
        """测试 parse_metaj_schema 方法"""
        # 创建一个 BaseDB 子类实例
        class TestDB(BaseDB):
            def construct_self_rows(self):
                return []
            def save_data(self, lines):
                pass
        
        # 创建临时 metaj 文件
        metaj_content = '{"id": "[:inc]", "name": "[:name]"}'
        metaj_file = os.path.join(self.temp_dir, 'metaj.json')
        with open(metaj_file, 'w') as f:
            f.write(metaj_content)
        
        # 模拟 parse_schema_from_text 方法
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema_from_text', return_value=self.mock_schema):
            with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
                db = TestDB(self.mock_args)
                self.mock_args.metaj = metaj_file
                schema = db.parse_metaj_schema()
                self.assertEqual(schema, self.mock_schema)

        # 删除临时文件
        os.unlink(metaj_file)

    def test_parse_schema_from_rows(self):
        """测试 parse_schema_from_rows 方法"""
        # 创建一个 BaseDB 子类实例
        class TestDB(BaseDB):
            def construct_self_rows(self):
                return []
            def save_data(self, lines):
                pass
        
        # 模拟 parse_schema 方法
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
            db = TestDB(self.mock_args)
            # 测试正常情况
            rows = [['id', 'int', '[:inc]'], ['name', 'varchar', '[:name]']]
            schema = db.parse_schema_from_rows(rows)
            self.assertEqual(len(schema), 2)
            self.assertEqual(schema[0]['name'], 'id')
            self.assertEqual(schema[1]['name'], 'name')

    def test_parse_schema_from_text(self):
        """测试 parse_schema_from_text 方法"""
        # 创建一个 BaseDB 子类实例
        class TestDB(BaseDB):
            def construct_self_rows(self):
                return []
            def save_data(self, lines):
                pass
        
        # 模拟 parse_schema 方法
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
            db = TestDB(self.mock_args)
            # 测试正常情况
            text = '{"id": "[:inc]", "name": "[:name]"}'
            schema = db.parse_schema_from_text(text)
            self.assertEqual(len(schema), 2)

    def test_print_data(self):
        """测试 print_data 方法"""
        # 创建一个 BaseDB 子类实例
        class TestDB(BaseDB):
            def construct_self_rows(self):
                return []
            def save_data(self, lines):
                pass
        
        # 模拟 parse_schema 方法和 queue.get_nowait 方法
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
            with patch('datafaker.compat.Queue.get_nowait', side_effect=[[1, 'test'], queue.Empty]):
                db = TestDB(self.mock_args)
                db.isover.value = True
                # 执行 print_data 方法，捕获输出
                with patch('builtins.print') as mock_print:
                    db.print_data()
                    # 验证 print 被调用
                    mock_print.assert_called()

    def test_fake_data(self):
        """测试 fake_data 方法"""
        # 创建一个 BaseDB 子类实例
        class TestDB(BaseDB):
            def construct_self_rows(self):
                return []
            def save_data(self, lines):
                pass
        
        # 模拟 parse_schema 方法、fake_column 方法和 get_cur_num 方法
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
            with patch('datafaker.dbs.basedb.BaseDB.fake_column', return_value=[1, 'test']):
                with patch('datafaker.dbs.basedb.BaseDB.get_cur_num', side_effect=[0, 1]):
                    db = TestDB(self.mock_args)
                    # 设置 num 为 1，只生成一条数据
                    db.args.num = 1
                    # 执行 fake_data 方法
                    db.fake_data()
                    # 验证 isover 被设置为 True
                    self.assertTrue(db.isover.value)

    def test_do_fake(self):
        """测试 do_fake 方法"""
        # 创建一个 BaseDB 子类实例
        class TestDB(BaseDB):
            def construct_self_rows(self):
                return []
            def save_data(self, lines):
                pass
        
        # 模拟 parse_schema 方法和 compat.Process
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
            with patch('datafaker.compat.Process') as mock_process:
                db = TestDB(self.mock_args)
                # 设置 num 为 1，使用单线程
                db.args.num = 1
                # 执行 do_fake 方法
                db.do_fake()
                # 验证 Process 被调用
                self.assertTrue(mock_process.called)

    def test_save_data(self):
        """测试 save_data 方法"""
        # 创建一个 BaseDB 子类实例
        class TestDB(BaseDB):
            def construct_self_rows(self):
                return []
        
        # 模拟 parse_schema 方法和 save_data 方法
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
            with patch('datafaker.dbs.basedb.BaseDB.save_data') as mock_save_data:
                db = TestDB(self.mock_args)
                # 测试数据
                lines = [[1, 'test'], [2, 'test2']]
                # 执行 save_data 方法
                db.save_data(lines)
                # 验证 save_data 被调用
                mock_save_data.assert_called_once_with(lines)

    def test_parse_schema_from_rows_with_duplicate_columns(self):
        """测试 parse_schema_from_rows 方法（重复列名）"""
        # 创建一个 BaseDB 子类实例
        class TestDB(BaseDB):
            def construct_self_rows(self):
                return []
            def save_data(self, lines):
                pass
        
        # 模拟 parse_schema 方法
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
            db = TestDB(self.mock_args)
            # 测试重复列名的情况
            rows = [['id', 'int', '[:inc]'], ['id', 'varchar', '[:name]']]
            with self.assertRaises(ParseSchemaError):
                db.parse_schema_from_rows(rows)

    def test_parse_schema_from_text_with_enum(self):
        """测试 parse_schema_from_text 方法（枚举类型）"""
        # 创建一个 BaseDB 子类实例
        class TestDB(BaseDB):
            def construct_self_rows(self):
                return []
            def save_data(self, lines):
                pass
        
        # 模拟 parse_schema 方法
        with patch('datafaker.dbs.basedb.BaseDB.parse_schema', return_value=self.mock_schema):
            db = TestDB(self.mock_args)
            # 测试枚举类型
            text = '{"status": "[:enum(active,inactive,pending)]"}'
            schema = db.parse_schema_from_text(text)
            self.assertEqual(len(schema), 1)
            self.assertEqual(schema[0]['cmd'], 'enum')


if __name__ == '__main__':
    unittest.main()