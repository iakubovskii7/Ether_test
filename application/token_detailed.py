import streamlit as st
import pandas as pd
import numpy as np
from application.load_transaction_data import load_ether_data_st, load_transaction_token_df
from application.utils import pivot_tables
from application.plots import plotly_line_series, two_lines
from application.utils import pivot_tables, create_time_series
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

    # Create time series dataset for all tokens USD/Quantity value by token

    quantity_outflow_token_df = create_time_series(filtered_df.query("From == 'user'"), 'token_short_name', "Quantity")
    quantity_inflow_token_df = create_time_series(filtered_df.query("To == 'user'"), 'token_short_name', "Quantity")
    value_usd_outflow_token_df = create_time_series(filtered_df.query("From == 'user'"), 'token_short_name', "Value_USD")
    value_usd_inflow_token_df = create_time_series(filtered_df.query("To == 'user'"), 'token_short_name', "Value_USD")

    quantity_token_df = quantity_outflow_token_df.join(quantity_inflow_token_df, rsuffix='_inflow', lsuffix='_outflow',
                                                       how='outer').fillna(0)
    usd_token_df = value_usd_outflow_token_df.join(value_usd_inflow_token_df, rsuffix='_inflow', lsuffix='_outflow',
                                                   how='outer').fillna(0)

    # Create time series dataset for all tokens in USD/Quantity value by receivers/senders

    quantity_outflow_receivers_df = create_time_series(filtered_df.query("From == 'user'"), 'To', "Quantity")
    quantity_inflow_senders_df = create_time_series(filtered_df.query("To == 'user'"), 'From', "Quantity")
    value_usd_outflow_receivers_df = create_time_series(filtered_df.query("From == 'user'"), 'To', "Value_USD")
    value_usd_inflow_senders_df = create_time_series(filtered_df.query("To == 'user'"), 'From', "Value_USD")

    quantity_rec_sen_df = quantity_outflow_receivers_df.join(quantity_inflow_senders_df, rsuffix='_inflow', lsuffix='_outflow',
                                                             how='outer').fillna(0)
    usd_rec_sen_df = value_usd_outflow_receivers_df.join(value_usd_inflow_senders_df, rsuffix='_inflow', lsuffix='_outflow',
                                                         how='outer').fillna(0)

    filtered_df['Value_USD_cumsum'] = filtered_df['Value_USD'].cumsum()
    st.dataframe(filtered_df)

    st.text("Total amount of token in USD by token type for OUTFLOW operations")
    st.table(pivot_tables(filtered_df.query("From == 'user'"),
                          'token_short_name', 'Value_USD_abs', threshold_share=1))

    st.text("Total amount of token in USD by token type for INFLOW operations")
    st.table(pivot_tables(filtered_df.query("To == 'user'"), 'token_short_name', 'Value_USD', threshold_share=1))

    st.text("Total amount of token in Quantity by token type for OUTFLOW operations")
    st.table(pivot_tables(filtered_df.query("From == 'user'"),
                          'token_short_name', 'Quantity_abs', threshold_share=1))

    st.text("Total amount of token in Quantity by token type for OUTFLOW operations")
    st.table(pivot_tables(filtered_df.query("To == 'user'"), 'token_short_name', 'Quantity_abs', threshold_share=1))

    st.text("Total amount of token in Quantity by receiver for OUTFLOW operations")
    st.table(pivot_tables(filtered_df.query("From == 'user'"), 'To', 'Quantity_abs', threshold_share=1))

    st.text("Total amount of token in Quantity by sender for INFLOW operations")
    st.table(pivot_tables(filtered_df.query("To == 'user'"), 'From', 'Quantity_abs', threshold_share=1))

    st.text("Total amount of token in USD by receiver for OUTFLOW operations")
    st.table(pivot_tables(filtered_df.query("From == 'user'"), 'To', 'Value_USD_abs', threshold_share=1))

    st.text("Total amount of token in USD by sender for INFLOW operations")
    st.table(pivot_tables(filtered_df.query("To == 'user'"), 'From', 'Value_USD_abs', threshold_share=1))

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

    # Choose your receiver/sender address
    total_turnover_receiver = filtered_df.query("From == 'user'").groupby(['To'], as_index=False)[['Value_USD_abs', "Quantity_abs"]].sum()\
        .sort_values("Value_USD_abs", ascending=False)\
        .assign(Value_USD_abs=lambda x: x['Value_USD_abs'].astype(int),
                Quantity_abs=lambda x: x['Quantity_abs'].astype(int))
    address_turnover = tuple(zip(total_turnover_receiver['To'].values,
                                  total_turnover_receiver['Quantity_abs'].values,
                                  total_turnover_receiver['Value_USD_abs'].values))
    chosen_address = st.selectbox("Choose receiver/sender address (receiver, turnover in Quantity, turnover in USD)",
                                  address_turnover)[0]
    st.plotly_chart(two_lines(quantity_rec_sen_df.reset_index()\
                              .query(f"(DateTime >= '{chosen_start_time}') & (DateTime <= '{chosen_end_time}')"),
                              "DateTime", f"{chosen_address}_outflow", f"{chosen_address}_inflow",
                              title='Quantity dynamic of inflow and outflow token'))




    return


