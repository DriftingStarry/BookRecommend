from flask import Flask, jsonify, request
from flask_cors import CORS
from models.Book import Book
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
