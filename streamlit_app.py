import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="英単語テストアプリ")

# CSS for custom background
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(180deg, #f4efd1 90%, #df3b1f 10%);
        height: 100vh;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# タイトルと説明
st.title('英単語テストアプリ')
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

# 出題範囲選択
st.sidebar.title('出題範囲を選択してください')
ranges = [f"{i*100+1}-{(i+1)*100}" for i in range(14)]
selected_range = st.sidebar.selectbox("出題範囲", ranges)

# 選択された範囲に基づいてデータをフィルタリング
range_start, range_end = map(int, selected_range.split('-'))
filtered_words_df = words_df[(words_df['No.'] >= range_start) & (words_df['No.'] <= range_end)].sort_values(by='No.')

# 制限時間の設定
time_limit = st.sidebar.slider("制限時間 (秒)", min_value=60, max_value=600, value=60, step=10)

# テスト形式選択 (トグルボタン風)
st.sidebar.title("テスト形式を選択してください")
test_type = st.sidebar.radio("", ('英語→日本語', '日本語→英語'), horizontal=True)

# テスト開始ボタン
if st.button('テストを開始する'):
    st.session_state.test_started = True
    st.session_state.correct_answers = 0
    st.session_state.wrong_answers = []
    st.session_state.current_question = 0
    st.session_state.start_time = time.time()
    st.session_state.time_limit = time_limit
    st.session_state.finished = False

    # 最初の問題を設定
    st.session_state.current_question_data = filtered_words_df.iloc[st.session_state.current_question]
    if test_type == '英語→日本語':
        options = list(filtered_words_df['語の意味'].sample(3))
        options.append(st.session_state.current_question_data['語の意味'])
    else:
        options = list(filtered_words_df['単語'].sample(3))
        options.append(st.session_state.current_question_data['単語'])
    options.append("わからない")
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
    if st.session_state.current_question < 100:
        st.session_state.current_question_data = filtered_words_df.iloc[st.session_state.current_question]
        if test_type == '英語→日本語':
            options = list(filtered_words_df['語の意味'].sample(3))
            options.append(st.session_state.current_question_data['語の意味'])
        else:
            options = list(filtered_words_df['単語'].sample(3))
            options.append(st.session_state.current_question_data['単語'])
        options.append("わからない")
        np.random.shuffle(options)
        st.session_state.options = options
        st.session_state.answer = None
    else:
        st.session_state.test_started = False
        st.session_state.finished = True

# 残り時間の表示と更新
def update_timer():
    if 'start_time' in st.session_state:
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = st.session_state.time_limit - elapsed_time
        if remaining_time > 0 and not st.session_state.finished:
            st.write(f"残り時間: {int(remaining_time)}秒")
            st.progress(elapsed_time / st.session_state.time_limit)  # タイマーの進行状況バーを表示
            time.sleep(1)
            st.experimental_rerun()  # ページを再レンダリングしてタイマーを更新
        else:
            st.session_state.test_started = False
            display_results()

# テスト終了後の結果表示
def display_results():
    correct_answers = st.session_state.correct_answers
    total_questions = 100
    accuracy = correct_answers / total_questions
    wrong_answers = len(st.session_state.wrong_answers)

    st.write(f"テスト終了！正解数: {correct_answers}/{total_questions}")
    st.progress(accuracy)
    
    st.write("正解数と不正解数")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("正解数", correct_answers)
    with col2:
        st.metric("不正解数", wrong_answers)

    st.write(f"正答率: {accuracy:.0%}")
    st.progress(accuracy)

    if st.session_state.wrong_answers:
        st.write("間違えた単語とその語の意味:")
        for no, word, meaning in st.session_state.wrong_answers:
            st.write(f"番号: {no}, 単語: {word}, 語の意味: {meaning}")

# テストが開始された場合の処理
if 'test_started' in st.session_state and st.session_state.test_started:
    if st.session_state.current_question < 100:
        if test_type == '英語→日本語':
            st.subheader(f"単語: {st.session_state.current_question_data['単語']}")
        else:
            st.subheader(f"語の意味: {st.session_state.current_question_data['語の意味']}")
        st.radio("選択してください", st.session_state.options, key='answer', on_change=update_question)
        update_timer()  # タイマーを更新
    else:
        display_results()
else:
    if 'start_time' in st.session_state:
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = st.session_state.time_limit - elapsed_time
        if remaining_time > 0 and not st.session_state.finished:
            st.write(f"残り時間: {int(remaining_time)}秒")
            st.progress(elapsed_time / st.session_state.time_limit)  # タイマーの進行状況バーを表示
        else:
            st.session_state.test_started = False
            display_results()
