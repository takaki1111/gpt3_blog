import streamlit as st
from streamlit_chat import message
import requests
import datetime
import openai

API_KEY=st.secrets.OpenAI.API_KEY
openai.api_key = API_KEY

def text_summary(prompt,sum_str):
    # 分析の実施
    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    temperature=0.8,
    max_tokens=sum_str,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    #stop=["あなた:", "高橋:"]
    )

    # 分析結果の出力
    return response["choices"][0]["text"].replace('\n','')

prompt="Blog\nTitle:1\
\ntags:2\
\nSection:3\
\nFull text:"



st.header("ブログ記事ライティング")
title = st.text_input("ブログ記事のタイトル","") 
tags = st.text_input("見出し記事のタグ(含めたいキーワード)","") 
section = st.text_input("記事の見出し名","") 
sum_str =st.slider("生成する文字数", 0, 3000, 1000, 1)
if title and tags and section:
    prompt_input = prompt.translate(str.maketrans({'1': title, '2': tags,'3': section}))
    return_sent = text_summary(prompt_input,sum_str)

    st.text_area("見出し記事本文",return_sent, height=700,max_chars=3500)