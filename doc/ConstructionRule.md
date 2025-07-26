## 7 Data construction rule
English | [中文](zh_CN/数据构造规则.md)

#### 1. Common types of databases

This part of the data type can be used without specifying a metadata file.

- Numerical type
supports most standard SQL numeric data types.
These types include strict numeric data types ( int, integer, smallint, decimal, and numeric), as well as approximate numeric data types (float, real, and double, precision).

- Date and time type
The date and time types that represent time values ​​are datetime, date, timestamp, time, and year.

- String type
String types refer to char, varchar, binary, varbinary, blob, text, enum, and set. This section describes how these types work and how to use them in queries.


#### 2.Variable database type
------------------
| Type name | description | Defaults | note |
| ---- | ---- | ---- | ---- |
| M,D, negative, min, max) | M specifies the total number of data bits, D specifies the number of decimal places, negative specifies positive 1 negative 0, min,max is the min and max value and must be integer | None | Decimal (4, 2, 1, 70, 90) specifies a 4-digit, 2-digit fractional positive floating point number, such as 78.23 |
| string(min, max) | Min, max specifies the range of string digits | None | |
|date(start, end)| Start, end specifies the date range |  None | Such as date (1990-01-01, 2019-12-12) |


**auto increment type**
------
<font color=#6495ED face="黑体">
inc(mark, start, step)

mark: variable name

start: start value, default value is 1

step: increment step，default value is 1

inc(id) means that the column ID will grow by 1 every time starting from 1. It can be used for MySQL's auto increase primary key

inc(score, 100, 2), means that the column score increase by 2 from 100



</font>

**enum**
------

<font color=#6495ED face="黑体">
The enum type means randomly picking an object randomly from the list, for example:
enum(2, 4, 5, 18) means that one of the four integers 2, 4, 5, 8 is randomly selected each time.

If there is only one object in the enum array, it means that the data list is read from the file, one object per line:
enum(file://data.txt) means to read the list from the data.txt file in the current directory.

The enum type can be used to construct multi-table associations. For example, some fields of two tables use the same enum data list to generate data.
</font>


**order_enum**
-------
Usage same as enum type.

The difference is that it is used to generate enumeration values in cyclic order. It is often used to generate values in associated multiple columns. For example, one column is city code and the other column is city name. The city code needs to correspond to the city name one by one. The number of enumeration values should be the same for the associated multiple columns.

Note: due to multithreading, it is not guaranteed that the sequence is generated in strict accordance with the enumeration value list. But it can ensure that multiple related columns correspond one by one

Please search for issues for details

**op**
-------

<font color=#6495ED face="黑体">
The op type indicates that values are calculated from other columns, such as:

Op (C0 + C3) means the first column value plus the fourth column value

Op (C1 * C4 + C13) means the value of the first column multiplied by the value of the fifth column plus the value of the fourteenth column

</font>


### 3.Custom extension type
-----------------

- address


| rule mark | description |Example | note |
| -------- | -------- | ------ | ------- |
| country| Country name |  China |  |
|province | province | Henan | |
| city | city | Zhengzhou City | |
| city_suffix | City suffix | city | City or county |
|address| address | Block F, Nanning Road, Huairou, Chaohu County, Hebei Province, China 169812 |  |
|country_code | National code | AO | |
|district  | Area | Putuo | |
| latitude  | Geographic coordinates (latitude) | 68.0228435 | |
| longitude | Geographical coordinates (longitude) | 155.964341 | |
| postcode | Zip code | 803511 |  |
|street_address | Street address | Building W, Handan Road | |
|street_name |Street name | Hefei Road| |
| street_suffix | Street | street | |

- Numerical type

| rule mark | description |Example | note |
| -------- | -------- | ------ | ------- |
|random_digit | 0~9 random number| 1 | |
|random_digit_not_null |1~9 random number| 9| |
|random_element | random letter| a | |
|random_int|random number| 44 |The range can be set. The min and max can be set. The default value is 0~9999. For example, random_int(1,100)|
|random_letter| random letter| e | |
|random_number | random number | The digits parameter sets the number of digits of the generated number |For example, random_number(2) generates a 2-digit number |
|boolean| True/False| False | |
|numerify| Three random numbers| 934| |
| number | A certain number of digits | 44322 | number(digits=None, fix_len=0, positive=0) has three parameters, digits means how many digits, fix_len means whether the length is fixed (1 means fixed length, otherwise 1 to digits length) positive means whether it is a positive number (1 is positive, -1 is negative, 0 is both positive and negative). number(18, 1, 1) generates a positive integer with a fixed length of 18 digits|

- Company

| rule mark | description |Example | note |
| -------- | -------- | ------ | ------- |
| bs | Company service name | transition open-source content | |
| company | Company name (long)| Tiankai Information Co., Ltd. | |
| company_prefix | Company name (short)| Puhua Zhongcheng | |
| company_suffix | Company nature | Media Co., Ltd. | |
|job | Position | Project Execution/Coordination Staff | |

- Credit card, currency

| rule mark | description |Example | note |
| -------- | -------- | ------ | ------- |
|credit_card_expire | Credit card expiration date | 05/19 | |
| credit_card_full | Complete credit card information | JCB 16 digit Xia Zhang 3514193766205948 08/21CVC: 436 | |
| credit_card_number |Credit card number| 3500011993590161 | |
| credit_card_provider | Credit card type| American Express | |
| credit_card_security_code | Credit card security code| 190 | |
| currency_code | Currency code | HNL | |

- Date, time

| rule mark | description |Example | note |
| -------- | -------- | ------ | ------- |
| am_pm | AM/PM | AM | |
| century | Century | VII | |
| date | random date |2014-05-18 |date(start_date,end_date,format)<br>start_date represents the number of days pushed back from the current date. The default value is -30y, 30 years ago,<br>end_date represents the number of days pushed back from the current date. The default value is today<br>format is the date format. The default value is %Y-%m-%d<br>For example, date(-30d, +20d, %Y.%m.%d) |
| date_between| Date within specified range| 1997-08-29 |date_between(start_date,end_date,format)<br>start_date represents the start date, required<br>end_date represents the end date, required<br>format is the date format. The default value is %Y-%m-%d<br>date_between(2017-01-01, 2019-12-02, %Y%m%d)|
|date_this_month | Date of the current month | 2019-03-13 | |
| date_this_year | Date within this year | 2019-03-09 | |
| date_time/datetime | Time (from January 1, 1970 to present)| Can be datetime without parameters, or datetime(0) random time, datetime(1,%Y-%m-%d %H:%M) data generation time 2010-06-15 04:07 | datetime(now,format) two parameters: now(0,1 whether to use the current time, the default is 0 for random events, 1 for the current time), format(time format, default is %Y-%m-%d %H:%M:%S)|
| datetime_between | Specified range time | 2009-10-03 03:15:07 |datetime_between(sdt, edt, foramt='%Y-%m-%d %H:%M:%S'), sdt and edt are start and end times, the format is %Y-%m-%d %H:%M:%S, and the format is the output time format. datetime_between('2019-04-14 00:00:00', '2019-04-15 00:00:00') outputs 2019-04-14 00:55:07 |
| month | Random month| 05 | |
|month_name | Random month (English)| December | |
| time() | Random 24-hour time| 18:52:55 | |
| timezone | Random time zone| Europe/Andorra| |
|unix_time |Random Unix time| 203461583 | |
|timestamp |Random Unix time| timestamp/timestamp(0) random timestamp, timestamp(1) current data generation timestamp | With one parameter, the default is 0|
|year | Random year| 2017 | |

- internet

| rule mark | description |Example | note |
| -------- | -------- | ------ | ------- |
|file_extension | File extension | wav | |
| file_name | File name (including extension, without path)| werwe.jpg| |
|file_path | File path (including file name, extension)| /home/| |
| mime_type | mime Type| video/x-flv| |
|company_email |Company email | jieyan@14.cn | |
| domain_name | Domain name | jq.cn | |
| email | email | kren@wei.cn | |
|image_url | Random URL address | https://www.lorempixel.com/470/178| |
|ipv4 | IP4 address | 192.0.25.141 | |
| ipv6 | IP6 address | 206f:1ff0:374:2d5f:a6f8:69ef:4ba9:2d14 | |
| mac_address | MAC address | 65:02:ed:82:c6:98 | |
| tld | Website domain name suffix (.com,.net.cn, etc., excluding.) | cn | |
|uri | URI address| http://24.cn/ | |
|url | URL address| http://www.guiyinglei.cn/ | |

- PostgreSQL Types

| rule mark | description |Example | note |
| -------- | -------- | ------ | ------- |
| real | PostgreSQL REAL type (single precision float) | 12345.67 |  |
| numeric | PostgreSQL NUMERIC type (arbitrary precision) | 1234.56 | numeric(precision, scale) e.g. numeric(5,2) |
| money | PostgreSQL MONEY type (currency format) | $1,234.56 |  |
| timetz | PostgreSQL TIMETZ type (time with time zone) | 12:34:56+08:00 |  |
| timestamptz | PostgreSQL TIMESTAMPTZ type (timestamp with time zone) | 2023-01-01 12:34:56+08:00 |  |
| interval | PostgreSQL INTERVAL type (time interval) | 30 days 12:34:56 |  |
| bytea | PostgreSQL BYTEA type (binary data) | b'\x89PNG\r\n\x1a\n' |  |
| json | PostgreSQL JSON type | {"key": "value"} |  |
| jsonb | PostgreSQL JSONB type (binary JSON) | {"key": "value"} |  |
| inet | PostgreSQL INET type (IP address) | 192.168.1.1 |  |
| cidr | PostgreSQL CIDR type (network address) | 192.168.1.0/24 |  |
| macaddr | PostgreSQL MACADDR type (MAC address) | 08:00:2b:01:02:03 |  |
| uuid | PostgreSQL UUID type | 550e8400-e29b-41d4-a716-446655440000 |  |
| tsvector | PostgreSQL TSVECTOR type (full text search vector) | 'hello world' |  |
| xml | PostgreSQL XML type | <tag>value</tag> |  |

- Custom Primary Key Types

| rule mark | description |Example | note |
| -------- | -------- | ------ | ------- |
| str_pk | String primary key with prefix | ID00000001 | str_pk(prefix, digits) e.g. str_pk(TEST, 10) |
| hash_pk | Hash string primary key | a1b2c3d4e5f6 | hash_pk(length) e.g. hash_pk(16) |
| composite_pk | Composite primary key | part1_part2_123 | composite_pk(part1, part2, part3) |
| random_str_pk | Random string primary key | A1B2C3D4E5 | random_str_pk(length) e.g. random_str_pk(10) |

