import streamlit as st
import bcrypt
import time
import sqlite3

# Database setup: Create a connection and table if it doesn't exist
def init_db():
    conn = sqlite3.connect('creds.db')  # SQLite database file
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            hashed_password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to fetch user credentials from SQLite database
def load_creds(username):
    conn = sqlite3.connect('creds.db')
    cursor = conn.cursor()
    cursor.execute("SELECT hashed_password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]  # Return the hashed password if the user exists
    return None

# Function to check user credentials
def check_creds(username, password):
    hashed_password = load_creds(username)
    if hashed_password:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())  # Compare hashed password
    return False

# Function to register new users
def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    conn = sqlite3.connect('creds.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        st.success("User registered successfully!")
    except sqlite3.IntegrityError:
        st.error("Username already exists. Please choose a different username.")
    conn.close()

def login_page():
    st.image('resources/whu_logo.png', width=250)  # Display logo
    st.title('DATABASES GROUP PROJECT')
    st.subheader('Welcome to our Data Analysis App!📈📊')
    st.markdown("**_~ Group 2_**")

    # Create a form for login 
    with st.form(key='login_form'):
        username = st.text_input('Username')
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button('Login')

    # Check login credentials only if the form is submitted
    if submit_button:
        if check_creds(username, password):
            st.session_state.logged_in = True
            st.success('Login successful! Redirecting...')
            time.sleep(1)
            #st.session_state.page = 'main'  # Set page to main after successful login
            st.rerun()  # Redirect to main page
        else:
            st.error('Invalid username or password')
   
    st.info('Please register and login, if you are a first time user.')

    # Link to switch to registration page
    if st.button("Don't have an account? Register here", key="register_button"):
        st.session_state.page = 'register'
        st.rerun()  # Redirect to registration page

# Register page
def register_page():
    st.image('resources/whu_logo.png', width=250)  # Display logo
    st.header('Register for Databases Group Project')
    
    # Supporting instructions
    st.markdown("""
        **Please fill in the fields below to create a new account.**
        Once registered, you can log in and begin exploring the dashboard immediately.
    """)

    # Create a form for registration
    with st.form(key='register_form'):
        new_username = st.text_input('Choose a Username')
        new_password = st.text_input("Choose a Password", type="password")
        register_button = st.form_submit_button('Register')

    # Register new user
    if register_button:
        if new_username and new_password:
            register_user(new_username, new_password)
        else:
            st.error("Please fill in both fields.")

    # Button to switch back to the login page 
    if st.button("Go back to Login"):
        st.session_state.page = 'login'
        st.rerun()  # Rerun to switch pages


# Main function to handle login and register views
def main_login():
    # Initialize database and table
    init_db()

    # Set default page to login if not already in session state
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # Render the page based on the current session state
    if st.session_state.page == 'login':
        login_page()
    if st.session_state.page == 'register':
        register_page()
