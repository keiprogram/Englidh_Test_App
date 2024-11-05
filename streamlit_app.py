import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import base64

st.set_page_config(page_title="English Vocabulary Test", page_icon='img/English_fabikon.png')

# スタイル設定
st.markdown(
    """
    <style>
    .reportview-container, .sidebar .sidebar-content {
        background-color: #022033;
        color: #ffae4b;
    }
    .stButton > button, .choice-button {
        background-color: #ffae4b;
        color: #022033;
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .stButton > button:hover, .choice-button:hover {
        background-color: #ffd17f;
    }
    .choices-container, .header-container, .button-container, .results-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 20px;
    }
    .results-table {
        border-collapse: collapse;
        width: 100%;
    }
    .results-table th, .results-table td {
        border: 1px solid #ffae4b;
        padding: 8px;
        text-align: center;
    }
    .results-table th {
        background-color: #022033;
        color: #ffae4b;
    }
    .results-table tr:nth-child(even) {
        background-color: #e3e3e3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 画像読み込み関数
def load_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_path = 'img/English.png'
image_base64 = load_image(image_path)
image_html = f'<img src="data:image/png;base64,{image_base64}" style="border-radius: 20px; width: 500px;">'

st.markdown('<div class="header-container">', unsafe_allow_html=True)
st.markdown(image_html, unsafe_allow_html=True)
st.title('英単語テスト')
st.write('英単語を順に表示して、勉強をサポートします！')
st.markdown('</div>', unsafe_allow_html=True)

# データ読み込み関数
@st.cache_data
def load_data():
    leap_parts = [pd.read_excel(f"リープベーシック見出語・用例リスト(Part {i}).xlsx") for i in range(1, 5)]
    leap_data = pd.concat(leap_parts, ignore_index=True)
    system_data = pd.read_excel("/mnt/data/シスタン.xlsx")
    return leap_data, system_data

leap_words_df, system_words_df = load_data()

# サイドバー設定
st.sidebar.title("テスト形式を選択してください")
test_type = st.sidebar.radio("", ('英語→日本語', '日本語→英語'), horizontal=True)

st.sidebar.title('単語帳を選択してください')
word_list = st.sidebar.radio("単語帳", ("LEAP Basic英単語帳", "システム英単語"))

# 単語帳の選択に応じてデータと範囲を設定
if word_list == "LEAP Basic英単語帳":
    words_df = leap_words_df
    ranges = [f"{i*100+1}-{(i+1)*100}" for i in range(14)]  # LEAP Basicの範囲
else:
    words_df = system_words_df
    ranges = [f"{i*100+1}-{(i+1)*100}" for i in range(len(words_df) // 100 + 1)]  # システム英単語の範囲

st.sidebar.title('出題範囲を選択してください')
selected_range = st.sidebar.selectbox("出題範囲", ranges)

# サイドバーで出題数を選択するスライダーを追加
st.sidebar.title('出題数を選択してください')
num_questions = st.sidebar.slider('出題数', min_value=1, max_value=50, value=10)

range_start, range_end = map(int, selected_range.split('-'))
filtered_words_df = words_df[(words_df['No.'] >= range_start) & (words_df['No.'] <= range_end)].sort_values(by='No.')

# 以下、テスト開始の処理や結果表示の処理などのコードが続きます
# (上記までの修正に合わせてデータロードやUIの設定を調整してください)
