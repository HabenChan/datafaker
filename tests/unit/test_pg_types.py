#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from datafaker.fakedata import FackData

# 创建FackData实例
facker = FackData('zh_CN')

print("Testing PostgreSQL and custom types:")
print("=" * 50)

# 测试PostgreSQL类型
print("PostgreSQL REAL:", facker.fake_real())
print("PostgreSQL NUMERIC(8,3):", facker.fake_numeric(8, 3))
print("PostgreSQL MONEY:", facker.fake_money())
print("PostgreSQL TIMETZ:", facker.fake_timetz())
print("PostgreSQL TIMESTAMPTZ:", facker.fake_timestamptz())
print("PostgreSQL INTERVAL:", facker.fake_interval())
print("PostgreSQL BYTEA (first 20 bytes):", facker.fake_bytea(20)[:20])
print("PostgreSQL JSON:", facker.fake_json())
print("PostgreSQL JSONB (first 30 chars):", str(facker.fake_jsonb())[:30])
print("PostgreSQL INET:", facker.fake_inet())
print("PostgreSQL CIDR:", facker.fake_cidr())
print("PostgreSQL MACADDR:", facker.fake_macaddr())
print("PostgreSQL UUID:", facker.fake_uuid())
print("PostgreSQL TSVECTOR:", facker.fake_tsvector())
print("PostgreSQL XML:", facker.fake_xml())

print("\n" + "=" * 50)
print("Custom Primary Key Types:")
print("=" * 50)

# 测试自定义主键类型
print("String PK:", facker.fake_str_pk("ID", 10))
print("Hash PK:", facker.fake_hash_pk(20))
print("Random String PK:", facker.fake_random_str_pk(15))

print("\n" + "=" * 50)
print("MySQL BLOB/TEXT Types:")
print("=" * 50)

# 测试MySQL BLOB/TEXT类型
print("TINYBLOB (first 10 bytes):", facker.fake_tinyblob()[:10])
print("TINYTEXT:", facker.fake_tinytext(50))
print("MEDIUMTEXT (first 50 chars):", facker.fake_mediumtext(50)[:50])
print("LONGTEXT (first 50 chars):", facker.fake_longtext(50)[:50])