#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datafaker.datatypes.mysql import MySQLDataType
from datafaker.datatypes.postgresql import PostgreSQLDataType
from datafaker.datatypes.hive import HiveDataType


class FackData(MySQLDataType):
    """
    兼容旧版本的类名拼写错误
    """
    pass


class FakeData(MySQLDataType):
    """
    数据生成主类，继承自MySQLDataType
    保持向后兼容性
    """
    pass
