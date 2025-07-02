# 用于导入书籍信息到数据库

import pandas as pd
import pymysql
import math

# MySQL 连接配置
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'bookRec114514_'
MYSQL_DB = 'books'
MYSQL_TABLE = 'bookInfo'

# 需要导入的字段
csv_path = './backend/utils/origin_data/books.csv'
use_columns = [
    'book_id',
    'goodreads_book_id',
    'authors',
    'title',
    'language_code',
    'original_publication_year',
    'average_rating',
    'image_url',
    'ratings_count'
]
field_map = {
    'book_id': 'id',
    'goodreads_book_id': 'goodreadsId',
    'authors': 'authors',
    'title': 'title',
    'language_code': 'lang',
    'original_publication_year': 'year',
    'average_rating': 'avgRating'
}

def safe_int(val):
    return int(val) if not (pd.isnull(val) or (isinstance(val, float) and math.isnan(val))) else None

def safe_float(val):
    return float(val) if not (pd.isnull(val) or (isinstance(val, float) and math.isnan(val))) else None

def safe_str(val):
    if pd.isnull(val) or (isinstance(val, float) and math.isnan(val)):
        return None
    return str(val)

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
    id INT PRIMARY KEY,
    goodreadsId INT,
    authors TEXT,
    title VARCHAR(255),
    lang VARCHAR(20),
    year INT,
    avgRating FLOAT,
    cover TEXT,
    ratingsCount INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
cursor.execute(create_table_sql)

# 插入语句
insert_sql = f"""
INSERT INTO {MYSQL_TABLE} (id, goodreadsId, authors, title, lang, year, avgRating, cover, ratingsCount)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    goodreadsId=VALUES(goodreadsId),
    authors=VALUES(authors),
    title=VALUES(title),
    lang=VALUES(lang),
    year=VALUES(year),
    avgRating=VALUES(avgRating)
"""

# 分块读取并导入
chunksize = 1000
total = 0
for chunk in pd.read_csv(csv_path, usecols=use_columns, chunksize=chunksize):
    chunk = chunk.rename(columns=field_map)
    data = []
    for idx, row in chunk.iterrows():
        nan_fields = []
        for col in ['id', 'goodreadsId', 'authors', 'title', 'lang', 'year', 'avgRating', 'image_url', 'ratings_count']:
            if pd.isnull(row[col]) or (isinstance(row[col], float) and math.isnan(row[col])):
                nan_fields.append(col)
        if nan_fields:
            print(f'发现包含 NaN 的数据（csv 行号: {idx + total + 1}，字段: {nan_fields}）：')
            print(row)
        data.append((
            safe_int(row['id']),
            safe_int(row['goodreadsId']),
            safe_str(row['authors']),
            safe_str(row['title']),
            safe_str(row['lang']),
            safe_int(row['year']),
            safe_float(row['avgRating']),
            safe_str(row['image_url']),
            safe_int(row['ratings_count'])
        ))
    cursor.executemany(insert_sql, data)
    conn.commit()
    total += len(data)
    print(f'已导入 {total} 条数据...')

cursor.close()
conn.close()
print('全部书籍数据已成功分片导入 MySQL books.bookInfo 表！')





