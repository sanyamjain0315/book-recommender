import streamlit as st
import pandas as pd
import pickle
import numpy as np


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
            col1, col2, col3 = st.columns(3)
            for book in recommendations:
                with col1:
                    st.image(book[2], caption=book[0])
                with col2:
                    st.write(book[0])
                with col3:
                    st.write(book[1])