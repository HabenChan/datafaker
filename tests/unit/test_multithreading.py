#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
import time
from datafaker.multithreading import StoppableThread, Process, Lock, Value, List, Dict


class TestMultithreading(unittest.TestCase):
    """测试 multithreading.py 文件"""

    def test_stoppable_thread(self):
        """测试 StoppableThread 类"""
        # 创建一个测试线程
        class TestThread(StoppableThread):
            def run(self):
                try:
                    while not self.stopped():
                        time.sleep(0.1)
                except KeyboardInterrupt:
                    pass
        
        # 测试线程的创建和终止
        thread = TestThread()
        thread.start()
        time.sleep(0.1)
        thread.terminate()
        thread.join()
        
        # 验证线程已停止
        self.assertTrue(thread.stopped())

    def test_process(self):
        """测试 Process 类"""
        # 验证 Process 是 StoppableThread 的别名
        self.assertEqual(Process, StoppableThread)

    def test_lock(self):
        """测试 Lock 类"""
        # 创建一个锁
        lock = Lock()
        
        # 测试锁的获取和释放
        lock.acquire()
        self.assertTrue(lock.locked())
        lock.release()
        self.assertFalse(lock.locked())

    def test_value(self):
        """测试 Value 类"""
        # 测试不同类型的值
        int_value = Value('i', 10)
        self.assertEqual(int_value.value, 10)
        
        float_value = Value('f', 3.14)
        self.assertAlmostEqual(float_value.value, 3.14, places=5)

    def test_list(self):
        """测试 List 类"""
        # 验证 List 是 list 的别名
        self.assertEqual(List, list)
        
        # 测试 List 的功能
        test_list = List([1, 2, 3])
        self.assertEqual(test_list, [1, 2, 3])

    def test_dict(self):
        """测试 Dict 类"""
        # 验证 Dict 是 dict 的别名
        self.assertEqual(Dict, dict)
        
        # 测试 Dict 的功能
        test_dict = Dict({'a': 1, 'b': 2})
        self.assertEqual(test_dict, {'a': 1, 'b': 2})


if __name__ == '__main__':
    unittest.main()