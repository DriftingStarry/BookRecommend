import db
from models.Book import Book

def getBookInfo(id:int):
    res = db.getBookInfo(id)
    # id, goodreadsId, authors, title, lang, year, avgRating, cover
    # print(res)
    return Book(
        id=res[0],
        goodreadsId=res[1],
        authors=res[2],
        title=res[3],
        lang=res[4],
        year=res[5],
        avgRating=res[6],
        cover=res[7],
        ratingsCount=res[8]
    )
    
def getBooks(page:int, pageSize:int):
    res, total = db.getBooksByPage(page, pageSize)
    return [Book(
        id=row[0],
        goodreadsId=row[1],
        authors=row[2],
        title=row[3],
        lang=row[4],
        year=row[5],
        avgRating=row[6],
        cover=row[7],
        ratingsCount=row[8]
    ) for row in res], total

def getBookRecommend(by:str, id:int):
    if by != 'book' and by != 'user': return []
    res = db.getBookRecommend(id) if by == 'book' else db.getUserRecommend(id)
    # print(res)

    return [getBookInfo(row[0]) for row in res]

def add_favor_book(user_id: int, book_id: int):
    return db.addFavorBook(user_id, book_id)

def del_favor_book(user_id: int, book_id: int):
    return db.delFavorBook(user_id, book_id)

def get_favor_books(user_id: int):
    bookIds = db.getFavorBooks(user_id)
    # print(bookIds)
    return [row[0] for row in bookIds]