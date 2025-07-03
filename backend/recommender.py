# recommender.py
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

class BookRecommender:
    def __init__(self, train_csv):
        self.train_df = pd.read_csv(train_csv)
        self.user_book_matrix = self.train_df.groupby(['user_id', 'item_id']).size().unstack(fill_value=0)
        self.user_ids = self.user_book_matrix.index.tolist()
        self.item_ids = self.user_book_matrix.columns.tolist()

        self.user_id_to_index = {uid: idx for idx, uid in enumerate(self.user_ids)}
        self.item_id_to_index = {iid: idx for idx, iid in enumerate(self.item_ids)}
        self.index_to_item_id = {idx: iid for iid, idx in self.item_id_to_index.items()}

        self.user_sparse = csr_matrix(self.user_book_matrix.values)
        self.item_sparse = csr_matrix(self.user_book_matrix.values.T)

        self.user_model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=6)
        self.user_model.fit(self.user_sparse)

        self.item_model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=6)
        self.item_model.fit(self.item_sparse)

        self.user_distances, self.user_indices = self.user_model.kneighbors(self.user_sparse)
        self.item_distances, self.item_indices = self.item_model.kneighbors(self.item_sparse)

    def recommend_for_user(self, user_id, top_k=5):
        if user_id not in self.user_id_to_index:
            return []
        user_idx = self.user_id_to_index[user_id]
        seen_books = set(self.user_book_matrix.iloc[user_idx][self.user_book_matrix.iloc[user_idx] > 0].index)

        sim_users = self.user_indices[user_idx][1:top_k + 1]
        sim_scores = 1 - self.user_distances[user_idx][1:top_k + 1]

        candidate_books = {}
        for sim_user, score in zip(sim_users, sim_scores):
            books = self.user_book_matrix.iloc[sim_user][self.user_book_matrix.iloc[sim_user] > 0].index
            for book in books:
                if book not in seen_books:
                    candidate_books[book] = candidate_books.get(book, 0) + score

        sorted_books = sorted(candidate_books.items(), key=lambda x: x[1], reverse=True)
        return [book for book, _ in sorted_books[:top_k]]

    def similar_books(self, item_id, top_k=5):
        if item_id not in self.item_id_to_index:
            return []
        item_idx = self.item_id_to_index[item_id]
        sim_items = self.item_indices[item_idx][1:top_k + 1]
        return [self.index_to_item_id[idx] for idx in sim_items]

    def generate_all_recommendations(self, top_k=5, output_csv='data/recommend_result.csv'):
        records = []

        for user_id in self.user_ids:
            user_based_recommend = self.recommend_for_user(user_id, top_k=top_k)
            seen_books = self.user_book_matrix.loc[user_id][self.user_book_matrix.loc[user_id] > 0].index.tolist()

            book_based_recommend = set()
            for book_id in seen_books:
                book_based_recommend.update(self.similar_books(book_id, top_k=top_k))
            book_based_recommend -= set(seen_books)

            records.append({
                'user_id': user_id,
                'user_based': list(user_based_recommend),
                'item_based': list(book_based_recommend)
            })

        pd.DataFrame(records).to_csv(output_csv, index=False)

if __name__ == '__main__':
    recommender = BookRecommender('data/train_dataset.csv')
    recommender.generate_all_recommendations(top_k=5)
