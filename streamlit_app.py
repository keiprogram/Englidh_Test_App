import streamlit as st
import pandas as pd
import time

# ページ設定
st.set_page_config(page_title="Vocabulary Test App", layout="wide")

# Excelファイルからデータを読み込み
excel_file = '/mnt/data/リープベーシック見出語・用例リスト(Part 1).xlsx'
df = pd.read_excel(excel_file)

# 単語とその意味をリストに格納
words = df['単語'].tolist()
meanings = df['意味'].tolist()

# 単語と意味のペアを辞書にする
word_dict = dict(zip(words, meanings))

# タイトルを設定
st.title('Vocabulary Test App')

# テストの説明
st.write("5分間でできるだけ多くの単語の意味を回答してください。")

# テスト開始ボタン
if st.button('テストを開始する'):
    st.session_state['start'] = True
    st.session_state['current_index'] = 0
    st.session_state['correct_answers'] = 0
    st.session_state['start_time'] = time.time()

# テストの実施
if 'start' in st.session_state and st.session_state['start']:
    current_time = time.time()
    elapsed_time = current_time - st.session_state['start_time']
    remaining_time = 300 - elapsed_time  # 5分（300秒）からの残り時間

    if remaining_time > 0:
        st.write(f"残り時間: {int(remaining_time)}秒")
        current_word = words[st.session_state['current_index']]
        user_answer = st.text_input(f"意味を入力してください: {current_word}")

        if st.button('次へ'):
            if user_answer == word_dict[current_word]:
                st.session_state['correct_answers'] += 1
            st.session_state['current_index'] += 1
            if st.session_state['current_index'] >= len(words):
                st.session_state['current_index'] = 0  # ループする
    else:
        st.session_state['start'] = False
        st.write(f"テスト終了！正解数: {st.session_state['correct_answers']}")

# 初期化ボタン
if st.button('初期化する'):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()
