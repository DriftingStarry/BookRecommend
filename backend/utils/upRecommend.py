import pymysql
from collections import defaultdict, Counter
import random

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

def generate_user_recommend(top_k=5, max_sim_users=10):
    # 1. 一次性加载 favor 表
    conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB, charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute("SELECT userId, bookId FROM favor")
    favor_records = cursor.fetchall()
    cursor.close()
    conn.close()
    print("load table fin")

    user_favors = defaultdict(set)
    book_users = defaultdict(set)
    for userId, bookId in favor_records:
        user_favors[userId].add(bookId)
        book_users[bookId].add(userId)

    users = list(user_favors.keys())
    total = len(users)
    for idx, user in enumerate(users):
        favors = user_favors[user]
        rec_count = Counter()
        for fav in favors:
            sim_users = list(book_users[fav])
            if len(sim_users) > max_sim_users:
                sim_users = random.sample(sim_users, max_sim_users)
            for sim_user in sim_users:
                if sim_user == user:
                    continue
                for b in user_favors[sim_user]:
                    if b not in favors:
                        rec_count[b] += 1
        recs = [b for b, _ in rec_count.most_common(top_k)]
        insert_user_recommend(user, recs)
        if (idx+1) % 10 == 0 or idx == total-1:
            print(f"[userRecommend-ItemCF] 已处理 {idx+1}/{total} 个用户")

if __name__ == '__main__':
    print("开始生成 bookRecommend...")
    generate_book_recommend(top_k=5)
    print("开始生成 userRecommend...")
    generate_user_recommend(top_k=5)
    print("全部推荐生成完毕！")
