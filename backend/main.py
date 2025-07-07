from flask import Flask, jsonify, request
from flask_cors import CORS
import service.book as bookService

app = Flask(__name__)
CORS(app)  # 启用跨域支持，方便前端调用

@app.route('/test', methods=['GET'])
def test():
    """测试接口"""
    return jsonify({
        "code": 200,
        "msg": "yee",
        "data": "yee"
    })

@app.route('/book', methods=['GET'])
def getBookInfo():
    """获取书籍信息"""
    id = int(request.args.get('id'))
    book = bookService.getBookInfo(id)
    return jsonify({
        "code": 200,
        "msg": "获取书籍信息成功",
        "data": book.to_dict()
    })

@app.route('/books', methods=['GET'])
def getBooks():
    """获取书籍列表"""
    page = int(request.args.get('page'))
    pageSize = int(request.args.get('pageSize'))
    books, total = bookService.getBooks(page, pageSize)
    return jsonify({
        "code": 200,
        "msg": "获取书籍列表成功",
        "data": {
            "books": [
                book.to_dict() for book in books
            ],
            "total": total
        }
    })

@app.route('/recommend', methods=['GET'])
def getRecommend():
    """获取推荐书籍"""
    by = request.args.get('by')
    id = int(request.args.get('id'))
    books = bookService.getBookRecommend(by, id)
    return jsonify({
        "code": 200,
        "msg": "获取推荐书籍成功",
        "data": [
            book.to_dict() for book in books
        ]
    })

@app.route('/user/favor', methods=['GET', 'POST', 'DELETE'])
def favor_handler():
    if request.method == 'GET':
        user_id = int(request.args.get('userId'))
        print(user_id)
        if not user_id:
            return jsonify({"code": 400, "msg": "缺少 userId", "data": None})
        try:
            user_id = int(user_id)
        except:
            return jsonify({"code": 400, "msg": "userId 格式错误", "data": None})
        book_ids = bookService.get_favor_books(user_id)
        return jsonify({"code": 200, "msg": "查询成功", "data": book_ids})
    elif request.method == 'POST':
        user_id = request.form.get('userId')
        book_id = request.form.get('bookId')
        if not user_id or not book_id:
            return jsonify({"code": 400, "msg": "缺少 userId 或 bookId", "data": None})
        try:
            user_id = int(user_id)
            book_id = int(book_id)
        except:
            return jsonify({"code": 400, "msg": "userId 或 bookId 格式错误", "data": None})
        success, msg = bookService.add_favor_book(user_id, book_id)
        return jsonify({"code": 200 if success else 400, "msg": msg, "data": success})
    elif request.method == 'DELETE':
        user_id = request.form.get('userId')
        book_id = request.form.get('bookId')
        if not user_id or not book_id:
            return jsonify({"code": 400, "msg": "缺少 userId 或 bookId", "data": None})
        try:
            user_id = int(user_id)
            book_id = int(book_id)
        except:
            return jsonify({"code": 400, "msg": "userId 或 bookId 格式错误", "data": None})
        success, msg = bookService.del_favor_book(user_id, book_id)
        return jsonify({"code": 200 if success else 400, "msg": msg, "data": success})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
