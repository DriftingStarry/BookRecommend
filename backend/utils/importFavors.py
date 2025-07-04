import pandas as pd
import pymysql
import math

# MySQL 连接配置
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'bookRec114514_'
MYSQL_DB = 'books'
MYSQL_TABLE = 'favor'

# 需要导入的字段
csv_path = '.origin_data/favors.csv'
use_columns = [
    'user_id',
    'item_id'
]
field_map = {
    'user_id': 'user_id',
    'item_id': 'book_id'
}

def safe_int(val):
    return int(val) if not (pd.isnull(val) or (isinstance(val, float) and math.isnan(val))) else None

# 连接 MySQL
conn = pymysql.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB,
    charset='utf8mb4'
)
cursor = conn.cursor()

# 初始化表（如果不存在则创建）
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {MYSQL_TABLE} (
    favor_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    book_id INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
cursor.execute(create_table_sql)

# 插入语句
insert_sql = f"""
INSERT INTO {MYSQL_TABLE} (user_id, book_id)
VALUES (%s, %s)
"""

# 分块读取并导入
chunksize = 1000
total = 0
for chunk in pd.read_csv(csv_path, usecols=use_columns, chunksize=chunksize):
    chunk = chunk.rename(columns=field_map)
    data = []
    for idx, row in chunk.iterrows():
        nan_fields = []
        for col in ['user_id', 'book_id']:
            if pd.isnull(row[col]) or (isinstance(row[col], float) and math.isnan(row[col])):
                nan_fields.append(col)
        if nan_fields:
            print(f'发现包含 NaN 的数据（csv 行号: {idx + total + 1}，字段: {nan_fields}）：')
            print(row)
        data.append((
            safe_int(row['user_id']),
            safe_int(row['book_id'])
        ))
    cursor.executemany(insert_sql, data)
    conn.commit()
    total += len(data)
    print(f'已导入 {total} 条数据...')

cursor.close()
conn.close()
print('全部用户喜欢书籍数据已成功分片导入 MySQL books.favor 表！') 