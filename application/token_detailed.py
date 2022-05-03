import streamlit as st
import pandas as pd
import numpy as np
from application.load_transaction_data import load_ether_data_st, load_transaction_token_df
from application.utils import pivot_tables
from application.plots import plotly_line_series, two_lines
from application.utils import pivot_tables
pd.options.display.precision = 1


def show_detailed_token_statistics():
    """
    This function calculate statistics in method's and user type slices
    :return:
    """
    st.subheader("DETAILED TOKEN STATISTICS")
    df = load_transaction_token_df(load_ether_data_st().query("Status != 'Error(0)'"))
    chosen_start_time = st.date_input("Enter start date", df['DateTime'].min())
    chosen_end_time = st.date_input("Enter end date", df['DateTime'].max())
    filtered_df = df.query(f"DateTime >= '{chosen_start_time}' & DateTime <= '{chosen_end_time}'")
    filtered_df['Quantity_abs'] = np.abs(filtered_df['Quantity'])
    filtered_df['Value_USD_abs'] = np.abs(filtered_df['Value_USD'])
    quantity_outflow_token_df = filtered_df \
        .query("From == 'user'") \
        .set_index(['DateTime', 'token_short_name'])['Quantity'].reset_index() \
        .pivot_table(index='DateTime', columns='token_short_name', values='Quantity', aggfunc=np.abs).resample(
        "D").sum()

    quantity_inflow_token_df = filtered_df \
        .query("To == 'user'") \
        .groupby(['DateTime', 'token_short_name'])['Quantity'].sum().reset_index() \
        .pivot_table(index='DateTime', columns='token_short_name', values='Quantity', aggfunc=np.abs).resample(
        "D").sum()

    value_usd_inflow_token_df = filtered_df \
        .query("To == 'user'") \
        .groupby(['DateTime', 'token_short_name'])['Value_USD'].sum().reset_index() \
        .pivot_table(index='DateTime', columns='token_short_name', values='Value_USD', aggfunc=np.abs).resample(
        "D").sum()

    value_usd_outflow_token_df = filtered_df \
        .query("From == 'user'") \
        .set_index(['DateTime', 'token_short_name'])['Value_USD'].reset_index() \
        .pivot_table(index='DateTime', columns='token_short_name', values='Value_USD', aggfunc=np.abs).resample(
        "D").sum()

    quantity_token_df = quantity_outflow_token_df.join(quantity_inflow_token_df, rsuffix='_inflow', lsuffix='_outflow',
                                                       how='outer').fillna(0)
    usd_token_df = value_usd_outflow_token_df.join(value_usd_inflow_token_df, rsuffix='_inflow', lsuffix='_outflow',
                                                   how='outer').fillna(0)

    filtered_df['Value_USD_cumsum'] = filtered_df['Value_USD'].cumsum()
    st.dataframe(filtered_df)

    st.text("Total amount of token in USD by token type for OUTFLOW operations")
    st.table(pivot_tables(filtered_df.query("From == 'user'"),
                          'token_short_name', 'Value_USD_abs', threshold_share=1))

    st.text("Total amount of token in USD by token type for INFLOW operations")
    st.table(pivot_tables(filtered_df.query("To == 'user'"), 'token_short_name', 'Value_USD', threshold_share=1))

    st.text("Total amount of token in Quantity by token type for OUTGOING operations")
    st.table(pivot_tables(filtered_df.query("From == 'user'"),
                          'token_short_name', 'Quantity_abs', threshold_share=1))

    st.text("Total amount of token in Quantity by token type for INCOMING operations")
    st.table(pivot_tables(filtered_df.query("To == 'user'"), 'token_short_name', 'Quantity', threshold_share=1))

    st.plotly_chart(plotly_line_series(filtered_df.set_index("DateTime")['Value_USD']\
                                       .resample("D").sum().cumsum(),
                                       title='Net flow of all tokens in USD'))
    # Choose your token
    total_turnover_tokens = filtered_df.groupby(['token_short_name'], as_index=False)[['Value_USD_abs', "Quantity_abs"]].sum()\
        .sort_values("Value_USD_abs", ascending=False)\
        .assign(Value_USD_abs=lambda x: x['Value_USD_abs'].astype(int),
                Quantity_abs=lambda x: x['Quantity_abs'].astype(int))
    token_turnover = tuple(zip(total_turnover_tokens['token_short_name'].values,
                                     total_turnover_tokens['Quantity_abs'].values,
                                     total_turnover_tokens['Value_USD_abs'].values))
    chosen_token = st.selectbox("Choose token (token_name, turnover in Quantity, turnover in USD)",
                                token_turnover)[0]
    st.plotly_chart(two_lines(quantity_token_df.reset_index()\
                              .query(f"(DateTime >= '{chosen_start_time}') & (DateTime <= '{chosen_end_time}')"),
                              "DateTime", f"{chosen_token}_outflow", f"{chosen_token}_inflow",
                              title='Quantity dynamic of inflow and outflow token'))

    return


