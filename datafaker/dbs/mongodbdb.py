#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pymongo
from datafaker.dbs.basedb import BaseDB

class MongodbDB(BaseDB):
    
    def __init__(self, args):
        super(MongodbDB, self).__init__(args)
        self.dbtype = 'mongodb'
        self.client = None
        self.db = None
        self.collection = None
    
    def init_connection(self):
        """
        初始化MongoDB连接
        """
        # 解析连接字符串
        # 格式: mongodb://username:password@host:port/dbname
        import re
        pattern = r'mongodb://(.*?):(.*?)@(.*?):(.*?)/(.*?)'
        match = re.match(pattern, self.args.connect)
        if not match:
            raise Exception("Invalid MongoDB connection string")
        
        username, password, host, port, dbname = match.groups()
        
        # 创建MongoDB客户端
        self.client = pymongo.MongoClient(
            host=host,
            port=int(port),
            username=username,
            password=password
        )
        
        # 获取数据库和集合
        self.db = self.client[dbname]
        self.collection = self.db[self.args.table]
    
    def generate_data(self, field_list, fake):
        """
        生成单条数据
        """
        data = {}
        for field in field_list:
            field_name = field[0]
            field_type = field[1]
            field_args = field[2]
            
            # 生成数据
            value = fake.do_fake(field_type, field_args, self.current_num)
            data[field_name] = value
        
        self.current_num += 1
        return data
    
    def batch_insert(self, datas):
        """
        批量插入数据
        """
        if datas:
            self.collection.insert_many(datas)
    
    def do_fake(self):
        """
        执行数据生成
        """
        # 初始化连接
        self.init_connection()
        
        # 解析元数据
        self.parse_meta()
        
        # 生成数据
        if self.args.interval:
            # 流式数据生成
            self.stream_fake()
        else:
            # 批量数据生成
            self.batch_fake()
        
        # 关闭连接
        self.client.close()
