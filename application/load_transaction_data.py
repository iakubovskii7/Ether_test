import streamlit as st
import pandas as pd


def load_ether_data():
    data1 = pd.read_csv("data/transactions_ether/data1.csv")  # from 2022-08-04 to 2021-09-12
    data2 = pd.read_csv("data/transactions_ether/data2.csv")  # from 2021-09-12 to 2022-04-24
    current_value_col1 = [i for i in data1.columns if i.startswith("CurrentValue @")]
    current_value_col2 = [i for i in data2.columns if i.startswith("CurrentValue @")]
    data1 = data1.drop(columns=current_value_col1)
    data2 = data2.drop(columns=current_value_col2)
    cols = data1.columns
    df1 = data1.reset_index().drop(columns=['Method'])
    df2 = data2.reset_index().drop(columns=['Method'])
    df1.columns = cols
    df2.columns = cols
    df = pd.concat([df1, df2])\
        .drop_duplicates()\
        .sort_values("UnixTimestamp", ascending=False)\
        .drop(columns=['TxnFee(ETH)', 'UnixTimestamp', 'ContractAddress'])
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    return df


@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def load_ether_data_st():
    return load_ether_data()
