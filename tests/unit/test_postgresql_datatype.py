#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import uuid
from datafaker.constant import DEFAULT_LOCALE
from datafaker.datatypes.postgresql import PostgreSQLDataType

postgres_fakedata = PostgreSQLDataType(DEFAULT_LOCALE)


def test_postgresql_real():
    """测试PostgreSQL REAL类型"""
    real_val = postgres_fakedata.fake_real()
    assert isinstance(real_val, float)


def test_postgresql_numeric():
    """测试PostgreSQL NUMERIC类型"""
    # 测试默认参数
    numeric_val1 = postgres_fakedata.fake_numeric()
    assert isinstance(numeric_val1, str)
    
    # 测试指定精度和小数位数
    numeric_val2 = postgres_fakedata.fake_numeric(5, 2)
    assert isinstance(numeric_val2, str)
    if '.' in numeric_val2:
        integer_part, decimal_part = numeric_val2.split('.')
        assert len(decimal_part) == 2


def test_postgresql_money():
    """测试PostgreSQL MONEY类型"""
    money_val = postgres_fakedata.fake_money()
    assert isinstance(money_val, str)
    assert money_val.startswith('$')
    assert '.' in money_val


def test_postgresql_timetz():
    """测试PostgreSQL TIMETZ类型"""
    timetz_val = postgres_fakedata.fake_timetz()
    assert isinstance(timetz_val, str)
    assert ':' in timetz_val


def test_postgresql_timestamptz():
    """测试PostgreSQL TIMESTAMPTZ类型"""
    timestamptz_val = postgres_fakedata.fake_timestamptz()
    assert isinstance(timestamptz_val, str)
    assert ' ' in timestamptz_val


def test_postgresql_interval():
    """测试PostgreSQL INTERVAL类型"""
    interval_val = postgres_fakedata.fake_interval()
    assert isinstance(interval_val, str)
    assert 'days' in interval_val
    assert 'seconds' in interval_val


def test_postgresql_bytea():
    """测试PostgreSQL BYTEA类型"""
    bytea_val = postgres_fakedata.fake_bytea()
    assert isinstance(bytea_val, str)


def test_postgresql_json():
    """测试PostgreSQL JSON类型"""
    json_val = postgres_fakedata.fake_json()
    assert isinstance(json_val, str)
    parsed = json.loads(json_val)
    assert 'data' in parsed
    assert 'value' in parsed


def test_postgresql_jsonb():
    """测试PostgreSQL JSONB类型"""
    jsonb_val = postgres_fakedata.fake_jsonb()
    assert isinstance(jsonb_val, str)


def test_postgresql_inet():
    """测试PostgreSQL INET类型"""
    inet_val = postgres_fakedata.fake_inet()
    assert isinstance(inet_val, str)
    assert '.' in inet_val


def test_postgresql_cidr():
    """测试PostgreSQL CIDR类型"""
    cidr_val = postgres_fakedata.fake_cidr()
    assert isinstance(cidr_val, str)
    assert '/' in cidr_val


def test_postgresql_macaddr():
    """测试PostgreSQL MACADDR类型"""
    macaddr_val = postgres_fakedata.fake_macaddr()
    assert isinstance(macaddr_val, str)


def test_postgresql_uuid():
    """测试PostgreSQL UUID类型"""
    uuid_val = postgres_fakedata.fake_uuid()
    assert isinstance(uuid_val, str)
    # 验证UUID格式
    try:
        uuid.UUID(uuid_val)
    except ValueError:
        assert False, "UUID格式不正确"


def test_postgresql_tsvector():
    """测试PostgreSQL TSVECTOR类型"""
    tsvector_val = postgres_fakedata.fake_tsvector()
    assert isinstance(tsvector_val, str)


def test_postgresql_xml():
    """测试PostgreSQL XML类型"""
    xml_val = postgres_fakedata.fake_xml()
    assert isinstance(xml_val, str)
    assert '<root>' in xml_val
    assert '</root>' in xml_val
