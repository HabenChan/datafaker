#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from datafaker.fakedata import FackData

# 创建FackData实例
facker = FackData('zh_CN')

# 测试fake_str_pk方法
print("Testing fake_str_pk method:")
for i in range(5):
    result = facker.fake_str_pk("PK", 10)
    print(f"  {result}")

print("\nTesting fake_hash_pk method:")
for i in range(3):
    result = facker.fake_hash_pk(16)
    print(f"  {result}")

print("\nTesting fake_random_str_pk method:")
for i in range(3):
    result = facker.fake_random_str_pk(12)
    print(f"  {result}")