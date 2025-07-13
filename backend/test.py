import pandas as pd
import ast

# 1. 读数据
rec_df = pd.read_csv("data/recommend_result.csv")
rec_df["user_based"]  = rec_df["user_based"].apply(ast.literal_eval)
rec_df["item_based"]  = rec_df["item_based"].apply(ast.literal_eval)

# 2. 取每个 user 的第一本书
rec_df["first_user_based"]  = rec_df["user_based"].apply(lambda x: x[0] if x else None)
rec_df["first_item_based"]  = rec_df["item_based"].apply(lambda x: x[0] if x else None)

# 3. 只保留需要的列
rec_df = rec_df[["user_id", "first_user_based", "first_item_based"]]

# 4. 读 test_dataset.csv（只含 user_id 列）
test_df = pd.read_csv("data/test_dataset.csv")[["user_id"]]

# 5. 用 merge 把两表拼接起来（左连接，确保顺序与 test_df 一致）
test_df = pd.merge(test_df, rec_df, on="user_id", how="left")

# 6. 最终 test_df 包含三列：user_id, first_user_based, first_item_based
test_df.to_csv(r"data/test_df.csv", index=False)