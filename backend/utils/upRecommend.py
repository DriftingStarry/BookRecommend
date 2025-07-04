import pymysql

MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'bookRec114514_'
MYSQL_DB = 'books'

def get_all_books():
    conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB, charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute("SELECT id, authors, lang, year FROM bookInfo")
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return books  # [(id, authors, lang, year), ...]

def get_all_users():
    conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB, charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT userId FROM favor")
    users = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return users

def get_user_favors(user_id):
    conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB, charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute("SELECT bookId FROM favor WHERE userId=%s", (user_id,))
    books = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return books

def insert_book_recommend(book_id, rec_book_ids):
    conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB, charset='utf8mb4')
    cursor = conn.cursor()
    # 先删除旧的
    cursor.execute("DELETE FROM bookRecommend WHERE bookId=%s", (book_id,))
    for rec_id in rec_book_ids:
        cursor.execute("INSERT INTO bookRecommend (bookId, recBookId) VALUES (%s, %s)", (book_id, rec_id))
    conn.commit()
    cursor.close()
    conn.close()

def insert_user_recommend(user_id, rec_book_ids):
    conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB, charset='utf8mb4')
    cursor = conn.cursor()
    # 先删除旧的
    cursor.execute("DELETE FROM userRecommend WHERE userId=%s", (user_id,))
    for rec_id in rec_book_ids:
        cursor.execute("INSERT INTO userRecommend (userId, bookId) VALUES (%s, %s)", (user_id, rec_id))
    conn.commit()
    cursor.close()
    conn.close()

def book_similarity(book1, book2):
    # 简单内容相似度：作者相同+1，语言相同+1，年份相近+1
    score = 0
    if book1[1] == book2[1]:
        score += 1
    if book1[2] == book2[2]:
        score += 1
    if abs((book1[3] or 0) - (book2[3] or 0)) <= 2:
        score += 1
    return score

def generate_book_recommend(top_k=5):
    books = get_all_books()
    total = len(books)
    for idx, book in enumerate(books):
        sims = []
        for other in books:
            if other[0] == book[0]:
                continue
            sim = book_similarity(book, other)
            sims.append((other[0], sim))
        sims.sort(key=lambda x: x[1], reverse=True)
        recs = [bid for bid, s in sims[:top_k] if s > 0]
        insert_book_recommend(book[0], recs)
        if (idx+1) % 10 == 0 or idx == total-1:
            print(f"[bookRecommend] 已处理 {idx+1}/{total} 本书")

def generate_user_recommend(top_k=5):
    users = get_all_users()
    books = get_all_books()
    book_dict = {b[0]: b for b in books}
    total = len(users)
    for idx, user in enumerate(users):
        favors = get_user_favors(user)
        recs = set()
        for fav in favors:
            if fav not in book_dict:
                continue
            # 找相似书
            sims = []
            for other in books:
                if other[0] == fav:
                    continue
                sim = book_similarity(book_dict[fav], other)
                sims.append((other[0], sim))
            sims.sort(key=lambda x: x[1], reverse=True)
            for bid, s in sims[:top_k]:
                if s > 0:
                    recs.add(bid)
        recs = list(recs - set(favors))[:top_k]
        insert_user_recommend(user, recs)
        if (idx+1) % 10 == 0 or idx == total-1:
            print(f"[userRecommend] 已处理 {idx+1}/{total} 个用户")

if __name__ == '__main__':
    print("开始生成 bookRecommend...")
    generate_book_recommend(top_k=5)
    print("开始生成 userRecommend...")
    generate_user_recommend(top_k=5)
    print("全部推荐生成完毕！")
