import pandas as pd
import numpy as np
import streamlit as st

books = pd.read_csv('books.csv')[['book_id', 'title', 'authors']]
ratings = pd.read_csv('ratings.csv')

# Create dataframe as user_id -1 with my ratings
my_user_id = -1
user_input = st.text_area(label='Enter book name followed by a space and your rating. One entry per line. Minimum 10 entries.', placeholder='Frankenstein 4\nThe Great Gatsby 5\nThe Catcher in the Rye 4')
top_n = st.text_input(label='I want the top __ recommendations:', placeholder='10')
enter_button = st.button(label="Generate!")

if enter_button:
    user_input = user_input.split('\n')
    num_entries = sum(1 for line in user_input)

    my_ratings = []
    if num_entries > 1:
        for block in user_input:
            title = str(block[:-2])
            rating = int(block[-1])
            my_ratings.append([title, rating])
    else:
        st.warning('Please enter your book ratings!')

    my_ratings = pd.DataFrame(my_ratings, columns=['title', 'rating'])
    st.write('Your ratings:')
    st.dataframe(my_ratings, use_container_width=True)

    my_ratings['user_id'] = my_user_id

    # Add additional info (book_id, authors) from books to my_ratings df based on title
    my_ratings = pd.merge(my_ratings, books, on='title', how='left')

    # Append necessary columns from my ratings to ratings
    ratings = ratings._append(my_ratings[['user_id', 'book_id', 'rating']], ignore_index=True)

    # Merge ratings with book titles
    ratings = ratings.merge(books[['book_id', 'title']], how='left', on='book_id').dropna()

    # Create user-item-interaction matrix
    with st.spinner('Generating user-item-interaction matrix...'):
        matrix = ratings.pivot_table(
            index=['user_id'],
            columns=['title'],
            values='rating').fillna(np.nan)

    st.write('User-item-interaction matrix of the first 10 users:')
    st.table(matrix.head(10))

    # Ensure similarities are high-quality - 'similar' users must have at least 10 similar books
    min_common_ratings = num_entries // 4
    is_my_rated_books = matrix.loc[my_user_id].notna()

    # Calculate correlation coefficient between my_user_id's ratings and each user_id's ratings
    similarities = matrix.corrwith(matrix.loc[my_user_id], axis=1)

    st.write('Correlation matrix of your book ratings against the ratings of the first 10 users (None means your books are not similar enough):')
    st.dataframe(similarities.head(10), use_container_width=True)

    common_ratings_count = (matrix.notna() & is_my_rated_books).sum(axis=1)

    similarities[common_ratings_count < min_common_ratings] = np.nan
    similarities.loc[my_user_id] = np.nan

    # Use collaborative filtering to provide rating weights depending on user similarity scores
    min_similarity = 0.5 if num_entries < 15 else 0.7
    min_num_ratings = 10

    def calculate_weighted_rating(user_ratings, similarities):
        """
        Calculate weighted average rating for each book based on user similarities.
        """
        neighbors = similarities > min_similarity

        # Ensure proper dot product calculation
        valid_indices = neighbors & user_ratings.notna() & similarities.notna()

        weighted_sum = np.dot(user_ratings[valid_indices], similarities[valid_indices])
        total_weight = np.sum(similarities[valid_indices])

        predicted_rating = weighted_sum / total_weight if total_weight != 0 else np.nan

        # Ensure sufficient ratings
        if user_ratings[valid_indices].notna().sum() <= min_num_ratings:
            predicted_rating = np.nan

        return predicted_rating

    predicted_scores = {}
    for book in matrix.columns:
        user_ratings = matrix[book]
        predicted_scores[book] = calculate_weighted_rating(user_ratings, similarities)

    predicted_scores = pd.Series(predicted_scores)
    predicted_scores = predicted_scores.dropna()

    st.write('Here are our recommendations with rating predictions for you!')
    st.dataframe(predicted_scores[~is_my_rated_books].sort_values(ascending=False).head(int(top_n)), use_container_width=True)
