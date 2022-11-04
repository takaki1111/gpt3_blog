import streamlit as st
from streamlit_chat import message
import requests
import datetime
import openai
import yaml


with open('config.yaml', 'r') as yml:
    config = yaml.safe_load(yml)


intr_dir = config['intr']

sec_sentc_dir = config['sec_sentc']

summery_text_dir = config['summery_text']

seo_prompt_dir = config['seo_prompt']


with open(intr_dir, "r", encoding="utf-8") as f:
     intr = f.read()

with open(sec_sentc_dir, "r", encoding="utf-8") as f:
     sec_sentc = f.read()
sec_sentc = sec_sentc.replace('\n','')

with open(summery_text_dir, "r", encoding="utf-8") as f:
     summery_text = f.read()
summery_text = summery_text.replace('\n','')

with open(seo_prompt_dir, "r", encoding="utf-8") as f:
     seo_prompt = f.read()

API_KEY=st.secrets.OpenAI.API_KEY
openai.api_key = API_KEY

def make_sentence(prompt,sum_str,temperature):
    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    temperature=temperature,
    max_tokens=sum_str,
    top_p=1.0,
    frequency_penalty=0.86,
    presence_penalty=0.71,
    )

    # 分析結果の出力
    return response["choices"][0]["text"].replace('\n','')

st.header("ブログ記事ライティング")

mh1 = '①記事本文生成[記事のタイトル + タグ + 記事の見出し名]'
mh2 = '②記事本文生成[記事のタイトル + イントロ + 記事の見出し名 + 見出しの冒頭文章]'
mh3 = '③文章の要約'
mh4 = '④SEOテキスト(エリア情報)の生成'
mh5 = '⑤感情分析'


genre = st.radio(
     "以下の5つから行いたい文章生成のタスクを選んでください。",
     (mh1,mh2,mh3,mh4,mh5))

if genre == mh1:

    title = st.text_input("ブログ記事のタイトル","",placeholder="例)マーケティングに活かせる「行動経済学」のススメ") 
    tags = st.text_input("見出し記事のタグ(含めたいキーワード)","",placeholder="例)行動経済学、フレーム、バイアス、ナッジ") 
    section = st.text_input("記事の見出し名","",placeholder="例)「行動経済学」とはいったい何か")
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

    title = st.text_input("ブログ記事のタイトル","",placeholder="例)福利厚生でネイル体験") 
    #intr = st.text_input("記事のイントロ(導入文)を2～3行程度","") 
    intr = st.text_area(label="記事のイントロ(導入文)を2～3行程度",height=50,placeholder=intr) 
    section = st.text_input("記事の見出し名","",placeholder = "例)社内の福利厚生ネイル")
    #sec_sentc = st.text_input("見出しの冒頭文章(2～3行くらいの文量)","")
    sec_sentc = st.text_area(label="見出しの冒頭文章(2～3行くらいの文量)",height=50,placeholder=sec_sentc)
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

    

elif genre == mh3:
    input_text = st.text_area(label="要約する元のテキスト",height=500,max_chars=3000,placeholder=summery_text) 
    sum_str =st.slider("生成する最大文字数", 0, 3000, 1000, 1)    
    temperature = st.slider("出現させる単語のランダム性", 0.0, 2.0, 0.80, 0.05)
    point = st.slider("要約で得たい文章の数", 1, 7, 3, 1)

    prompt ='''tl;dr:ポイントは以下のXXX点です。'''
    prompt = prompt.replace('XXX',str(point))
    input_text = input_text.replace('\n','')
    prompt_input = input_text + prompt
    button_name = '文章を要約する'

elif genre == mh4:
     pref = st.selectbox('都道府県を以下から選んでください',
                         ('東京','大阪', '神奈川県', '福岡県','富山県','宮城県'))
     sum_str =st.slider("生成する最大文字数", 0, 3000, 1000, 1)    
     temperature = st.slider("出現させる単語のランダム性", 0.0, 2.0, 0.50, 0.05)
     num_seo_txt = st.slider("生成するSEOテキストの数", 1, 5, 3, 1)    

     ini_text = sec_sentc
     prompt = "Blog\nTitle:自分らしく大阪を旅する♪観光ポイント＆エリアの特徴を紹介！\ntags:XXX\nSection:XXXってこんなところ！\nFull text:XXXは"
     prompt = prompt.replace('XXX', pref)
     prompt_input = seo_prompt + prompt
     button_name = 'SEOテキストを生成させる'

     if st.button(button_name):
          for i in range(num_seo_txt):
               full_text = make_sentence(prompt_input,sum_str,temperature)
               seo_text = pref + "は" + full_text
               st.text_area(label='SEOテキスト'+str(i+1), value=seo_text, height=300,max_chars=3500)

elif genre == mh5:
     senti_sent = st.text_input("感情分析を行う文章","",placeholder="例)今日転んで痛かった") 
     #sum_str =st.slider("生成する最大文字数", 0, 3000, 1000, 1)    
     #temperature = st.slider("出現させる単語のランダム性", 0.0, 2.0, 0.70, 0.05)
     prompt="次のコメントを感情分析します。\nコメント:いいね\n感情:ポジティブ\nコメント:いまいち\n感情:ネガティブ\nコメント:まずまず\n感情:ニュートラル\nコメント:XXX\n感情:"
     prompt = prompt.replace('XXX', senti_sent)
     prompt_input = prompt
     button_name = '感情分析を行う'

     if st.button(button_name):
          full_text = make_sentence(prompt_input,sum_str=sum_str =100,temperature=0.7)
          st.text_input("感情分析の結果",full_text) 
