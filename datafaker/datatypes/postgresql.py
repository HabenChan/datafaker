#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
import datetime
import uuid
import json
from typing import Any, Optional
from datafaker.datatypes.base import BaseDataType

class PostgreSQLDataType(BaseDataType):
    
    def fake_real(self, *args: Any) -> float:
        """PostgreSQL REAL类型（单精度浮点）"""
        return self.faker.pyfloat(left_digits=4, right_digits=2)
    
    def fake_numeric(self, precision: Optional[int] = None, scale: Optional[int] = None) -> str:
        """
        PostgreSQL NUMERIC类型
        precision: 总位数
        scale: 小数位数
        """
        if precision is None:
            # 如果没有指定精度，默认使用10位总长度
            precision = 10
        if scale is None:
            # 如果没有指定小数位数，默认使用2位小数
            scale = 2
            
        # 整数部分位数
        integer_digits = precision - scale
        
        # 生成整数部分
        if integer_digits > 0:
            max_integer = 10 ** integer_digits - 1
            integer_part = self.faker.random_int(0, max_integer)
        else:
            integer_part = 0
            
        # 生成小数部分
        if scale > 0:
            # 生成scale位数字的字符串
            decimal_part = "".join([str(self.faker.random_digit()) for _ in range(scale)])
        else:
            decimal_part = ""
            
        # 组合数字
        if scale > 0:
            number_str = f"{integer_part}.{decimal_part}"
        else:
            number_str = str(integer_part)
            
        # 随机添加正负号
        if self.faker.boolean():
            number_str = "-" + number_str
            
        return number_str
    
    def fake_money(self, *args: Any) -> str:
        """PostgreSQL MONEY类型（货币格式）"""
        return "${:,.2f}".format(self.faker.pyfloat(positive=True, max_value=100000))
    
    def fake_timetz(self, *args: Any) -> str:
        """PostgreSQL TIMETZ类型（带时区时间）"""
        return self.faker.time(pattern="%H:%M:%S%z")

    def fake_timestamptz(self, *args: Any) -> str:
        """PostgreSQL TIMESTAMPTZ类型（带时区时间戳）"""
        return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S%z")

    def fake_interval(self, *args: Any) -> str:
        """PostgreSQL INTERVAL类型（时间间隔）"""
        days = random.randint(0, 365)
        seconds = random.randint(0, 86400)
        return f"{days} days {seconds} seconds"
    
    def fake_bytea(self, max_bytes: int = 1024) -> str:
        """PostgreSQL BYTEA类型（二进制数据）"""
        blob_data = self.faker.binary(length=random.randint(1, max_bytes))
        return blob_data.hex()  # 返回十六进制字符串而不是bytes

    def fake_json(self, *args: Any) -> str:
        """PostgreSQL JSON类型"""
        return json.dumps({"data": self.faker.word(), "value": self.faker.random_int()})

    def fake_jsonb(self, *args: Any) -> str:
        """PostgreSQL JSONB类型（二进制JSON）"""
        return self.fake_json()  # 直接返回JSON字符串而不是编码后的bytes
    
    def fake_inet(self, *args: Any) -> str:
        """PostgreSQL INET类型（IP地址）"""
        return self.faker.ipv4()

    def fake_cidr(self, *args: Any) -> str:
        """PostgreSQL CIDR类型（网络地址）"""
        return f"{self.faker.ipv4()}/{random.randint(16, 24)}"

    def fake_macaddr(self, *args: Any) -> str:
        """PostgreSQL MACADDR类型（MAC地址）"""
        return self.faker.mac_address()  
        
    def fake_uuid(self, *args: Any) -> str:
        """PostgreSQL UUID类型"""
        return str(uuid.uuid4())

    def fake_tsvector(self, max_words: int = 5) -> str:
        """PostgreSQL TSVECTOR类型（全文搜索向量）"""
        words = [self.faker.word() for _ in range(random.randint(1, max_words))]
        return " ".join(words)

    def fake_xml(self, *args: Any) -> str:
        """PostgreSQL XML类型"""
        return f"<root><value>{self.faker.random_int()}</value></root>" 
