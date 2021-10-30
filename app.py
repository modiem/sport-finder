import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# variables
choice_1 = 1

@st.cache
def get_df():
    df = pd.read_csv('data/skills.csv').set_index("Sport")
    questions = pd.read_csv("data/question.csv")
    return df, questions

df, questions = get_df()

# st.write(df.head())


page = st.radio(
    "Do you exercise regularly?",
    (" ", "Yes", "No")
)

if page == "Yes":
    choice_1 = st.radio(
        "Are you interested in having a new buddy?",
        (" ", "Yes", "No")
    )

if choice_1 == "Yes":
    st.subheader(
        "Bob is looking for a new buddy to do what you are doing! Chat him up now and get a discount for your next subscription!"
    )

if page == "No":
    st.header("Now is the time to find a sport for you!")
    arr = []
    for col in df.columns:
        question = questions[questions['factor'] == col]['question'].values[0]
        st.subheader(question)
        a = st.slider(" ",1, 10, value = np.random.randint(3, 10),key = col)

        arr.append(a)

    arr = np.array(arr).reshape(1,-1)
    dic = {"fitted": cosine_similarity(df, arr).reshape(-1)}
    result = pd.DataFrame(dic, index = df.index, columns=["fitted"]).sort_values(by=["fitted"], ascending=False)

    st.write(result.head(3))
