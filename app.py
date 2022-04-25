import streamlit as st
st.set_page_config(layout="wide")
from application.login import is_authenticated, clean_blocks, generate_login_block, login
import pandas as pd
import numpy as np


def main():

    st.title("Analysis of user behaviour in Etherium blockchain")



login_blocks = generate_login_block()
password = login(login_blocks)
if is_authenticated(password):
    clean_blocks(login_blocks)
    main()

elif password:
    st.info("Please enter a valid password")

st.stop()
