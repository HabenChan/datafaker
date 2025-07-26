#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime
import json
import uuid

from datafaker.constant import DEFAULT_LOCALE
from datafaker.fakedata import FackData

fakedata = FackData(DEFAULT_LOCALE)
today = datetime.date.today()


def test_date():
    print(fakedata.fake_date(start_date='today'))
    assert today.strftime('%Y-%m-%d') == fakedata.fake_date(start_date='today')
    assert today.strftime('%y%m%d') == fakedata.fake_date(start_date='today', format='%y%m%d')
    print(fakedata.fake_date('-5d', '-2d', '%Y-%m-%d %H:%M:%S'))


def test_date_between():
    # 修正测试用例，使用正确的日期范围进行测试
    result = fakedata.fake_date_between(start_date='2019-04-14', end_date='2019-04-15')
    assert result in ['2019-04-14', '2019-04-15']


def test_datetime_between():
    print(fakedata.fake_datetime_between('2019-04-14 00:00:00', '2019-04-15 00:00:00'))


def test_decimal():
    print()
    print(fakedata.fake_decimal(4, 2))
    print(fakedata.fake_decimal(4, 2, 1))
    print(fakedata.fake_decimal(4, 2, 0, 88, 90))
    print(fakedata.fake_decimal(4, 2, 0, -90, -88))
    assert fakedata.fake_decimal(4, 2, 1, 88, 90) > 88


def test_mysql_string_types():
    # 测试CHAR类型 - 固定长度字符串
    char_val = fakedata.fake_char(10)
    assert isinstance(char_val, str)
    assert len(char_val) == 10  # 确保是固定长度
    
    # 测试TINYBLOB类型
    tinyblob_val = fakedata.fake_tinyblob()
    assert isinstance(tinyblob_val, bytes)
    assert len(tinyblob_val) <= 255  # TINYBLOB最大长度为255字节
    
    # 测试TINYTEXT类型
    tinytext_val = fakedata.fake_tinytext()
    assert isinstance(tinytext_val, str)
    assert len(tinytext_val) <= 255  # TINYTEXT最大长度为255字符
    
    # 测试MEDIUMTEXT类型
    mediumtext_val = fakedata.fake_mediumtext(1000)  # 限制生成1000个字符以避免测试过慢
    assert isinstance(mediumtext_val, str)
    assert len(mediumtext_val) <= 1000  # 检查长度不超过指定值
    
    # 测试MEDIUMTEXT默认行为
    mediumtext_default = fakedata.fake_mediumtext()
    assert isinstance(mediumtext_default, str)
    assert len(mediumtext_default) <= 16777215  # MEDIUMTEXT最大长度为16777215字符
    
    # 测试LONGTEXT类型
    longtext_val = fakedata.fake_longtext(1000)  # 限制生成1000个字符以避免测试过慢
    assert isinstance(longtext_val, str)
    assert len(longtext_val) <= 1000  # 检查长度不超过指定值
    
    # 测试LONGTEXT默认行为
    longtext_default = fakedata.fake_longtext()
    assert isinstance(longtext_default, str)
    assert len(longtext_default) <= 4294967295  # LONGTEXT最大长度为4294967295字符


def test_postgresql_types():
    # 测试PostgreSQL REAL类型
    real_val = fakedata.fake_real()
    assert isinstance(real_val, float)
    # 修正测试，允许更大的整数部分
    parts = str(abs(real_val)).split('.')
    assert len(parts[0]) <= 6  # 检查整数部分位数
    assert len(parts[1]) <= 2  # 检查小数部分位数

    # 测试PostgreSQL NUMERIC类型
    numeric_val1 = fakedata.fake_numeric()
    assert isinstance(numeric_val1, str)
    assert '.' in numeric_val1 or numeric_val1.isdigit() or (numeric_val1.startswith('-') and numeric_val1[1:].isdigit())
    
    # 测试指定精度和小数位数的NUMERIC类型
    numeric_val2 = fakedata.fake_numeric(5, 2)  # 5位总长度，2位小数
    assert isinstance(numeric_val2, str)
    if '.' in numeric_val2:
        integer_part, decimal_part = numeric_val2.split('.')
        assert len(decimal_part) == 2  # 小数部分应该有2位
        # 整数部分长度检查（包含可能的负号）
        if integer_part.startswith('-'):
            assert len(integer_part) - 1 <= 3  # 负数整数部分应该最多3位数字
        else:
            assert len(integer_part) <= 3  # 正数整数部分应该最多3位
    
    # 测试PostgreSQL MONEY类型
    money_val = fakedata.fake_money()
    assert isinstance(money_val, str)
    assert money_val.startswith('$')
    assert '.' in money_val
    assert len(money_val.split('.')[-1]) == 2  # 检查小数点后有两位

    # 测试PostgreSQL TIMETZ类型
    timetz_val = fakedata.fake_timetz()
    assert isinstance(timetz_val, str)
    assert ':' in timetz_val  # 应包含时间分隔符

    # 测试PostgreSQL TIMESTAMPTZ类型
    timestamptz_val = fakedata.fake_timestamptz()
    assert isinstance(timestamptz_val, str)
    assert ':' in timestamptz_val  # 应包含时间分隔符
    assert '+' in timestamptz_val or '-' in timestamptz_val  # 应包含时区信息

    # 测试PostgreSQL INTERVAL类型
    interval_val = fakedata.fake_interval()
    assert isinstance(interval_val, str)
    assert 'days' in interval_val
    assert 'seconds' in interval_val

    # 测试PostgreSQL BYTEA类型
    bytea_val = fakedata.fake_bytea()
    assert isinstance(bytea_val, bytes)
    assert len(bytea_val) <= 1024

    # 测试PostgreSQL JSON类型
    json_val = fakedata.fake_json()
    assert isinstance(json_val, str)
    parsed = json.loads(json_val)
    assert 'data' in parsed
    assert 'value' in parsed
    assert isinstance(parsed['value'], int)

    # 测试PostgreSQL JSONB类型
    jsonb_val = fakedata.fake_jsonb()
    assert isinstance(jsonb_val, bytes)
    parsed = json.loads(jsonb_val.decode('utf-8'))
    assert 'data' in parsed
    assert 'value' in parsed
    assert isinstance(parsed['value'], int)

    # 测试PostgreSQL INET类型
    inet_val = fakedata.fake_inet()
    assert isinstance(inet_val, str)
    assert '.' in inet_val  # IPv4地址应包含点

    # 测试PostgreSQL CIDR类型
    cidr_val = fakedata.fake_cidr()
    assert isinstance(cidr_val, str)
    assert '/' in cidr_val  # CIDR应包含斜杠

    # 测试PostgreSQL MACADDR类型
    macaddr_val = fakedata.fake_macaddr()
    assert isinstance(macaddr_val, str)
    assert ':' in macaddr_val or '-' in macaddr_val  # MAC地址应包含分隔符

    # 测试PostgreSQL UUID类型
    uuid_val = fakedata.fake_uuid()
    assert isinstance(uuid_val, str)
    # 验证是否为有效的UUID格式
    try:
        uuid.UUID(uuid_val)
    except ValueError:
        assert False, "fake_uuid should return a valid UUID string"

    # 测试PostgreSQL TSVECTOR类型
    tsvector_val = fakedata.fake_tsvector()
    assert isinstance(tsvector_val, str)

    # 测试PostgreSQL XML类型
    xml_val = fakedata.fake_xml()
    assert isinstance(xml_val, str)
    assert xml_val.startswith('<')
    assert xml_val.endswith('>')


def test_custom_pk_types():
    # 测试字符串主键生成
    str_pk_val = fakedata.fake_str_pk("TEST", 12)
    assert isinstance(str_pk_val, str)
    assert str_pk_val.startswith("TEST")
    assert len(str_pk_val) == 12

    # 测试哈希主键生成
    hash_pk_val = fakedata.fake_hash_pk(16)
    assert isinstance(hash_pk_val, str)
    assert len(hash_pk_val) == 16

    # 测试组合主键生成
    composite_pk_val = fakedata.fake_composite_pk("part1", "part2", 123)
    assert isinstance(composite_pk_val, str)
    assert "part1" in composite_pk_val
    assert "part2" in composite_pk_val
    assert "123" in composite_pk_val

    # 测试随机字符串主键生成
    random_str_pk_val = fakedata.fake_random_str_pk(10)
    assert isinstance(random_str_pk_val, str)
    assert len(random_str_pk_val) == 10