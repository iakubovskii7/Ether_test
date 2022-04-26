import streamlit as st
st.set_page_config(layout="wide")
from application.login import is_authenticated, clean_blocks, generate_login_block, login
from application.load_transaction_data import load_streamlit_data
from application.main_stat import show_statistics
import pandas as pd
import numpy as np


transactions_df = load_streamlit_data()


def main():

    st.title("Analysis of user behaviour in Ethereum blockchain")
    page = st.sidebar.selectbox("Statistics type",
                                ("Historic analysis",
                                 "Log analysis"))
    if page == "Historic analysis":
        show_statistics(transactions_df)





login_blocks = generate_login_block()
password = login(login_blocks)
if is_authenticated(password):
    clean_blocks(login_blocks)
    main()

elif password:
    st.info("Please enter a valid password")

st.stop()
