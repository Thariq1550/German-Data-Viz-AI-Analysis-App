import streamlit as st
from login import main_login
from map_plot import main_map

def main():
    # Initialize session state variables if they don't exist
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state.logged_in:
        st.title("Feature Selection and Visualization")
        main_map()
    else:
        main_login()  # Show the login screen if not logged in

if __name__ == '__main__':
    main()