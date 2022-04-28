import streamlit as st
import pandas as pd
import numpy as np
from load_transaction_data import load_ether_data_st
from utils import pivot_tables
pd.options.display.precision = 1


def show_base_statistics():
    st.subheader("BASE TRANSACTIONS STATISTICS")
    df = load_ether_data_st()
    chosen_start_time = st.date_input("Enter start date", df['DateTime'].min())
    chosen_end_time = st.date_input("Enter end date", df['DateTime'].max())
    all_methods = df['Method'].unique().tolist()
    all_methods.append('All')
    chosen_method = st.selectbox('Choose method', all_methods, index=len(all_methods)-1)
    filtered_df = df.query(f"DateTime >= '{chosen_start_time}' & DateTime <= '{chosen_end_time}'")
    if chosen_method != 'All':
        filtered_df = df.query(f"Method == '{chosen_method}'")
    st.dataframe(filtered_df[['DateTime', 'From', 'To', 'Method',
                              'Value_IN(ETH)', 'Value_OUT(ETH)',
                              'Quantity', 'Value_USD'
                              ]].set_index("DateTime").style.format(
        {col: '{:.1f}' for col in filtered_df.select_dtypes(exclude="object")})
    )

    st.text("Total incoming ETH operation methods")
    st.table(pivot_tables(filtered_df, 'Method', 'Value_IN(ETH)'))

    st.text("Total outgoing ETH operation methods")
    st.table(pivot_tables(filtered_df, 'Method', 'Value_OUT(ETH)'))

    st.text("Total incoming ETH operation partners")
    st.table(pivot_tables(filtered_df.query("To == 'user'"), "From", "Value_IN(ETH)"))

    st.text("Total outgoing ETH operation partners")
    st.table(pivot_tables(filtered_df.query("From == 'user'"), "To", "Value_OUT(ETH)"))




