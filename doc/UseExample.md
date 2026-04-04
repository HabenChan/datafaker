## 5. Usage Examples

English | [中文](zh_CN/使用举例.md)

$ stands for terminal prompt

### 5.1. View the version number and parameter usage instructions
---------

```
$ datafaker --version
0.0.8

$ datafaker --help
usage: datafaker [-h] [--meta [META]] [--interval INTERVAL] [--version]
                 [--outprint] [--outspliter OUTSPLITER] [--locale LOCALE]
                 [--outfile OUTFILE] [--format FORMAT]
                 [--withheader]
                 [dbtype] [connect] table [num]

Generates SQLAlchemy model code from an existing database.

positional arguments:
  dbtype                data source type
  connect               connect info to the database
  table                 table to process
  num                   number of records to generate

optional arguments:
  -h, --help            show this help message and exit
  --meta [META]         meta file path
  --interval INTERVAL   the interval to make stream data
  --version             print the version number and exit
  --outprint            print fake data to screen
  --outspliter OUTSPLITER
                        print data, to split columns
  --locale LOCALE       which country language
  --format FORMAT       outprint and outfile format: json, text (default:
                        text)
```

### 5.2. Create a student table in MySQL
---------

```sql
CREATE TABLE stu (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT 'Auto-increment ID',
	name VARCHAR(20) NOT NULL COMMENT 'Student name',
	school VARCHAR(20) NOT NULL COMMENT 'School name',
	nickname VARCHAR(20) NOT NULL COMMENT 'Nickname',
	age INT NOT NULL COMMENT 'Age',
	class_num INT NOT NULL COMMENT 'Class size',
	score DECIMAL(4,2) NOT NULL COMMENT 'Score',
	phone BIGINT NOT NULL COMMENT 'Phone number',
	email VARCHAR(64) COMMENT 'Email',
	ip VARCHAR(32) COMMENT 'IP address',
	address TEXT COMMENT 'Home address'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

```

Create a metadata file `meta.txt` with the student table description. The content of `meta.txt`:
```
id||int||Auto-increment ID[:inc(id,1)]
name||varchar(20)||Student name[:name]
school||varchar(20)||School name[:enum(file://names.txt)]
nickname||varchar(20)||Nickname[:enum(鬼泣, 高小王子, 歌神, 逗比)]
age||int||Student age[:age]
class_num||int||Class size[:int(10, 100)]
score||decimal(4,2)||Score[:decimal(4,2,1)]
phone||bigint||Phone number[:phone_number]
email||varchar(64)||Email[:email]
ip||varchar(32)||IP address[:ipv4]
address||text||Home address[:address]
```

Each row in the `meta.txt` file is a field description, divided into three columns by `||`:

- First column: Field name
- Second column: Table field type
- Third column: Field comment with construction rule tag


If no construction rule is specified, a random string within 20 characters will be generated. You can add a rule, for example: `Student name[:name]`

The `School name[:enum(file://names.txt)]` indicates that the enumeration data is read from the local file `names.txt`. The content of `names.txt` should contain the school names to be randomly selected from:
```
Tsinghua Middle School
People and Center
Guangdong Middle School
Pig Farm School
Old Compound School
```

The construction rules are described in detail in the Construction Rules section.

**Note:** `meta.txt` and `names.txt` must be in the same directory when running datafaker. If there are no enum types, the `names.txt` file is not needed.

### 5.3. Read metadata from meta.txt, split by `,,`, generate 10 records, and output to screen
----------------

```
$ datafaker mysql mysql+mysqldb://root:root@localhost:3600/test stu 10 --outprint --meta meta.txt --outspliter ,, 

 1, Bao Hong,, and the center, Gao Xiao prince,, 3,, 81,, 55.6,, 13197453222,, mwei@gmail.com,, 192.100.224.255, Block I, Liangping Zhu Road, Xining City, Jiangsu Province 944204
 2, Liu Dong, Tsinghua Middle School, Gao Xiaopu, 3,, 31,, 52.4,, 15206198472,, lili@kong.cn,, 203.0.190.6, Block E, Hingshan Hohhot Street, Jiahe City, Inner Mongolia Autonomous Region 706421
 3,,  ,, ,, ,,9,,84,,72.51,,18944398099,,zouchao@gmail.com,,203.1.53.166,Xihe Huizhou Street, Yongan City, Anhui Province, 345415
 4,, Wang Yu,, pig farm,, teasing, 6,89,,19.3,,18,628,114,285,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
 5, Lu Guizhi,, pig farm,, tea, 8, 9, 99, 92.22,, 13304570255,, na55@ti.cn,, 168.136.127.200, Block C, Xuhui Yin Street, Ying County, Jiangsu Province, China 908240
 6, Gu Yang,, pig farm,  ,, 9, 32,, 43.14,, 18025578420,, linping@pr.net,, 174.50.222.39, Block Z, Daye Street, Liangping, Huizhou County, Heilongjiang Province 611736, China
 7, Yang Jie,, People and Center, Devil May Cry, 6, 35,, 81.25,, 13654306263,, minzhong@xiaxia.cn,, 100.57.79.2, Block V, Shawan Wang Street, Linshi, Hubei Province 544660
 8, Shen Yi,, People and Center, Devil May Cry, 6, 14, 14, 73.61,, 13866020503,, changxiulan@chaoxia.cn,, 198.248.254.56, Dongli Ningde Street, Heshan County, Shaanxi Province Block 810017
 9, Shen Qiang,, Guangdong Middle School,, teasing, 7,48,,90.65,,13915915013,,ysun@chao.cn,,169.210.122.39,Z,Zhuan Street,Zhubei Street, Dongmei County, Gansu Province 619755
 10,, Li Dandan,, the old compound, Devil May Cry,, 3,, 67,, 87.63,, 18899812516,, xiulanmo@qin.cn,, 192.52.218.133, 791911, Block E, Xiaoshan Macau Street, Yidu County, Hunan Province
generated records : 10
printed records : 10
time used: 0.458 s
```

If you remove the `--outprint` parameter, the data will be written to MySQL:

```sh
$ datafaker rdb mysql+mysqldb://root:root@localhost:3600/test?charset=utf8 stu 10 --meta meta.txt
```

If you run datafaker again, you must modify `id[:inc(id,11)]` in meta.txt to avoid duplicate key errors.


### Construction Rule Priority

The parser will preferentially parse the construction rule tag in the third column of the field comment. If there is no tag, it will parse based on the field type in the second column.

This approach offers two benefits:
1. For existing data tables, users can copy the table schema using `desc tablename` or `show full columns from tablename`, and then add special processing rules in the comments if the default field type behavior is not sufficient.
2. For new tables, users can directly include the construction rules in the table comments when creating the table, eliminating the need to specify a separate metadata file.


### 5.4. Read metadata from data/hive_meta.txt, generate 1000 records, and insert into Hive

Username is `yarn`. Hive must support ACID; otherwise, data files will be generated and uploaded to HDFS.

```
datafaker hive hive://yarn@localhost:10000/test stu 1000 --meta data/hive_meta.txt
```

### 5.5. Write to file, write to out.txt in /home directory
--------------------

```
datafaker file /home out.txt 10 --meta meta.txt --format json
```


### 5.6. Write to Kafka, write to the topic `hello` every 1 second
-------------------------------------------

```
$ datafaker kafka localhost:9092 hello 1 --meta meta.txt --outprint
{"school": "\u4eba\u548c\u4e2d\u5fc3", "name": "\u5218\u91d1\u51e4", "ip": "192.20.103.235", "age": 9, "email": "chaokang@gang.cn", "phone": "13256316424", "score": 3.45, "address": "\u5e7f\u4e1c\u7701\u5b81\u5fb7\u5e02\u6d54\u9633\u5468\u8defu\u5ea7 990262", "class_num": 24, "nickname": "\u9017\u6bd4", "id": 1}
{"school": "\u4eba\u548c\u4e2d\u5fc3", "name": "\u6768\u4e3d", "ip": "101.129.18.230", "age": 3, "email": "min60@hv.net", "phone": "18183286767", "score": 22.16, "address": "\u8fbd\u5b81\u7701\u592a\u539f\u5e02\u53cb\u597d\u6c55\u5c3e\u8defG\u5ea7 382777", "class_num": 30, "nickname": "\u6b4c\u795e", "id": 2}
{"school": "\u6e05\u534e\u4e2d\u5b66", "name": "\u8d75\u7ea2", "ip": "192.0.3.34", "age": 9, "email": "fxiao@gmail.com", "phone": "18002235094", "score": 48.32, "address": "\u5e7f\u897f\u58ee\u65cf\u81ea\u6cbb\u533a\u65ed\u5e02\u6c88\u5317\u65b0\u6731\u8defc\u5ea7 684262", "class_num": 63, "nickname": "\u6b4c\u795e", "id": 3}
{"school": "\u6e05\u534e\u4e2d\u5b66", "name": "\u5f20\u7389\u6885", "ip": "198.20.50.222", "age": 3, "email": "xiulanlei@cw.net", "phone": "15518698519", "score": 85.96, "address": "\u5b81\u590f\u56de\u65cf\u81ea\u6cbb\u533a\u6d69\u53bf\u767d\u4e91\u4e4c\u9c81\u6728\u9f50\u8857s\u5ea7 184967", "class_num": 18, "nickname": "\u9017\u6bd4", "id": 4}
{"school": "\u732a\u573a", "name": "\u674e\u6842\u5170", "ip": "192.52.195.184", "age": 8, "email": "fxiao@konggu.cn", "phone": "18051928254", "score": 97.87, "address": "\u9ed1\u9f8d\u6c5f\u7701\u54c8\u5c14\u6ee8\u53bf\u6c38\u5ddd\u6d2a\u8857E\u5ea7 335135", "class_num": 46, "nickname": "\u9ad8\u5c0f\u738b\u5b50", "id": 5}
{"school": "\u4eba\u548c\u4e2d\u5fc3", "name": "\u5434\u60f3", "ip": "192.42.234.178", "age": 3, "email": "uliang@yahoo.com", "phone": "14560810465", "score": 6.32, "address": "\u5b81\u590f\u56de\u65cf\u81ea\u6cbb\u533a\u516d\u76d8\u6c34\u5e02\u5357\u6eaa\u7f57\u8857M\u5ea7 852408", "class_num": 12, "nickname": "\u9b3c\u6ce3", "id": 6}
^Cgenerated records : 6
insert records : 6
time used: 6.285 s
```
The result is:

![result](img/kafka.png)

### JSON Nesting or Arbitrary Data Structure
```sh
datafaker kafka localhost:9092 hello 10 --metaj meta.txt
```
Use `--metaj` for metadata file `meta.txt`:
```json
{
    "name": [:name],
    "age": [:age],
    "school": {
        "sch_name": [:enum(file://../data/names.txt)],
        "sch_address": [:address],
        "scores": [
            {
                "class": [:enum(Math, English)],
                "score": [:decimal(4,2,1)]
            },
            {
                "class": [:enum(Chinese, Computer)],
                "score": [:decimal(4,2,1)]
            }
        ]
    }
}
```

Datafaker replaces the marked strings in `meta.txt` while preserving the original format, including tabs and spaces. The result is:
```json
{
    "name": "驷俊",
    "age": 95,
    "school": {
        "sch_name": "旧大院",
        "sch_address": "湖北省济南市上街宁德路I座 557270",
        "scores": [
            {
                "class": "Math",
                "score": 83.28
            },
            {
                "class": "Computer",
                "score": 52.37
            }
        ]
    }
}
```

You can compress the JSON to a single string:
```json
{"name":[:name],"age":[:age],"school":{"sch_name":[:enum(file://../data/names.txt)],"sch_address":[:address],"scores":[{"class":[:enum(Math,English)],"score":[:decimal(4,2,1)]},{"class":[:enum(Chinese,Computer)],"score":[:decimal(4,2,1)]}]}}
```


### 5.7. Write to HBase
----------

```
datafaker hbase localhost:9090 test-table 10 --meta data/hbase.txt
```
You must start the HBase Thrift service (not Thrift2).

For example, create table `test-table` with column family `Cf`. The content of metadata file `hbase.txt` is:

```
rowkey||varchar(20)||the rowkey
Cf:name||varchar(20)||student name
Cf:age||int||age[:age]
```

The first row must be the rowkey. `rowkey(0,1,4)` indicates that the rowkey is formed by joining the values of the first and fifth columns with `_`.


### 5.8. Write to Elasticsearch
-------

```
datafaker es localhost:9200 example1/tp1 100 --auth elastic:elastic --meta meta.txt
```

`localhost:9200` is the connection string for Elasticsearch. Multiple hosts can be specified by separating them with commas, such as `host1:9200,host2:9200`.

`example1/tp1` is the index and type, separated by a backslash.

`elastic:elastic` is the username and password. This parameter is not required if authentication is not enabled.

### 5.9. Write to Oracle
-----
```
datafaker rdb oracle://root:root@127.0.0.1:1521/helowin stu 10 --meta meta.txt
```

The SQLAlchemy connection string must start with `oracle:`.
