import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="英単語テストアプリ")

# タイトルと説明
st.title('英単語テストアプリ')
st.write('英単語をランダムに表示して、勉強をサポートします！')

# Load the data from multiple Excel files
@st.cache
def load_data():
    part1 = pd.read_excel("リープベーシック見出語・用例リスト(Part 1).xlsx")
    part2 = pd.read_excel("リープベーシック見出語・用例リスト(Part 2).xlsx")
    part3 = pd.read_excel("リープベーシック見出語・用例リスト(Part 3).xlsx")
    part4 = pd.read_excel("リープベーシック見出語・用例リスト(Part 4).xlsx")
    return pd.concat([part1, part2, part3, part4], ignore_index=True)

words_df = load_data()

# ガチャ機能
if st.button('ガチャを引く！'):
    selected_word = words_df.sample().iloc[0]
    
    st.session_state.selected_word = selected_word
    st.session_state.display_meaning = False

if 'selected_word' in st.session_state:
    st.header(f"単語名: {st.session_state.selected_word['単語']}")
    if 'レア度' in st.session_state.selected_word:
        st.subheader(f"レア度: {st.session_state.selected_word['レア度']}")

    if st.button('意味を確認する'):
        st.session_state.display_meaning = True

    if st.session_state.display_meaning:
        st.write(f"意味: {st.session_state.selected_word['意味']}")

# テスト機能
if st.button('テストを開始する'):
    st.session_state.test_started = True
    st.session_state.correct_answers = 0
    st.session_state.current_question = 0
    st.session_state.start_time = time.time()

if 'test_started' in st.session_state and st.session_state.test_started:
    if st.session_state.current_question < 10:
        question = words_df.sample().iloc[0]
        st.session_state.current_question_data = question
        options = list(words_df['意味'].sample(3))
        options.append(question['意味'])
        np.random.shuffle(options)

        st.subheader(f"単語: {question['単語']}")
        answer = st.radio("意味を選んでください", options)

        if st.button('回答する'):
            if answer == question['意味']:
                st.session_state.correct_answers += 1
            st.session_state.current_question += 1
    else:
        st.session_state.test_started = False
        st.write(f"テスト終了！正解数: {st.session_state.correct_answers}/10")
        st.write(f"正答率: {st.session_state.correct_answers * 10}%")
else:
    if 'start_time' in st.session_state:
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = 60 - elapsed_time
        if remaining_time > 0:
            st.write(f"残り時間: {int(remaining_time)}秒")
        else:
            st.session_state.test_started = False
            st.write(f"時間切れ！正解数: {st.session_state.correct_answers}/10")
            st.write(f"正答率: {st.session_state.correct_answers * 10}%")
