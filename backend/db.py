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
    
    