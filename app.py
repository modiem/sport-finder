import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from bs4 import BeautifulSoup
import urllib
import regex as re
import requests
import urllib.request
from PIL import Image
from io import BytesIO

def get_main_wiki_image(title):
    person_url = []
    urlpage =  'https://en.wikipedia.org/wiki/' + title
    # query the website and return the html to the variable 'page'
    page = requests.get(urlpage).text
    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')
    for raw_img in soup.find_all('img'):
        link = raw_img.get('src')
    # The first image on the page with the URL strucutre below is usually 
    # the image inside the infobox. We exlcude any .svg images, as they are 
    # vector graphics common to all Wikipedia pages
        if re.search('wikipedia/.*/thumb/', link) and not re.search('.svg', link):
            person_url = "http:" + link
            # Once the first image has been found, we break out of the loop and search the next page
            break
    return person_url

# variables
choice_1 = 1

@st.cache
def get_df():
    df = pd.read_csv('data/skills.csv').set_index("Sport")
    questions = pd.read_csv("data/question.csv")
    return df, questions

df, questions = get_df()

st.title("Sport for Everyone! 🧞")
st.markdown("""---""")


st.sidebar.markdown('''
    <h3 style="font-size=24px;">Do you exercise regularly? </h3>
    ''', unsafe_allow_html=True)
page = st.sidebar.radio(
    "",
    ("Make a choice", "Yes", "No"),
    key = 1
)

if page == "Yes":
    st.markdown('''
    <h3 style="font-size=24px;">Are you interested in having a new buddy?</h3>
    ''', unsafe_allow_html=True)
    choice_1 = st.radio(
        "",
        ("Make a choice", "Yes", "No"),
        key = 2
    )

if choice_1 == "Yes":
    st.markdown('''
        <h4 style="text-align: center">Bob is looking for a new buddy to do what you are doing! Chat him up now and get a discount on your next subscription!</h4>
    ''', unsafe_allow_html=True)
if choice_1 == "No":
    st.markdown('''
        <h4 style="text-align: center">What a pity! You can always change this in the settings later if you change your mind.</h4>
    ''', unsafe_allow_html=True)
    

if page == "No":
    st.markdown('''
        <h3 style="text-align: center">Now it's time to find you a perfect sport!</h3>
    ''', unsafe_allow_html=True)
    st.markdown("""---""")
    arr = []
    for col in df.columns:
        question = questions[questions['factor'] == col]['question'].values[0]
        st.subheader(f"{col}: {question}")
        a = st.slider(" ",1, 10, 1,key = col)

        arr.append(a)

    arr = np.array(arr).reshape(1,-1)
    dic = {"fitted": cosine_similarity(df, arr).reshape(-1)}
    result = pd.DataFrame(dic, index = df.index, columns=["fitted"]).sort_values(by=["fitted"], ascending=False)



    for i in range(3):
        st.info(f"{result.iloc[i].name} is your No.{i+1} match.")
        img = get_main_wiki_image(result.iloc[i].name)
        if len(img) > 0:
            try:
                response = requests.get(img)
                img = Image.open(BytesIO(response.content))
                st.image(img, width = 300)
            except:
                pass
