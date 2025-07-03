import pandas as pd

# 加载数据
df = pd.read_csv(r'data/train_dataset.csv')

# 统计每个 item_id 被多少不同用户喜欢
book_user_count = df.groupby('item_id')['user_id'].nunique().reset_index()
book_user_count.columns = ['item_id', 'count']

# 线性映射 count → score (范围：2 ~ 5)
min_count = book_user_count['count'].min()
max_count = book_user_count['count'].max()

# 防止除以零
if max_count == min_count:
    book_user_count['score'] = 3.5  # 所有得分中间值
else:
    book_user_count['score'] = 2 + (book_user_count['count'] - min_count) * 3 / (max_count - min_count)

# 四舍五入保留两位小数（可选）
book_user_count['score'] = book_user_count['score'].round(2)

# 排序并保存
book_user_count = book_user_count.sort_values(by='item_id', ascending=True)

# 保存到 CSV 文件
book_user_count.to_csv('data/test_dataset.csv', index=False)

print(book_user_count)
