#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime
import random
import time
from faker import Faker, Factory
from datafaker import compat
from datafaker.compat import Dict
import json
import uuid


class FackData(object):

    def __init__(self, locale):

        self.faker = Factory().create(locale)
        self.faker_funcs = dir(self.faker)
        self.lock = compat.Lock()
        self.auto_inc = Dict()
        self.current_num = 0

    ######## mysql 数值类型 #############

    def fake_tinyint(self, digits=None, unsigned=False):
        return self.faker.random_int(0, 255) if unsigned else self.faker.random_int(-128, 127)

    def fake_smallint(self, digits=None, unsigned=False):
        return self.faker.random_int(0, 65535) if unsigned else self.faker.random_int(-32768, 32767)

    def fake_mediumint(self, digits=None, unsigned=False):
        return self.faker.random_int(0, 16777215) if unsigned else self.faker.random_int(-8388608, 8388607)

    def fake_int(self, min=None, max=None, unsigned=False):
        if min or max:
            return self.faker.random_int(min, max)
        return self.faker.random_int(0, 4294967295) if unsigned else self.faker.random_int(-2147483648, 2147483647)

    def fake_integer(self, *args):
        return self.fake_int(*args)

    def fake_bigint(self, unsigned=False):
        return self.faker.random_int(0, 18446744073709551615) if unsigned==False \
            else self.faker.random_int(-9223372036854775808, 9223372036854775807)

    def fake_float(self, *args):
        return self.faker.pyfloat()

    def fake_double(self, *args):
        return self.fake_float()

    def fake_decimal(self, digits, right_digits, flag=None,
                min_value=None, max_value=None):
        """
        mysql中DECIMAL(6,2);
        最多可以存储6位数字，小数位数为2位; 因此范围是从-9999.99到9999.99

        而pyfloat left_digits, right_digits 表示小数点左右数字位数
        :param args:
        :return:
        """
        if flag is None:
            flag = random.randint(0, 1)
        number = self.faker.pyfloat(left_digits=(digits - right_digits), right_digits=right_digits,
                                  positive=True, min_value=min_value, max_value=max_value)
        return number if flag == 1 else -number


    ############ mysql 日期和时间类型 ###################

    def fake_date(self, start_date='-30y', end_date='today', format='%Y-%m-%d'):
        """
        以今天为基点，start_day, end_day两个参数，往前后推的天数
        end_day默认今天
        format为输出格式
        :param args:
        :return:
        """

        thedate = self.faker.date_between(start_date, end_date)
        return thedate.strftime(format)

    def fake_datetime_between(self, sdt, edt, foramt='%Y-%m-%d %H:%M:%S'):
        sdatetime = datetime.datetime.strptime(sdt, '%Y-%m-%d %H:%M:%S')
        stimestamp = int(time.mktime(sdatetime.timetuple()))

        edatetime = datetime.datetime.strptime(edt, '%Y-%m-%d %H:%M:%S')
        etimestamp = int(time.mktime(edatetime.timetuple()))

        timestamp = random.randint(stimestamp, etimestamp)
        ltime = time.localtime(timestamp)
        return time.strftime(foramt, ltime)

    def fake_date_between(self, start_date, end_date, format='%Y-%m-%d'):
        # 去掉时分秒，不然后续计算天差值会出错

        start_date_time = '{0} 00:00:00'.format(start_date)
        end_date_time = '{0} 23:59:59'.format(end_date)
        random_datetime = self.fake_datetime_between(start_date_time, end_date_time)
        random_date = datetime.datetime.strptime(random_datetime.split()[0], '%Y-%m-%d').date()
        return datetime.datetime.strftime(random_date, format)


    def fake_time(self, *args):
        return self.faker.time()

    def fake_year(self, *args):
        return self.faker.year()

    def fake_datetime(self, now=0, format='%Y-%m-%d %H:%M:%S'):
        dt = datetime.datetime.now() if now else self.faker.date_time()
        return dt.strftime(format)



    def fake_timestamp(self, now=0):

        # timestamp = int(time.time()) if now else self.faker.unix_time()
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ########### mysql 字符串类型##############

    def fake_char(self, length=255):
        return self.faker.pystr(min_chars=length, max_chars=length)

    def fake_varchar(self, max_chars=255):
        return self.faker.pystr(min_chars=1, max_chars=max_chars)

    def fake_tinyblob(self, *args):
        # TINYBLOB类型最大长度为255字节
        length = random.randint(0, 255)
        blob_data = self.faker.binary(length=length)
        return blob_data.hex()  # 返回十六进制字符串而不是bytes

    def fake_tinytext(self, *args):
        max_nb_chars = args[0] if len(args) else 255
        return self.faker.text(max_nb_chars=max_nb_chars)

    def fake_text(self, *args):
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

    def fake_mediumtext(self, *args):
        # MEDIUMTEXT类型最大长度为16777215字符 (2^24 - 1)
        # 为了性能考虑，默认生成较小的文本
        max_nb_chars = args[0] if len(args) else 10000
        # 限制最大长度不超过MEDIUMTEXT的限制
        if max_nb_chars > 16777215:
            max_nb_chars = 16777215
        return self.faker.text(max_nb_chars=max_nb_chars)

    def fake_longtext(self, *args):
        # LONGTEXT类型最大长度为4294967295字符 (2^32 - 1)
        # 为了性能考虑，默认生成较小的文本
        max_nb_chars = args[0] if len(args) else 10000
        # 限制最大长度不超过LONGTEXT的限制
        if max_nb_chars > 4294967295:
            max_nb_chars = 4294967295
        return self.faker.text(max_nb_chars=max_nb_chars)

    ############ hive 基本数据类型 #############

    def fake_number(self, digits=None, fix_len=0, positive=0):
        """
        digits=None, fix_len=0, positive=0

        :param digits:
        :param fix_len:
        :param positive:
        :return:
        """
        fixlen = (fix_len == 1)
        val = self.faker.random_number(digits=digits, fix_len=fixlen)
        if positive > 0:
            val = val if val >= 0 else -val
        if positive < 0:
            val = val if val <= 0 else -val
        return val

    def fake_string(self, *args):
        return self.faker.pystr(*args)

    ####### 定制函数 ##########
    def fake_age(self, *args):
        if not args:
            args = [0, 120]
        return self.faker.random_int(*args)

    def fake_inc(self, mark, start=0, step=1):
        """
        用于实现整型变量自增
        :param args:
        :return:
        """
        with self.lock:
            if mark not in self.auto_inc:
                self.auto_inc[mark] = int(start)
            ret = self.auto_inc[mark]
            self.auto_inc[mark] += int(step)
        return ret

    def fake_enum(self, *args):
        """
        实现枚举类型，随机返回一个列表中值
        :param args: 枚举数组
        :return:
        """
        return random.choice(list(args))

    def fake_order_enum(self, *args):
        """
        用于循环顺序产生枚举值。常用于多列关联产生值
        :param args: 数组值
        :return:
        """
        datas = list(args)
        num = len(datas)

        idx = (self.current_num % num) - 1
        return datas[idx]


    def fake_op(self, *args):
        """
        实现多字段四项运算
        :param args:
        :return:
        """
        return None

    def fake_real(self, *args):
        """PostgreSQL REAL类型（单精度浮点）"""
        return self.faker.pyfloat(left_digits=4, right_digits=2)
    
    def fake_numeric(self, precision=None, scale=None):
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
    
    def fake_money(self, *args):
        """PostgreSQL MONEY类型（货币格式）"""
        return "${:,.2f}".format(self.faker.pyfloat(positive=True, min_value=0, max_value=100000))
    
    def fake_timetz(self, *args):
        """PostgreSQL TIMETZ类型（带时区时间）"""
        return self.faker.time(pattern="%H:%M:%S%z")

    def fake_timestamptz(self, *args):
        """PostgreSQL TIMESTAMPTZ类型（带时区时间戳）"""
        return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S%z")

    def fake_interval(self, *args):
        """PostgreSQL INTERVAL类型（时间间隔）"""
        days = random.randint(0, 365)
        seconds = random.randint(0, 86400)
        return f"{days} days {seconds} seconds"
    
    def fake_bytea(self, max_bytes=1024):
        """PostgreSQL BYTEA类型（二进制数据）"""
        blob_data = self.faker.binary(length=random.randint(1, max_bytes))
        return blob_data.hex()  # 返回十六进制字符串而不是bytes

    def fake_json(self, *args):
        """PostgreSQL JSON类型"""
        return json.dumps({"data": self.faker.word(), "value": self.faker.random_int()})

    def fake_jsonb(self, *args):
        """PostgreSQL JSONB类型（二进制JSON）"""
        return self.fake_json()  # 直接返回JSON字符串而不是编码后的bytes
    
    def fake_inet(self, *args):
        """PostgreSQL INET类型（IP地址）"""
        return self.faker.ipv4()

    def fake_cidr(self, *args):
        """PostgreSQL CIDR类型（网络地址）"""
        return f"{self.faker.ipv4()}/{random.randint(16, 24)}"

    def fake_macaddr(self, *args):
        """PostgreSQL MACADDR类型（MAC地址）"""
        return self.faker.mac_address()  
        
    def fake_uuid(self, *args):
        """PostgreSQL UUID类型"""
        return str(uuid.uuid4())

    def fake_tsvector(self, max_words=5):
        """PostgreSQL TSVECTOR类型（全文搜索向量）"""
        words = [self.faker.word() for _ in range(random.randint(1, max_words))]
        return " ".join(words)

    def fake_xml(self, *args):
        """PostgreSQL XML类型"""
        return f"<root><value>{self.faker.random_int()}</value></root>" 
    
    def fake_str_pk(self, prefix="ID", digits=8):
        """
        生成带前缀的自增字符串主键（如：ID00000001）
        :param prefix: 主键前缀
        :param digits: 总长度
        :return: 字符串主键
        """
        mark = f"str_pk_{prefix}"
        with self.lock:
            if mark not in self.auto_inc:
                self.auto_inc[mark] = 0
            current_val = self.auto_inc[mark]
            self.auto_inc[mark] += 1
        # 计算数字部分的位数
        prefix_len = len(prefix)
        number_len = int(digits) - prefix_len
        # 确保数字部分至少有1位
        if number_len < 1:
            number_len = 1
        return f"{prefix}{str(current_val).zfill(number_len)}"

    def fake_hash_pk(self, length=32):
        """
        生成哈希字符串主键（如UUID的简化版）
        :param length: 哈希长度（16/32/64）
        :return: 哈希字符串
        """
        return self.faker.sha256(raw_output=False)[:length]

    def fake_composite_pk(self, *parts):
        """
        生成组合主键（多个字段用分隔符合并）
        :param parts: 要组合的值列表
        :return: 组合后的字符串
        """
        separator = "_"
        return separator.join(str(part) for part in parts)

    def fake_random_str_pk(self, length=16, chars="ABCDEFGHJKLMNPQRSTUVWXYZ23456789"):
        """
        生成随机字符串主键（避免易混淆字符）
        :param length: 字符串长度
        :param chars: 允许的字符集
        :return: 随机字符串
        """
        return ''.join(random.choices(chars, k=length))
    ######## 执行主函数 #########
    def do_fake(self, keyword, args, current_num):
        """
        首先查看是否在faker类的成员函数内，如果在则调用；
        否者调用FakeData类中自定义的成员函数
        :param keyword:
        :param args:
        :return:
        """
        self.current_num = current_num
        method = getattr(self, 'fake_' + keyword, None)
        if callable(method):
            return method(*args)
        if keyword in self.faker_funcs:
            method = getattr(self.faker, keyword, None)
            if callable(method):
                return method(*args)
        return None