import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

st.title("Find your Sport!")

@st.cache
def get_df():
    df = pd.read_excel('data/new skill.xlsx') 
    return df.set_index("Sport")

df = get_df()



arr = []
for i in range(14):
    st.subheader(f'Question No.{i+1}')
    a = st.slider(" ",1, 10, value = np.random.randint(3, 10),key = i)

    arr.append(a)

arr = np.array(arr).reshape(1,-1)
dic = {"fitted": cosine_similarity(df, arr).reshape(-1)}
result = pd.DataFrame(dic, index = df.index, columns=["fitted"]).sort_values(by=["fitted"], ascending=False)

st.write(result.head(3))

