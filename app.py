import streamlit as st
st.set_page_config(page_title="Databases Project", page_icon=":globe_with_meridians:")
from login import main_login
from dashboard import main_dashboard


def main():
    # Initialize session state variables if they don't exist
    st.session_state.setdefault('first_visit', True)
    st.session_state.setdefault('logged_in', False)

    # If it's the first visit, refresh the page
    if st.session_state.first_visit:
        st.session_state.first_visit = False  # Set to False and rerun
        st.rerun()  # Refresh the page

    # Used the above check, to resolve a UI issue where in a unexpected component was displayed probably from cache memory
    # The component was displayed the first time the user lands on the URL, but was removed on refreshing the page

    if st.session_state.logged_in:
        main_dashboard() #Proceed to the main dashboard if the user is logged in
    else:
        main_login()  # Show the login screen if not logged in

if __name__ == '__main__':
    main()