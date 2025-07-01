# BookRecommend

> 请使用 [Git Commit Angular](https://juejin.cn/post/7126022242508472351) 提交规范进行提交

图书推荐系统, 数据来自 [goodbooks 10k](https://github.com/zygmuntz/goodbooks-10k)

- 实现功能
  - [ ] 根据图书推荐图书
  - [ ] 根据用户推荐图书

## 前端

vue3 全家桶 + element plus

## 后端

python flask

### 数据库设计

采用 mysql 存储

#### 书籍信息表 bookInfo

> 存储书籍信息

|id|title|cover|authors|goodreadsId|year|lang|avgRating|
|--|-----|-----|-------|-----------|----|----|---------|
|数据库内 id **主键**|书名|封面 url|作者|goodreadsId, 用于生成跳转链接|年份|语言|平均评分|

#### 用户书籍表 favor

> 存储用户喜爱的书籍

|userId|bookId|
|------|------|
|用户 id|书籍 id|

#### 用户推荐书籍表 userRecommend

> 存储用户的个性推荐, 定时更新

|userId|bookId|
|------|------|
|用户 id|书籍 id|

#### 书籍推荐书籍表 bookRecommend

> 根据书籍推荐书籍, 定时更新

|bookId|recBookId|
|------|------|
|当前书籍 id|推荐书籍 id|
