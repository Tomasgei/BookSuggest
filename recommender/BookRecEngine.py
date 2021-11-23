import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from . models import Book


class BookSuggestionEngine():

    def __init__(self,book_name):
        self.book_name = book_name
        self.books = "recommender/BX-Books.csv"
        self.ratings = "recommender/BX-Book-Ratings.csv"


    def prepare_data(self):
        df_books = pd.read_csv(
            self.books,
            encoding = "ISO-8859-1",
            sep=";",
            header=0,
            names=['isbn', 'title', 'author'],
            usecols=['isbn', 'title', 'author'],
            dtype={'isbn': 'str', 'title': 'str', 'author': 'str'})

        df_ratings = pd.read_csv(
            self.ratings,
            encoding = "ISO-8859-1",
            sep=";",
            header=0,
            names=['user', 'isbn', 'rating'],
            usecols=['user', 'isbn', 'rating'],
            dtype={'user': 'int32', 'isbn': 'str', 'rating': 'float32'})

        df_cleaned_ratings = df_ratings[df_ratings.rating != 0]
    
        #select users which gives more than x ratings
        rating_treshold = 30
        # mask
        valid_users = df_cleaned_ratings["user"].value_counts() >= rating_treshold
        
        # Create index for DataFrame from valid users
        # Construct dataset with valid users which gives more than 100 ratings
        # Merge Books and Ratings df to get clean data
        user_index = valid_users[valid_users].index
        df_cleaned_ratings = df_cleaned_ratings[df_cleaned_ratings["user"].isin(user_index)]
        clean_dataset = df_cleaned_ratings.merge(df_books, on="isbn")
        
        # get rating counts for every title from all valid users and reset index
        # rename rating columns to rating counts
        # get DataFrame with rating counts for every Book
        # get books with more than x rating counts
        # drop duplicate rating by same user
        count_rating = clean_dataset.groupby('title')['rating'].count().reset_index()
        count_rating.rename(columns={"rating":"rating_counts"}, inplace=True)
        final_dataset = count_rating.merge(clean_dataset, on="title")
        mask_ratings = final_dataset["rating_counts"] >= 10
        final_dataset = final_dataset[mask_ratings].reset_index(drop=True)
        final_dataset.drop_duplicates(["user","title"])

        # contruct pivot table for recommendation engine
        pivot = final_dataset.pivot_table(index="title",columns="user",values="rating")
        pivot.fillna(0,inplace=True)
 
        book_titles = pivot.index.tolist()
        row_index = book_titles.index(self.book_name)
        
        book_sparse = csr_matrix(pivot)
        model = NearestNeighbors(metric = 'cosine', algorithm='auto',n_neighbors=5)
        model.fit(book_sparse)
        distances, suggestions = model.kneighbors(pivot.iloc[row_index, :].values.reshape(1, -1))
        book_titles = []
        for i in range(len(suggestions)):
            book_titles.append(pivot.index[suggestions[i]])
            print(pivot.index[suggestions[i]])
        
        return book_titles



     

     

"""
if __name__ == '__main__':
    like_book_1 = 'Dark Justice' ## méně než 10 hodnocení
    like_book_2 = "Where the Heart Is (Oprah's Book Club (Paperback))"
    like_book_3 = 'The Queen of the Damned (Vampire Chronicles (Paperback))'
    like_book_4 = 'The Fellowship of The Ring (the lord of the rings, part 1)'
    like_book_5 = "The Fellowship of the Ring (The Lord of the Rings, Part 1)"
    like_book_6 =  "Harry Potter and the Sorcerer's Stone (Book 1)"

    a = BookSuggestionEngine(like_book_2)
    print(a)
    b = a.prepare_data()
    print(b)
    c = a.book_suggestions(b)
    print(c)
"""
if __name__ == '__main__':
    qs = Book.objects.all()
    df = qs.to_dataframe()
    print(df.head())
