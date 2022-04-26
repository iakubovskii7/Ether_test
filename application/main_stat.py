import streamlit as st
import pandas as pd
import numpy as np


def show_statistics(df):
    st.subheader("TRANSACTIONS STATISTICS")
    chosen_start_time = st.date_input("Enter start date", df['DateTime'].min())
    chosen_end_time = st.date_input("Enter end date", df['DateTime'].max())
    all_methods = df['Method'].unique().tolist()
    all_methods.append('All')
    chosen_method = st.selectbox('Choose method', all_methods, index=len(all_methods)-1)
    if chosen_method != 'All':
        filtered_df = df.query(f"Method == '{chosen_method}'")
    filtered_df = df.query(f"DateTime >= '{chosen_start_time}' & DateTime <= '{chosen_end_time}'")
    st.dataframe(filtered_df)

    st.text("ETH total per every transaction type:")
    st.dataframe(filtered_df.groupby(['Method'])[['Value_IN(ETH)', 'Value_OUT(ETH)']].sum() \
        .sort_values(["Value_OUT(ETH)", "Value_IN(ETH)"], ascending=False))

    st.text("ETH total per every user IN ")
    st.dataframe(filtered_df.groupby(['From'])['Value_IN(ETH)'].sum().to_frame("Total_IN")\
                 .join(filtered_df.groupby(['From'])['Value_IN(ETH)'].count().to_frame("Count_IN")))

    st.text("ETH total per every user OUT")
    st.dataframe(filtered_df.groupby(['To'])['Value_OUT(ETH)'].sum().to_frame("Total_OUT")\
                 .join(filtered_df.groupby(['To'])['Value_OUT(ETH)'].count().to_frame("Count_OUT")))






