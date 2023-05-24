import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO

st.set_page_config(page_title='Text to Speech', layout='centered')

st.header("Cún's Spelling Bee")

st.markdown("""Press the plus/minus buttons to navigate through the pages.""")
st.markdown("""Listen to the pronunciation, then enter the word to guess. Press Enter to submit your answer.""")
st.markdown("Reveal the word and pronunciation to check your answer.")
st.markdown("***")



def speak_word(word):
    tts = gTTS(text=word, lang='en')
    return tts

df = pd.read_csv('words.csv')
df = df.sample(frac=1, random_state=1).reset_index()
words_dict = df.to_dict('records')

words_per_page = 10
total_pages = len(words_dict) // words_per_page
if len(words_dict) % words_per_page > 0: total_pages += 1 # Accounting for words on the last page

words = {}

for i, record in enumerate(words_dict, start=1):
    word = record['word']
    tts = speak_word(word)
    st.session_state[word] = tts

page = st.number_input('Page', min_value=1, max_value=total_pages, value=1, step=1)

start = (page - 1) * words_per_page

for i in range(start, start+words_per_page):
    if i < len(words_dict):
        record = words_dict[i]
        word = record['word']
        pronunciation = record['pronunciation']

        # Reveal button
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Word {i+1}")
            reveal = st.button(f"Reveal Word and Pronunciation {i+1}")
            if reveal:
                st.write(f'Word {i+1}: {word}')
                st.write(f'Pronunciation: {pronunciation}')
        with col2:
            word_input = st.text_input("Enter word:", key=i)
            if word_input == word:
                st.write("Correct!")
            elif word_input == '':
                pass
            else:
                st.write("Incorrect!")

        audio_bytes = st.session_state[word]
        fp = BytesIO()
        audio = audio_bytes.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
