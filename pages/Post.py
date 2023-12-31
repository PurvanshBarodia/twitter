import streamlit as st
import requests

# Streamlit app
st.title("Post")

# Get user input
st.write("Get Post")
post_id = st.text_input("Enter Post ID:", key= "widget7")

# Make a request to the FastAPI endpoint
if st.button("Get Post"):
    response = requests.get(f"http://127.0.0.1:8000/posts/{post_id}")
    # Display the response
    try:
        post_id = int(post_id)
    except ValueError as e:
        st.write("Invalid Input")
    else:
        if response.status_code == 200:
            st.success(response.json())
        else:
            st.error(f"Error: {response.status_code}")

st.write("Create New Post")
post_id = st.text_input("Enter Post ID:", key="widget8")
title = st.text_input("Enter Post Title:", key="widget9")
content = st.text_input("Enter Post Content:",key="widget10")
user_id = st.text_input("Enter User ID:", key="widget11")




if st.button("Create Post"):
    # Display the response
    try:
        post_id = int(post_id)
    except ValueError as e:
        st.write("Invalid Input")
    else:
        pay_load = {"title":title, "content":content, "user_id":user_id, "id":post_id}
        response = requests.post("http://127.0.0.1:8000/posts/", json=pay_load)
        if response.status_code == 200:
            st.success(response.json())
        else:
            st.error(f"Error: {response.status_code}")

st.write("Delete Post")
post_id = st.text_input("Enter Post ID:", key="widget12")

if st.button("Delete Post"):
    try:
        post_id = int(post_id)
    except ValueError as e:
        st.write("Invalid Input")
    else:
        response = requests.delete(f"http://127.0.0.1:8000/delete_posts/{post_id}")
        if response.status_code == 200:
            st.success(response.json())
        else:
            st.error(f"Error: {response.status_code}")
