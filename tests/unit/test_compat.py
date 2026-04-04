#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import unittest
from unittest.mock import patch, MagicMock
import os

from datafaker.compat import (
    ensure_text_type, safe_encode, safe_encode_file, safe_decode,
    compat_input, compat_shell_quote, _windows_shell_quote,
    get_popen_kwargs_for_pager_cmd, NonTranslatedStdout,
    StdinMissingError, get_binary_stdin, get_binary_stdout,
    get_stdout_text_writer, get_stderr_text_writer, compat_open,
    bytes_print
)


class TestCompat(unittest.TestCase):
    """测试 compat.py 文件"""

    def test_ensure_text_type(self):
        """测试 ensure_text_type 函数"""
        # 测试字符串类型
        self.assertEqual(ensure_text_type("test"), "test")
        
        # 测试字节类型
        if sys.version_info[0] == 2:
            self.assertEqual(ensure_text_type(b"test"), u"test")
        else:
            self.assertEqual(ensure_text_type(b"test"), "test")
        
        # 测试其他类型
        with self.assertRaises(ValueError):
            ensure_text_type(123)

    def test_safe_encode(self):
        """测试 safe_encode 函数"""
        # 测试字符串类型
        result = safe_encode("test")
        self.assertIsNotNone(result)
        
        # 测试非字符串类型
        self.assertEqual(safe_encode(123), 123)

    def test_safe_encode_file(self):
        """测试 safe_encode_file 函数"""
        # 测试字符串类型
        result = safe_encode_file("test")
        self.assertIsNotNone(result)
        
        # 测试非字符串类型
        self.assertEqual(safe_encode_file(123), 123)

    def test_safe_decode(self):
        """测试 safe_decode 函数"""
        # 测试字符串类型
        result = safe_decode("test")
        self.assertIsNotNone(result)
        
        # 测试非字符串类型
        self.assertEqual(safe_decode(123), 123)

    @patch('builtins.input', return_value='test input')
    @patch('sys.stdout.write')
    @patch('sys.stdout.flush')
    def test_compat_input(self, mock_flush, mock_write, mock_input):
        """测试 compat_input 函数"""
        result = compat_input('Prompt: ')
        mock_write.assert_called_with('Prompt: ')
        mock_flush.assert_called_once()
        mock_input.assert_called_once()
        self.assertEqual(result, 'test input')

    def test_compat_shell_quote(self):
        """测试 compat_shell_quote 函数"""
        # 测试普通字符串
        self.assertEqual(compat_shell_quote('test'), 'test')
        
        # 测试带空格的字符串
        if sys.platform == 'win32':
            self.assertEqual(compat_shell_quote('test string'), '"test string"')
        else:
            self.assertEqual(compat_shell_quote('test string'), "'test string'")

    def test_windows_shell_quote(self):
        """测试 _windows_shell_quote 函数"""
        # 测试空字符串
        self.assertEqual(_windows_shell_quote(''), '""')
        
        # 测试普通字符串
        self.assertEqual(_windows_shell_quote('test'), 'test')
        
        # 测试带空格的字符串
        self.assertEqual(_windows_shell_quote('test string'), '"test string"')
        
        # 测试带引号的字符串
        self.assertEqual(_windows_shell_quote('test"string'), 'test\\"string')
        
        # 测试带反斜杠的字符串
        self.assertEqual(_windows_shell_quote('test\\string'), 'test\\string')

    def test_get_popen_kwargs_for_pager_cmd(self):
        """测试 get_popen_kwargs_for_pager_cmd 函数"""
        kwargs = get_popen_kwargs_for_pager_cmd()
        self.assertIn('args', kwargs)
        
        if sys.platform == 'win32':
            self.assertEqual(kwargs['shell'], True)
        else:
            self.assertNotIn('shell', kwargs)

    def test_non_translated_stdout(self):
        """测试 NonTranslatedStdout 上下文管理器"""
        with NonTranslatedStdout():
            # 测试上下文管理器不会抛出异常
            pass

    @patch('sys.stdin', None)
    def test_get_binary_stdin_with_none(self):
        """测试 get_binary_stdin 函数在 stdin 为 None 时的情况"""
        with self.assertRaises(StdinMissingError):
            get_binary_stdin()

    def test_get_binary_stdout(self):
        """测试 get_binary_stdout 函数"""
        result = get_binary_stdout()
        self.assertIsNotNone(result)

    def test_get_stdout_text_writer(self):
        """测试 get_stdout_text_writer 函数"""
        result = get_stdout_text_writer()
        self.assertIsNotNone(result)

    def test_get_stderr_text_writer(self):
        """测试 get_stderr_text_writer 函数"""
        result = get_stderr_text_writer()
        self.assertIsNotNone(result)

    def test_compat_open(self):
        """测试 compat_open 函数"""
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('test content')
            temp_file = f.name
        
        try:
            # 测试读取文件
            with compat_open(temp_file, 'r') as f:
                content = f.read()
                self.assertEqual(content, 'test content')
        finally:
            os.unlink(temp_file)

    def test_bytes_print(self):
        """测试 bytes_print 函数"""
        # 测试默认 stdout
        with patch('sys.stdout.buffer.write') as mock_write:
            bytes_print(b'test')
            mock_write.assert_called_once_with(b'test')
        
        # 测试自定义 stdout
        mock_stdout = MagicMock()
        mock_stdout.buffer.write = MagicMock()
        bytes_print(b'test', stdout=mock_stdout)
        mock_stdout.buffer.write.assert_called_once_with(b'test')


if __name__ == '__main__':
    unittest.main()