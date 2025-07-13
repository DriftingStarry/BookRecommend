import pandas as pd

class RecommendationGetter:
    def __init__(self, recommend_csv='data/recommend_result.csv'):
        self.df = pd.read_csv(recommend_csv, converters={
            'user_based': eval,
            'item_based': eval
        })

    def get_user_recommendations(self, user_id):
        row = self.df[self.df['user_id'] == user_id]
        if row.empty:
            return [], []
        user_based = row.iloc[0]['user_based']
        item_based = row.iloc[0]['item_based']
        return user_based, item_based

if __name__ == "__main__":
    re = RecommendationGetter()
    u, i = re.get_user_recommendations(0)
    df = pd.DataFrame(u, i)
    print(df)