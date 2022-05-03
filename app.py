import streamlit as st
st.set_page_config(layout="wide")
from application.login import is_authenticated, clean_blocks, generate_login_block, login
from application.base_analytics import show_base_statistics
from application.token_analytics import show_token_statistics
from application.token_detailed import show_detailed_token_statistics


def main():

    st.title("Analysis of user behaviour in Ethereum blockchain")
    page = st.sidebar.selectbox("Statistics type",
                                ("Base analytics",
                                 "Token analytics",
                                 "Detailed token analytics"
                                 ))
    if page == "Base analytics":
        show_base_statistics()
    if page == "Token analytics":
        show_token_statistics()
    if page == "Detailed token analytics":
        show_detailed_token_statistics()


login_blocks = generate_login_block()
password = login(login_blocks)


if is_authenticated(password):
    clean_blocks(login_blocks)
    main()

elif password:
    st.info("Please enter a valid password")

st.stop()
