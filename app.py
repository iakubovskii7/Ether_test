import streamlit as st
st.set_page_config(layout="wide")
from application.login import is_authenticated, clean_blocks, generate_login_block, login
from application.load_transaction_data import load_ether_data_st, load_token_data_st
from application.base_analytics import show_base_statistics
from application.token_analytics import show_token_statistics
import pandas as pd
import numpy as np


transactions_df = load_ether_data_st()
token_df = load_token_data_st()


def main():

    st.title("Analysis of user behaviour in Ethereum blockchain")
    page = st.sidebar.selectbox("Statistics type",
                                ("Base analytics",
                                 "Token analytics"))
    if page == "Base analytics":
        show_base_statistics()
    if page == "Token analytics":
        show_token_statistics()


login_blocks = generate_login_block()
password = login(login_blocks)
if is_authenticated(password):
    clean_blocks(login_blocks)
    main()

elif password:
    st.info("Please enter a valid password")

st.stop()
