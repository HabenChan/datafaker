#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime
import random
import time
from typing import Any, Optional, Union
from datafaker.datatypes.base import BaseDataType

class MySQLDataType(BaseDataType):
    
    ######## mysql 数值类型 #############
    def fake_tinyint(self, digits: Optional[Any] = None, unsigned: bool = False) -> int:
        return self.faker.random_int(0, 255) if unsigned else self.faker.random_int(-128, 127)
    
    def fake_smallint(self, digits: Optional[Any] = None, unsigned: bool = False) -> int:
        return self.faker.random_int(0, 65535) if unsigned else self.faker.random_int(-32768, 32767)
    
    def fake_mediumint(self, digits: Optional[Any] = None, unsigned: bool = False) -> int:
        return self.faker.random_int(0, 16777215) if unsigned else self.faker.random_int(-8388608, 8388607)
    
    def fake_int(self, min: Optional[int] = None, max: Optional[int] = None, unsigned: bool = False) -> int:
        if min or max:
            return self.faker.random_int(min, max)
        return self.faker.random_int(0, 4294967295) if unsigned else self.faker.random_int(-2147483648, 2147483647)
    
    def fake_integer(self, *args: Any) -> int:
        return self.fake_int(*args)
    
    def fake_bigint(self, unsigned: bool = False) -> int:
        return self.faker.random_int(-9223372036854775808, 9223372036854775807) if unsigned==False \
            else self.faker.random_int(0, 18446744073709551615)
    
    def fake_float(self, *args: Any) -> float:
        return self.faker.pyfloat()
    
    def fake_double(self, *args: Any) -> float:
        return self.fake_float()
    
    def fake_decimal(self, digits: int, right_digits: int, flag: Optional[int] = None,
                min_value: Optional[float] = None, max_value: Optional[float] = None) -> float:
        """
        mysql中DECIMAL(6,2);
        最多可以存储6位数字，小数位数为2位; 因此范围是从-9999.99到9999.99
        
        而pyfloat left_digits, right_digits 表示小数点左右数字位数
        :param digits: 总位数
        :param right_digits: 小数位数
        :param flag: 符号标志
        :param min_value: 最小值
        :param max_value: 最大值
        :return: 生成的小数
        """
        # 处理负数范围的情况
        positive = True
        if (min_value is not None and min_value < 0) or (max_value is not None and max_value < 0):
            positive = False
        
        if flag is None:
            flag = random.randint(0, 1)
        
        number = self.faker.pyfloat(left_digits=(digits - right_digits), right_digits=right_digits,
                                  positive=positive, min_value=min_value, max_value=max_value)
        
        # 如果指定了符号标志，覆盖随机符号
        if flag is not None:
            return number if flag == 1 else -number
        return number
    
    
    ############ mysql 日期和时间类型 ###################
    
    def fake_date(self, start_date: str = '-30y', end_date: str = 'today', format: str = '%Y-%m-%d') -> str:
        """
        以今天为基点，start_day, end_day两个参数，往前后推的天数
        end_day默认今天
        format为输出格式
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param format: 输出格式
        :return: 生成的日期
        """
        
        thedate = self.faker.date_between(start_date, end_date)
        return thedate.strftime(format)
    
    def fake_datetime_between(self, sdt: str, edt: str, foramt: str = '%Y-%m-%d %H:%M:%S') -> str:
        sdatetime = datetime.datetime.strptime(sdt, '%Y-%m-%d %H:%M:%S')
        stimestamp = int(time.mktime(sdatetime.timetuple()))
        
        edatetime = datetime.datetime.strptime(edt, '%Y-%m-%d %H:%M:%S')
        etimestamp = int(time.mktime(edatetime.timetuple()))
        
        timestamp = random.randint(stimestamp, etimestamp)
        ltime = time.localtime(timestamp)
        return time.strftime(foramt, ltime)
    
    def fake_date_between(self, start_date: str, end_date: str, format: str = '%Y-%m-%d') -> str:
        # 去掉时分秒，不然后续计算天差值会出错
        
        start_date_time = '{0} 00:00:00'.format(start_date)
        end_date_time = '{0} 23:59:59'.format(end_date)
        random_datetime = self.fake_datetime_between(start_date_time, end_date_time)
        random_date = datetime.datetime.strptime(random_datetime.split()[0], '%Y-%m-%d').date()
        return datetime.datetime.strftime(random_date, format)
    
    
    def fake_time(self, *args: Any) -> str:
        return self.faker.time()
    
    def fake_year(self, *args: Any) -> str:
        return self.faker.year()
    
    def fake_datetime(self, now: int = 0, format: str = '%Y-%m-%d %H:%M:%S') -> str:
        dt = datetime.datetime.now() if now else self.faker.date_time()
        return dt.strftime(format)
    
    def fake_timestamp(self, now: int = 0) -> int:
        return int(time.time()) if now else self.faker.unix_time()
    
    ########### mysql 字符串类型##############
    
    def fake_char(self, length: int = 255) -> str:
        return self.faker.pystr(min_chars=length, max_chars=length)
    
    def fake_varchar(self, max_chars: int = 255) -> str:
        return self.faker.pystr(min_chars=1, max_chars=max_chars)
    
    def fake_tinyblob(self, *args: Any) -> bytes:
        # TINYBLOB类型最大长度为255字节
        length = random.randint(0, 255)
        return self.faker.binary(length=length)
    
    def fake_tinytext(self, *args: Any) -> str:
        max_nb_chars = args[0] if len(args) else 255
        return self.faker.text(max_nb_chars=max_nb_chars)
    
    def fake_text(self, *args: Any) -> str:
        """
        生成随机文本
        :param args: 可选参数，指定生成文本的最大字符数
        :return: 随机生成的文本
        """
        max_nb_chars = args[0] if len(args) else 65535
        # 限制最大长度不超过MySQL TEXT类型的限制 (2^16 - 1)
        if max_nb_chars > 65535:
            max_nb_chars = 65535
        return self.faker.text(max_nb_chars=max_nb_chars)
    
    def fake_mediumtext(self, *args: Any) -> str:
        # MEDIUMTEXT类型最大长度为16777215字符 (2^24 - 1)
        # 为了性能考虑，默认生成较小的文本
        max_nb_chars = args[0] if len(args) else 10000
        # 限制最大长度不超过MEDIUMTEXT的限制
        if max_nb_chars > 16777215:
            max_nb_chars = 16777215
        return self.faker.text(max_nb_chars=max_nb_chars)
    
    def fake_longtext(self, *args: Any) -> str:
        # LONGTEXT类型最大长度为4294967295字符 (2^32 - 1)
        # 为了性能考虑，默认生成较小的文本
        max_nb_chars = args[0] if len(args) else 10000
        # 限制最大长度不超过LONGTEXT的限制
        if max_nb_chars > 4294967295:
            max_nb_chars = 4294967295
        return self.faker.text(max_nb_chars=max_nb_chars)
