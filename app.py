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

mh1 = '①記事本文生成[記事のタイトル + タグ + 記事の見出し名]'
mh2 = '②記事本文生成[記事のタイトル + イントロ + 記事の見出し名 + 見出しの冒頭文章]'
mh3 = '③文章の要約'


genre = st.radio(
     "以下の3つから行いたい文章生成のタスクを選んでください。",
     (mh1,mh2,mh3))

if genre == mh1:

    title = st.text_input("ブログ記事のタイトル","") 
    tags = st.text_input("見出し記事のタグ(含めたいキーワード)","") 
    section = st.text_input("記事の見出し名","")
    sum_str =st.slider("生成する最大文字数", 0, 3000, 1000, 1)
    temperature = st.slider("出現させる単語のランダム性", 0.0, 2.0, 0.80, 0.05)
    ini_text = ""
    prompt = "Blog\nTitle:X\ntags:Y\nSection:Z\nFull text:"
    prompt_input = prompt.translate(str.maketrans({'X': title, 'Y': tags,'Z': section}))
    button_name = '記事本文を生成させる'
    if st.button(button_name):
            full_text = make_sentence(prompt_input,sum_str,temperature)
            #full_text = ini_text + full_text
            st.text_area(label='記事本文', value=full_text, height=700,max_chars=3500)

    

elif genre == mh2:

    title = st.text_input("ブログ記事のタイトル","") 
    #intr = st.text_input("記事のイントロ(導入文)を2～3行程度","") 
    intr = st.text_area(label="記事のイントロ(導入文)を2～3行程度",height=50) 
    section = st.text_input("記事の見出し名","")
    #sec_sentc = st.text_input("見出しの冒頭文章(2～3行くらいの文量)","")
    sec_sentc = st.text_area(label="見出しの冒頭文章(2～3行くらいの文量)",height=50)
    sum_str =st.slider("生成する最大文字数", 0, 3000, 1000, 1)    
    temperature = st.slider("出現させる単語のランダム性", 0.0, 2.0, 0.80, 0.05)
    ini_text = sec_sentc
    prompt = "Blog\nTitle:X\nIntro:Y\nSection:Z\nFull text:R"
    prompt_input = prompt.translate(str.maketrans({'X': title, 'Y': intr,'Z': section,'R': sec_sentc}))
    button_name = '記事本文を生成させる'
    if st.button(button_name):
            full_text = make_sentence(prompt_input,sum_str,temperature)
            #full_text = ini_text + full_text
            st.text_area(label='記事本文', value=full_text, height=700,max_chars=3500)

    

else:
    input_text = st.text_area(label="要約する元のテキスト",height=300,max_chars=3000) 
    sum_str =st.slider("生成する最大文字数", 0, 3000, 1000, 1)    
    temperature = st.slider("出現させる単語のランダム性", 0.0, 2.0, 0.80, 0.05)
    point = st.slider("要約で得たい文章の数", 1, 7, 3, 1)

    prompt ='''tl;dr:ポイントは以下のXXX点です。'''
    prompt = prompt.replace('XXX',str(point))
    input_text = input_text.replace('\n','')
    prompt_input = input_text + prompt
    button_name = '文章を要約する'

        
    if st.button(button_name):
        full_text = make_sentence(prompt_input,sum_str,temperature)
        #full_text = ini_text + full_text
        st.text_area(label='要約文', value=full_text, height=700,max_chars=3500)

