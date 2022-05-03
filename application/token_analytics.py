import streamlit as st
import pandas as pd
import numpy as np
from application.plots import plotly_line_series, plotly_barplot
from application.load_transaction_data import load_token_data_st
from application.utils import pivot_tables


def show_token_statistics():
    st.subheader("TOKEN TRANSACTIONS STATISTICS")
    df = load_token_data_st().reset_index()
    df['Quantity_abs'] = np.abs(df['Quantity'])
    chosen_start_time = st.date_input("Enter start date", df['DateTime'].min())
    chosen_end_time = st.date_input("Enter end date", df['DateTime'].max())
    all_methods = df['Method'].unique().tolist()
    all_methods.append('All')
    chosen_method = st.selectbox('Choose method', all_methods, index=len(all_methods)-1)

    filtered_df = df.query(f"DateTime >= '{chosen_start_time}' & DateTime <= '{chosen_end_time}'")
    if chosen_method != 'All':
        filtered_df = filtered_df.query(f"Method == '{chosen_method}'")
    filtered_df['Value_USD_cumsum'] = filtered_df['Value_USD'].cumsum()

    st.dataframe(filtered_df)

    choose_share = st.number_input("Choose threshold for total share, %", value=1)

    st.text("Total amount of token in USD by token type")
    st.table(pivot_tables(filtered_df, 'token', 'Value_USD', threshold_share=choose_share))

    st.text("Total inflow token operation methods")
    st.table(pivot_tables(filtered_df.query("Value_USD > 0"), 'Method', 'Value_USD', threshold_share=choose_share))

    st.text("Total outflow token operation methods")
    st.table(pivot_tables(filtered_df.query("Value_USD < 0")\
                          .eval("Value_USD = abs(Value_USD)"), 'Method', 'Value_USD', threshold_share=choose_share))

    # Bar plots
    # Plots
    st.plotly_chart(plotly_barplot(pivot_tables(filtered_df, 'Method', 'Value_USD', threshold_share=choose_share, plot=True)\
                                   .reset_index(),
                                   x='Share_of_total', y='Method', title='Total inflow ETH operation methods'))

    st.plotly_chart(plotly_barplot(pivot_tables(filtered_df, 'Method', 'Value_USD', threshold_share=choose_share, plot=True)\
                                   .reset_index(),
                                   x='Share_of_total', y='Method', title='Total outflow ETH operation methods'))

    st.plotly_chart(plotly_barplot(pivot_tables(filtered_df.query("To == 'user'"), 'From', 'Value_USD',
                                                threshold_share=choose_share, plot=True)\
                                   .reset_index(),
                                   x='Share_of_total', y='From', title='Total inflow ETH operation partners'))

    st.plotly_chart(plotly_barplot(pivot_tables(filtered_df.query("From == 'user'"), 'To', 'Value_USD',
                                                threshold_share=choose_share, plot=True)\
                                   .reset_index(),
                                   x='Share_of_total', y='To', title='Total inflow ETH operation partners'))

    # Plot time series
    st.plotly_chart(plotly_line_series(filtered_df.set_index("DateTime")['Value_USD']\
                                       .resample("D").sum().cumsum(),
                                       title='Nominal amount of all tokens'))

    st.subheader("Physical amount of tokens during all period")
    inc_out = st.selectbox("Choose type", ["Inflow", "Outflow"])
    if inc_out == "Inflow":
        st.plotly_chart(plotly_line_series(filtered_df\
                                           .query("token == 'cETH' & To == 'user'")\
                                           .set_index("DateTime").resample("D")['Quantity_abs'].sum().cumsum(),
                        title='Compound ETH'))

        st.plotly_chart(plotly_line_series(filtered_df\
                                           .query("token == 'cDAI' & To == 'user'")\
                                           .set_index("DateTime").resample("D")['Quantity_abs'].sum().cumsum(),
                        title='Compound DAI'))

        st.plotly_chart(plotly_line_series(filtered_df\
                                           .query("token == 'USDC' & To == 'user'")\
                                           .set_index("DateTime").resample("D")['Quantity_abs'].sum().cumsum(),
                        title='Stablecoin, USDC'))

        st.plotly_chart(plotly_line_series(filtered_df\
                                           .query("token == 'CurveDAI' & To == 'user'")\
                                           .set_index("DateTime").resample("D")['Quantity_abs'].sum().cumsum(),
                        title='Stablecoin, CurveDAI'))

        st.plotly_chart(plotly_line_series(filtered_df\
                                           .query("token == 'TetherUSD' & To == 'user'")\
                                           .set_index("DateTime").resample("D")['Quantity_abs'].sum().cumsum(),
                        title='Stablecoin, TetherUSD'))

        st.plotly_chart(plotly_line_series(filtered_df\
                                           .query("token == 'DAI' & To == 'user'")\
                                           .set_index("DateTime").resample("D")['Quantity_abs'].sum().cumsum(),
                        title='Stablecoin, DAI'))

    if inc_out == "Outflow":
        st.plotly_chart(plotly_line_series(filtered_df\
                                           .query("token == 'cETH' & From == 'user'")\
                                           .set_index("DateTime").resample("D")['Quantity_abs'].sum().cumsum(),
                        title='Compound ETH'))

        st.plotly_chart(plotly_line_series(filtered_df\
                                           .query("token == 'cDAI' & From == 'user'")\
                                           .set_index("DateTime").resample("D")['Quantity_abs'].sum().cumsum(),
                        title='Compound DAI'))

        st.plotly_chart(plotly_line_series(filtered_df\
                                           .query("token == 'USDC' & From == 'user'")\
                                           .set_index("DateTime").resample("D")['Quantity_abs'].sum().cumsum(),
                        title='Stablecoin, USDC'))

        st.plotly_chart(plotly_line_series(filtered_df\
                                           .query("token == 'CurveDAI' & From == 'user'")\
                                           .set_index("DateTime").resample("D")['Quantity_abs'].sum().cumsum(),
                        title='Stablecoin, CurveDAI'))

        st.plotly_chart(plotly_line_series(filtered_df\
                                           .query("token == 'TetherUSD' & From == 'user'")\
                                           .set_index("DateTime").resample("D")['Quantity_abs'].sum().cumsum(),
                        title='Stablecoin, TetherUSD'))

        st.plotly_chart(plotly_line_series(filtered_df\
                                           .query("token == 'DAI' & From == 'user'")\
                                           .set_index("DateTime").resample("D")['Quantity_abs'].sum().cumsum(),
                        title='Stablecoin, DAI'))




    return
