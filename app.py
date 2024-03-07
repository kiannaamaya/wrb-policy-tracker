import streamlit as st
from app_pages import home, data_explanation, data_filtering

def main():
    st.sidebar.title("Navigation")
    if 'page' not in st.session_state:
        st.session_state.page = "Home"  # Default page

    if st.sidebar.button("Home"):
        st.session_state.page = "Home"
    if st.sidebar.button("Data Explaination"):
        st.session_state.page = "Data Explaination"
    if st.sidebar.button("Explore Policy Impact"):
        st.session_state.page = "Explore Policy Impact"

    if st.session_state.page == "Home":
        home.show()
    elif st.session_state.page == "Data Explaination":
        data_explanation.show()
    elif st.session_state.page == "Explore Policy Impact":
        data_filtering.show()



if __name__ == "__main__":
    main()
