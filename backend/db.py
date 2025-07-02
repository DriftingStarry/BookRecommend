import pymysql

MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'bookRec114514_'
MYSQL_DB = 'books'

def getBookInfo(bookId:int)->tuple[int,str,str,str,str,int,float,str,int]:
    conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM bookInfo WHERE id = {bookId}")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def getBookRecommend(bookId:int)->tuple[tuple[int]]:
    conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    cursor.execute(f"SELECT recBookId FROM bookRecommend WHERE bookId = {bookId}")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def getUserRecommend(userId:int)->tuple[tuple[int]]:
    conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    cursor.execute(f"SELECT bookId FROM userRecommend WHERE userId = {userId}")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def getBooksByPage(page: int, page_size: int)->tuple[tuple[tuple[int,str,str,str,str,int,float,str,int]], int]:
    conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    # 获取总数
    cursor.execute("SELECT COUNT(*) FROM bookInfo;")
    total_row = cursor.fetchone()
    total = total_row[0] if total_row else 0
    # 获取当前页数据
    offset = (page - 1) * page_size
    sql = "SELECT * FROM bookInfo LIMIT %s OFFSET %s;"
    cursor.execute(sql, (page_size, offset))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data, total
    
def addFavorBook(userId:int, bookId:int):
    conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    try:
        # 校验是否已存在
        cursor.execute("SELECT 1 FROM favor WHERE userId=%s AND bookId=%s", (userId, bookId))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False, '已经喜爱书籍'
        # 插入新记录
        cursor.execute("INSERT INTO favor (userId, bookId) VALUES (%s, %s)", (userId, bookId))
        conn.commit()
        cursor.close()
        conn.close()
        return True, '添加成功'
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return False, str(e)

def delFavorBook(userId:int, bookId:int):
    conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM favor WHERE userId=%s AND bookId=%s", (userId, bookId))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        if affected > 0:
            return True, '删除成功'
        else:
            return False, '未找到记录'
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return False, str(e)

def getFavorBooks(userId:int)->tuple[tuple[int]]:
    conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT bookId FROM favor WHERE userId=%s", (userId,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        # 返回 id 列表
        print('re', result)
        return result
    except Exception as e:
        cursor.close()
        conn.close()
        return ()