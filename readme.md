# BookRecommend

> 请使用 [Git Commit Angular](https://juejin.cn/post/7126022242508472351) 提交规范进行提交

图书推荐系统, 数据来自 [goodbooks 10k](https://github.com/zygmuntz/goodbooks-10k)  

demo 地址 [http://121.41.114.45:10000/](http://121.41.114.45:10000/)

- 实现功能
  - [x] 根据图书推荐图书
  - [x] 根据用户推荐图书

## 前端

基于 Vue3 + Vite + Pinia + Element Plus 实现

### 整体架构

- 使用 Vue3 组合式 API，提升代码可维护性和复用性。
- 状态管理采用 Pinia，便于全局状态（如用户、图书、收藏等）集中管理。
- 路由采用 vue-router，支持多页面跳转和参数传递。
- 与后端通过 axios 进行 RESTful API 通信，接口统一封装在 src/api。

### 页面设计

- views 目录下包含主要页面：
  - HomeView.vue：主页，展示图书列表和推荐内容。
  - BookDetailView.vue：图书详情页，展示单本书详细信息及相关推荐。
  - FavorView.vue：用户收藏页，展示用户喜欢的书籍。
  - LoginView.vue：登录页，支持用户 ID 登录。

### 构建

> 需要 node22+ 环境, 安装 pnpm

1. 进入 frontend 目录  
2. 在目录下的 .env.production 内将 apiUrl 为实际后端部署 url  
3. 运行

  ```bash
  pnpm build
  ```

构建产物存在目录下的 dist 目录内, 为静态页面, 配置静态网站托管即可部署

## 后端

基于 Python Flask 实现, 数据库采用 MySQL

### 整体架构

- 采用 Flask 框架，结构清晰，易于扩展。
- 主要分为 API 层（main.py）、服务层（service/）、数据模型层（models/）、工具层（utils/）。

### 主要模块

- models/Book.py：定义图书数据模型。
- service/book.py：封装图书相关的业务逻辑。
- db.py：数据库连接与操作封装。
- utils/ 目录：包含数据导入、推荐算法等辅助脚本。

### 推荐算法

- 推荐核心在 utils/upRecommend.py，定时运行，自动更新推荐内容。
- 推荐策略：
  - 基于内容的图书相似推荐（作者、语言、年份等特征）
  - 基于物品/用户协同过滤的个性化推荐（UserCF/ItemCF）
- 推荐结果写入 bookRecommend、userRecommend 两张表，供前端实时查询。

### 数据库交互

- 采用 pymysql 连接 MySQL，所有数据操作均通过 SQL 实现。
- 数据表设计简洁，便于扩展。

### 部署

1. 进入 backend 目录
2. 安装 requirements.txt 的库

   ```bash
   pip install -r requirements.txt
   ```

3. 部署 MySQL 服务, 按 db.py 中的定义配置数据库用户与表
4. 在 utils 目录下创建 origin_data, 将对应的数据文件放入其中, 分别运行 importBooks.py 与 importFavors.py, 将数据导入数据库中
5. 启动项目, 将监听 5000 端口

   ```bash
   python main.py
   ```

6. 设置定时计划, 定期执行 backend/utils/upRecommend.py 对推荐内容进行更新

### 数据库设计

采用 mysql 存储

#### 书籍信息表 bookInfo

> 存储书籍信息

|id|title|cover|authors|goodreadsId|year|lang|avgRating|
|--|-----|-----|-------|-----------|----|----|---------|
|数据库内 id **主键**|书名|封面 url|作者|goodreadsId, 用于生成跳转链接|年份|语言|平均评分|

#### 用户书籍表 favor

> 存储用户喜爱的书籍

|favor_id|userId|bookId|
|--------|------|------|
|记录id|用户 id|书籍 id|

#### 用户推荐书籍表 userRecommend

> 存储用户的个性推荐, 定时更新

|id|userId|bookId|
|--|----|------|
|记录id|用户 id|书籍 id|

#### 书籍推荐书籍表 bookRecommend

> 根据书籍推荐书籍, 定时更新

|id|bookId|recBookId|
|--|----|------|
|记录id|当前书籍 id|推荐书籍 id|
