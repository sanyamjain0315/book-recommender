import streamlit as st
import pandas as pd
import pickle
import numpy as np
import re


def recommend(book_name):
    # index fetch
    try:
        # Loading important variables and files
        pt = pickle.load(open('recommender_pickle_files\\pt.pkl','rb'))
        books = pickle.load(open('recommender_pickle_files\\books.pkl','rb'))
        similarity_scores = pickle.load(open('recommender_pickle_files\\similarity_scores.pkl','rb'))
        
        index = np.where(pt.index==book_name)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:5]
    
        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            
            data.append(item)
        return data
    except:
        return

if __name__=="__main__":
    st.title("GreatReads")
    user_input = st.text_input("Enter a movie you like")
    recommendations = recommend(user_input)
    if st.button("Recommend"):
        if not recommendations:
            st.text("Apologies, we could not find \"{user_input}\" in our system")
        else:
            st.subheader("For you")
            
            n_books = len(recommendations)
            n_cols = 3
            n_rows = int((1 + n_books // n_cols) * 3)
            rows = [st.columns(n_cols) for _ in range(n_rows)]
            cols = [column for row in rows for column in row]

            columns_order = []
            for i in range(0, len(recommendations), 3):
                for j in range(3):
                    columns_order.append(recommendations[i][j])
                    columns_order.append(recommendations[i+1][j]) if i+1 < len(recommendations) else columns_order.append('')
                    columns_order.append(recommendations[i+2][j]) if i+2 < len(recommendations) else columns_order.append('')
            
            for col, item in zip(cols, columns_order):
                if re.match(r'https?://\S+', item) is not None:
                    # col.text(item)
                    col.image(item, use_column_width="always")
                else:
                    col.text(item)