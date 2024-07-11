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

# 出題範囲選択
st.sidebar.title('出題範囲を選択してください')
ranges = [f"{i*100+1}-{(i+1)*100}" for i in range(14)]
selected_range = st.sidebar.selectbox("出題範囲", ranges)

# 選択された範囲に基づいてデータをフィルタリング
range_start, range_end = map(int, selected_range.split('-'))
filtered_words_df = words_df[(words_df['No.'] >= range_start) & (words_df['No.'] <= range_end)]

# テスト機能
if st.button('テストを開始する'):
    st.session_state.test_started = True
    st.session_state.correct_answers = 0
    st.session_state.wrong_answers = 0
    st.session_state.current_question = 0
    st.session_state.start_time = time.time()
    
    st.write("テストが始まりました。")
    st.write("60秒間でできるだけ多くの問題に回答してください。")
    st.write("残り時間は以下のように表示されます。")

if 'test_started' in st.session_state and st.session_state.test_started:
    if st.session_state.current_question < 10:
        question = filtered_words_df.sample().iloc[0]
        st.session_state.current_question_data = question
        options = list(filtered_words_df['語の意味'].sample(3))
        options.append(question['語の意味'])
        np.random.shuffle(options)

        st.subheader(f"単語: {question['単語']}")
        answer = st.radio("語の意味を選んでください", options)

        if st.button('回答する'):
            if answer == question['語の意味']:
                st.session_state.correct_answers += 1
            else:
                st.session_state.wrong_answers += 1
            st.session_state.current_question += 1
    else:
        st.session_state.test_started = False
        st.write(f"テスト終了！正解数: {st.session_state.correct_answers}/10")
        st.write(f"間違えた問題数: {st.session_state.wrong_answers}/10")
        st.write(f"正答率: {st.session_state.correct_answers * 10}%")
else:
    if 'start_time' in st.session_state:
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = 60 - elapsed_time
        if remaining_time > 0:
            st.write(f"残り時間: {int(remaining_time)}秒")
            st.progress(elapsed_time / 60.0)  # タイマーの進行状況バーを表示
        else:
            st.session_state.test_started = False
            st.write(f"時間切れ！正解数: {st.session_state.correct_answers}/10")
            st.write(f"間違えた問題数: {st.session_state.wrong_answers}/10")
            st.write(f"正答率: {st.session_state.correct_answers * 10}%")
