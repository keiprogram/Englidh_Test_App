# Streamlitライブラリをインポート
import streamlit as st

# タイトルを設定
st.title('Streamlitのサンプルアプリ')

# テキスト入力ボックスを作成し、ユーザーからの入力を受け取る
user_input = st.text_input('あなたの名前を入力してください')

# ボタンを作成し、クリックされたらメッセージを表示
if st.button('挨拶する'):
    st.success(f'こんにちは、{user_input}さん!')

# スライダーを作成し、値を選択
number = st.slider('好きな数字を選んでください', 0, 100)

# 選択した数字を表示
st.write(f'あなたが選んだ数字は{number}です。')

# 2進数に変換する機能
binary_representation = bin(number)[2:]  # 'bin'関数で2進数に変換し、先頭の'0b'を取り除く
st.write(f'その数字の2進数表現は{binary_representation}です。')
