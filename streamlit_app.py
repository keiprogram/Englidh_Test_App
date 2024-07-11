import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="英単語テストアプリ")

# タイトルと説明
st.title('英単語テストアプリ')
st.write('英単語を順に表示して、勉強をサポートします！')

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
filtered_words_df = words_df[(words_df['No.'] >= range_start) & (words_df['No.'] <= range_end)].sort_values(by='No.')

# テスト機能
if st.button('テストを開始する'):
    st.session_state.test_started = True
    st.session_state.correct_answers = 0
    st.session_state.wrong_answers = []
    st.session_state.current_question = 0
    st.session_state.start_time = time.time()
    
    st.write("テストが始まりました。")
    st.write("100問のテストです。全ての問題に回答してください。")

if 'test_started' in st.session_state and st.session_state.test_started:
    if st.session_state.current_question < 100:
        question = filtered_words_df.iloc[st.session_state.current_question]
        st.session_state.current_question_data = question

        # 選択肢を作成
        options = list(filtered_words_df['語の意味'].sample(3))
        options.append(question['語の意味'])
        np.random.shuffle(options)

        st.subheader(f"単語: {question['単語']}")
        answer = st.radio("語の意味を選んでください", options)

        if st.button('回答する'):
            if answer == question['語の意味']:
                st.session_state.correct_answers += 1
            else:
                st.session_state.wrong_answers.append((question['単語'], question['語の意味']))
            st.session_state.current_question += 1
            st.experimental_rerun()  # ページをリフレッシュして次の問題を表示
    else:
        st.session_state.test_started = False
        st.write(f"テスト終了！正解数: {st.session_state.correct_answers}/100")
        st.write(f"正答率: {st.session_state.correct_answers}%")
        
        if st.session_state.wrong_answers:
            st.write("間違えた単語とその意味:")
            for word, meaning in st.session_state.wrong_answers:
                st.write(f"単語: {word}, 語の意味: {meaning}")
