from flask import Flask, jsonify, request
from flask_cors import CORS
from models.books import Book

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
    print(request.args.get('id'))
    return jsonify({
        "code": 200,
        "msg": "获取书籍信息成功",
        "data": Book(
            authors="yee",
            avgRating=1.0,
            cover="yee",
            goodreadsId="yee",
            id=1,
            lang="yee",
            ratingsCount="yee",
            title="yee",
            year=2025
        ).to_dict()
    })

@app.route('/books', methods=['GET'])
def getBooks():
    """获取书籍列表"""
    print(request.args.get('page'))
    print(request.args.get('pageSize'))
    return jsonify({
        "code": 200,
        "msg": "获取书籍列表成功",
        "data": {
            "books": [
                Book(
                    authors="yee",
                    avgRating=1.0,
                    cover="yee",
                    goodreadsId="yee",
                    id=1,
                    lang="yee",
                    ratingsCount="yee",
                    title="yee",
                    year=2025
                ).to_dict()
            ],
            "total": 100
        }
    })

@app.route('/recommend', methods=['GET'])
def getRecommend():
    """获取推荐书籍"""
    print(request.args.get('by'))
    print(request.args.get('id'))
    return jsonify({
        "code": 200,
        "msg": "获取推荐书籍成功",
        "data": [
            Book(
                authors="yee",
                avgRating=1.0,
                cover="yee",
                goodreadsId="yee",
                id=1,
                lang="yee",
                ratingsCount="yee",
                title="yee",
                year=2025
            ).to_dict()
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
