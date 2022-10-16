import streamlit as st
from streamlit_chat import message
import requests
import datetime
import openai


API_KEY=st.secrets.OpenAI.API_KEY
openai.api_key = API_KEY

def make_sentence(prompt,sum_str,temperature):
    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    temperature=temperature,
    max_tokens=sum_str,
    top_p=1.0,
    frequency_penalty=0.5,
    presence_penalty=0.0,
    )

    # 分析結果の出力
    return response["choices"][0]["text"].replace('\n','')

st.header("ブログ記事ライティング")

mh1 = '記事のタイトル + タグ + 記事の見出し名'
mh2 = '記事のタイトル + イントロ + 記事の見出し名 + 見出しの冒頭文章'

genre = st.radio(
     "以下の2つから見出し記事本文の生成方法を選んでください。",
     (mh1, mh2))

if genre == mh1:

    title = st.text_input("ブログ記事のタイトル","") 
    tags = st.text_input("見出し記事のタグ(含めたいキーワード)","") 
    section = st.text_input("記事の見出し名","")
    sum_str =st.slider("生成する最大文字数", 0, 3000, 1000, 1)
    temperature = st.slider("出現させる単語のランダム性", 0.0, 2.0, 0.80, 0.05)
    ini_text = ""
    prompt = "Blog\nTitle:X\ntags:Y\nSection:Z\nFull text:"
    prompt_input = prompt.translate(str.maketrans({'X': title, 'Y': tags,'Z': section}))

    

else:

    title = st.text_input("ブログ記事のタイトル","") 
    intr = st.text_input("記事のイントロ(導入文)を2～3行程度","") 
    section = st.text_input("記事の見出し名","")
    sec_sentc = st.text_input("見出しの冒頭文章(2～3行くらいの文量)","")
    sum_str =st.slider("生成する最大文字数", 0, 3000, 1000, 1)    
    temperature = st.slider("出現させる単語のランダム性", 0.0, 2.0, 0.80, 0.05)
    ini_text = sec_sentc
    prompt = "Blog\nTitle:X\nIntro:Y\nSection:Z\nFull text:R"
    prompt_input = prompt.translate(str.maketrans({'X': title, 'Y': intr,'Z': section,'R': sec_sentc}))




if st.button('見出し記事本文生成'):
    full_text = make_sentence(prompt_input,sum_str,temperature)
    full_text = ini_text + full_text
    st.text_area(label='見出し記事本文', value=full_text, height=700,max_chars=3500)
else:
    st.text_area(label='見出し記事本文', value="", height=700,max_chars=3500)

