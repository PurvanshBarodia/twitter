import streamlit as st
import requests
from wordcloud import WordCloud
from io import BytesIO
from PIL import Image
import asyncio
import pickle
import os
from datetime import datetime


# Function to save the WordCloud object to a pickle file
def save_wordcloud(wordcloud, filename="wordcloud.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(wordcloud, file)

# Function to load the WordCloud object from a pickle file
def load_wordcloud(filename="wordcloud.pkl"):
    if os.path.exists(filename):
        with open(filename, "rb") as file:
            return pickle.load(file)
    return None

#Function to fetch data from API
async def fetch_data_async():
    response = requests.get("http://127.0.0.1:8000/post-cloud/")
    if response.status_code == 200:
        words = response.json().get('concatenated_titles_without_stop_words')
        wordcloud = WordCloud(collocations = False, background_color = 'white').generate(words)
        return save_wordcloud(wordcloud)
    else:
        st.error(f"Error: {response.status_code}")
        return None

file_path = "last_run_datetime.txt"

# Function to read the last saved datetime value
def read_last_run_datetime():
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                last_run_datetime_str = file.read()
                return datetime.strptime(last_run_datetime_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass
    return None

# Function to save the current datetime value
def save_current_datetime(current_datetime):
    with open(file_path, "w") as file:
        file.write(current_datetime.strftime("%Y-%m-%d %H:%M:%S"))

# Get the last saved datetime value
last_run_datetime = read_last_run_datetime()

st.write(" Post Word Cloud")

async def get_word_cloud():
    task = asyncio.create_task(fetch_data_async())

    # Use the pre-saved WordCloud object
    saved_wordcloud = load_wordcloud()
    wordcloud = saved_wordcloud

    # Display the word cloud using st.image()
    st.image(saved_wordcloud.to_image(), caption='Word Cloud', use_column_width=True)

    await task


if st.button("Get Word Cloud"):
    asyncio.run(get_word_cloud())
    # # Use the pre-saved WordCloud object
    # saved_wordcloud = load_wordcloud()
    # wordcloud = saved_wordcloud
    # # Display the word cloud using st.image()
    # st.image(wordcloud.to_image(), caption='Word Cloud', use_column_width=True)
    # # If there's no last saved datetime, use a default value (e.g., current time)
    if last_run_datetime is None:
        last_run_datetime = datetime.now()

    st.write("Fatched Time:", last_run_datetime)
    # current_time = datetime.now()
    # formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # Update last_run_datetime to the current time
    last_run_datetime = datetime.now()

    # Save the current datetime value for the next run
    save_current_datetime(last_run_datetime)


