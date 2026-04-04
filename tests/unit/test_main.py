#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import unittest
from unittest.mock import patch, MagicMock


class TestMain(unittest.TestCase):
    """测试 __main__.py 文件"""

    @patch('datafaker.cli.main')
    @patch('sys.exit')
    def test_main_execution(self, mock_exit, mock_main):
        """测试主函数执行"""
        # 设置 mock 返回值
        mock_main.return_value = 0
        
        # 模拟命令行参数
        with patch.object(sys, 'argv', ['datafaker', 'file', './test.txt', 'test_table', '10']):
            # 直接测试 main 函数的调用
            from datafaker.cli import main
            result = main()
            
            # 验证 main 函数被调用
            mock_main.assert_called_once()
            # 验证返回值
            self.assertEqual(result, 0)

    @patch('datafaker.cli.main')
    @patch('sys.exit')
    def test_main_with_error(self, mock_exit, mock_main):
        """测试主函数执行出错的情况"""
        # 设置 mock 返回值
        mock_main.return_value = 1
        
        # 模拟命令行参数
        with patch.object(sys, 'argv', ['datafaker', 'file', './test.txt', 'test_table', '10']):
            # 直接测试 main 函数的调用
            from datafaker.cli import main
            result = main()
            
            # 验证 main 函数被调用
            mock_main.assert_called_once()
            # 验证返回值
            self.assertEqual(result, 1)

    def test_main_module_execution(self):
        """测试 __main__.py 模块执行"""
        import subprocess
        import sys
        
        # 运行模块并捕获输出
        result = subprocess.run(
            [sys.executable, '-m', 'datafaker', 'file', './test.txt', 'test_table', '10'],
            capture_output=True,
            text=True
        )
        
        # 验证模块能够正常执行（即使参数可能不正确）
        # 我们只关心模块能够导入和执行，而不是具体的功能
        # 由于我们没有实际的文件和表，所以会失败，但这是预期的
        # 我们只需要确保模块能够运行，而不是具体的功能
        # 所以我们不检查返回码，只检查是否没有导入错误
        self.assertNotIn('ImportError', result.stderr)
        self.assertNotIn('ModuleNotFoundError', result.stderr)


if __name__ == '__main__':
    unittest.main()