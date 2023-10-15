import streamlit as st
import pandas as pd

if __name__=="__main__":
    # Reading the ranked recomendations
    top_ten_ranked = pd.read_csv('user_recommendations.csv')

    # Geting the list of users
    user_ids = top_ten_ranked['User-ID'].unique()

    st.title("Book recommender")
    user = st.select_slider("Pick a user",user_ids)
    recommendations = top_ten_ranked.loc[top_ten_ranked['User-ID'] == user]['Title']
    if st.button("Recommend"):
        st.table(recommendations)
        