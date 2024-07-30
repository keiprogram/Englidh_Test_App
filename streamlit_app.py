import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import base64

# ページ設定をスクリプトの最初に配置
st.set_page_config(
    page_title="English Vocabulary Test",
)

# カスタムCSSを適用
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #022033;
        color: #ffae4b;
        text-align: center;
    }
    .sidebar .sidebar-content {
        background-color: #022033;
        color: #ffae4b;
    }
    .st-bd {
        background-color: #022033;
        color: #ffae4b;
        text-align: center;
    }
    .st-cd {
        background-color: #022033;
        color: #ffae4b;
        text-align: center;
    }
    .st-ec {
        color: #ffae4b;
    }
    .st-cd {
        background-color: #022033;
    }
    img {
        border-radius: 20px; /* 画像の角を丸くする */
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .stButton > button {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .stRadio > div {
        text-align: center;
    }
    h1, h2, h3, h4, h5, h6, .stMarkdown, .stText, .stSubheader {
        text-align: center;
    }
    .stRadio > div {
        display: inline-block;
        margin: 0 auto;
    }
    .stRadio label {
        display: block;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ロゴ画像の表示
def load_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_path = 'img/English.png'
image_base64 = load_image(image_path)
image_html = f'<img src="data:image/png;base64,{image_base64}" style="border-radius: 20px;">'
st.markdown(image_html, unsafe_allow_html=True)

# タイトルと説明
st.title('英単語テスト')
st.write('英単語を順に表示して、勉強をサポートします！')

# Load the data from multiple Excel files
@st.cache_data
def load_data():
    part1 = pd.read_excel("リープベーシック見出語・用例リスト(Part 1).xlsx")
    part2 = pd.read_excel("リープベーシック見出語・用例リスト(Part 2).xlsx")
    part3 = pd.read_excel("リープベーシック見出語・用例リスト(Part 3).xlsx")
    part4 = pd.read_excel("リープベーシック見出語・用例リスト(Part 4).xlsx")
    return pd.concat([part1, part2, part3, part4], ignore_index=True)

words_df = load_data()

# テスト形式選択 (トグルボタン風)
st.sidebar.title("テスト形式を選択してください")
test_type = st.sidebar.radio("", ('英語→日本語', '日本語→英語'), horizontal=True)

# 出題範囲選択
st.sidebar.title('出題範囲を選択してください')
ranges = [f"{i*100+1}-{(i+1)*100}" for i in range(14)]
selected_range = st.sidebar.selectbox("出題範囲", ranges)

# 選択された範囲に基づいてデータをフィルタリング
range_start, range_end = map(int, selected_range.split('-'))
filtered_words_df = words_df[(words_df['No.'] >= range_start) & (words_df['No.'] <= range_end)].sort_values(by='No.')

# テスト開始ボタン
if st.button('テストを開始する'):
    st.session_state.test_started = True
    st.session_state.correct_answers = 0
    st.session_state.current_question = 0
    st.session_state.finished = False
    st.session_state.wrong_answers = []

    # ランダムに50問を選択
    selected_questions = filtered_words_df.sample(50).reset_index(drop=True)
    st.session_state.selected_questions = selected_questions
    st.session_state.total_questions = len(selected_questions)

    # 最初の問題を設定
    st.session_state.current_question_data = selected_questions.iloc[st.session_state.current_question]
    if test_type == '英語→日本語':
        options = list(selected_questions['語の意味'].sample(3))
        options.append(st.session_state.current_question_data['語の意味'])
    else:
        options = list(selected_questions['単語'].sample(3))
        options.append(st.session_state.current_question_data['単語'])
    np.random.shuffle(options)
    st.session_state.options = options
    st.session_state.answer = None

# 問題更新用の関数
def update_question():
    if test_type == '英語→日本語':
        correct_answer = st.session_state.current_question_data['語の意味']
        question_word = st.session_state.current_question_data['単語']
    else:
        correct_answer = st.session_state.current_question_data['単語']
        question_word = st.session_state.current_question_data['語の意味']

    if st.session_state.answer == correct_answer:
        st.session_state.correct_answers += 1
    else:
        st.session_state.wrong_answers.append((
            st.session_state.current_question_data['No.'],
            question_word,
            correct_answer
        ))

    st.session_state.current_question += 1
    if st.session_state.current_question < st.session_state.total_questions:
        st.session_state.current_question_data = st.session_state.selected_questions.iloc[st.session_state.current_question]
        if test_type == '英語→日本語':
            options = list(st.session_state.selected_questions['語の意味'].sample(3))
            options.append(st.session_state.current_question_data['語の意味'])
        else:
            options = list(st.session_state.selected_questions['単語'].sample(3))
            options.append(st.session_state.current_question_data['単語'])
        np.random.shuffle(options)
        st.session_state.options = options
        st.session_state.answer = None
    else:
        st.session_state.finished = True

# テスト終了後の結果表示
def display_results():
    correct_answers = st.session_state.correct_answers
    total_questions = st.session_state.total_questions
    wrong_answers = [wa for wa in st.session_state.wrong_answers if wa[0] in st.session_state.selected_questions['No.'].values]
    accuracy = correct_answers / total_questions

    st.write(f"テスト終了！正解数: {correct_answers}/{total_questions}")
    st.progress(accuracy)
    
    st.write("正解数と不正解数")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("正解数", correct_answers)
    with col2:
        st.metric("不正解数", total_questions - correct_answers)

    st.write(f"正答率: {accuracy:.0%}")
    st.progress(accuracy)

    if wrong_answers:
        st.write("間違えた単語とその語の意味 (番号の小さい順):")
        # 番号の小さい順にソート
        wrong_answers.sort(key=lambda x: x[0])
        for no, word, meaning in wrong_answers:
            st.write(f"番号: {no}, 単語: {word}, 語の意味: {meaning}")

# テストが開始された場合の処理
if 'test_started' in st.session_state and st.session_state.test_started:
    if st.session_state.current_question < st.session_state.total_questions:
        if test_type == '英語→日本語':
            st.subheader(f"単語: {st.session_state.current_question_data['単語']}")
        else:
            st.subheader(f"語の意味: {st.session_state.current_question_data['語の意味']}")
        st.radio("選択してください", st.session_state.options, key='answer', on_change=update_question)
    else:
        display_results()
else:
    if 'test_started' in st.session_state and st.session_state.finished:
        display_results()
