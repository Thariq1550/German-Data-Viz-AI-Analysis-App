import json
import streamlit as st
import bcrypt
import time

# Load user cres from JSON file
def load_creds():
    with open('creds.json', 'r') as file:
        return json.load(file)
    
# Function to check user creds
def check_creds(username, password, credentials):
    hashed_password = credentials.get(username)
    if hashed_password:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
    return False
    
# Login page
def main_login():
    st.image('resources/whu_logo.png', width=250)  # Display logo
    st.title('Databases Group Project')
    st.subheader('Group2')

    # Create a form for login 
    with st.form(key='login_form'):
        username = st.text_input('Username')
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button('Login')

    # Load creds and check login
    if submit_button:
        credentials = load_creds()
        if check_creds(username, password, credentials):
            st.success('Login successful! Redirecting...')
            time.sleep(1)  # Delay for 1 second before rerunning
            # Proceed to the main content of your app
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error('Invalid username or password')
