import streamlit as st
import requests

# Streamlit app
st.title("FastAPI and Streamlit Integration")

# Get user input
st.write("Get User")
user_id = st.text_input("Enter User ID:", key= "widget1")

# Make a request to the FastAPI endpoint
if st.button("Get User"):
    response = requests.get(f"http://127.0.0.1:8000/user/{user_id}")
    # Display the response
    try:
        user_id = int(user_id)
    except ValueError as e:
        st.write("Invalid Input")
    else:
        if response.status_code == 200:
            st.success(response.json())
        else:
            st.error(f"Error: {response.status_code}")

st.write("Create New User")
user_id = st.text_input("Enter User ID:", key="widget2")
user_name = st.text_input("Enter User Name:", key="widget3")


if st.button("Create User"):
    # Display the response
    try:
        user_id = int(user_id)
    except ValueError as e:
        st.write("Invalid Input")
    else:
        pay_load = {"id":user_id, "username":user_name}
        response = requests.post("http://127.0.0.1:8000/users/", json=pay_load)
        if response.status_code == 200:
            st.success(response.json())
        else:
            st.error(f"Error: {response.status_code}")

st.write("Update User")
user_id = st.text_input("Enter User ID:", key="widget4")
user_name = st.text_input("Enter new name:", key="widget5")

if st.button("Update User"):
    try:
        user_id = int(user_id)
    except ValueError as e:
        st.write("Invalid Input")
    else:
        params = {"new_name":user_name}
        response = requests.put(f"http://127.0.0.1:8000/update-user-name/{user_id}",params=params)
        if response.status_code == 200:
            st.success(response.json())
        else:
            st.error(f"Error: {response.status_code}")

st.write("Delete User")
user_id = st.text_input("Enter User ID:", key="widget6")

if st.button("Delete User"):
    try:
        user_id = int(user_id)
    except ValueError as e:
        st.write("Invalid Input")
    else:
        response = requests.delete(f"http://127.0.0.1:8000/user/{user_id}")
        if response.status_code == 200:
            st.success(response.json())
        else:
            st.error(f"Error: {response.status_code}")









