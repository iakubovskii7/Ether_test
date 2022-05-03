import streamlit as st
import pandas as pd
import numpy as np
import glob


contract_hash_dict = {
 "0x99fd1378ca799ed6772fe7bcdc9b30b389518962": "user",
 "0x2a67035357C3045438F3A92E46870a9E48e5AAB7".lower(): "suspected_user1",
 "0x937cdc9e86ba06aa5aaea221017a1d9fc7f59efd".lower(): "suspected_user2",
 "0xC098B2a3Aa256D2140208C3de6543aAEf5cd3A94".lower(): "FTX Exchange 2",
 "0xF403C135812408BFbE8713b5A23a04b3D48AAE31".lower(): "Convex Finance: Booster",
 "0x2dded6Da1BF5DBdF597C45fcFaa3194e53EcfeAF".lower(): "Curve.fi: cyDAI/cyUSDT/cyUSDC Pool",
 "0xDef1C0ded9bec7F1a1670819833240f027b25EfF".lower(): "0x: Exchange Proxy",
 "0xf650C3d88D12dB855b8bf7D11Be6C55A4e07dCC9".lower(): "Compound: cUSDT Token",
 "0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5".lower(): "Compound: cETH Token",
 "0xccF4429DB6322D5C611ee964527D42E5d685DD6a".lower(): "Compound: cWBTC2 Token",
  "0x39AA39c021dfbaE8faC545936693aC917d5E7563".lower(): "Compound: cUSDC Token",
 "0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B".lower(): "Compound: Comptroller ",
 "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48".lower(): "Centre: USD Coin",
 "0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9".lower(): "yearn: yUSDC Vault V2",
 "0x6cbAFEE1FaB76cA5B5e144c43B3B50d42b7C8c8f".lower(): "Abracadabra.Money: yvUSDC v2 Market",
 "0xA79828DF1850E8a3A3064576f380D90aECDD3359".lower(): "Curve Finance: 3Pool Deposit Zap",
 "0x920D9BD936Da4eAFb5E25c6bDC9f6CB528953F9f".lower(): "Abracadabra.Money: yvWETH v2 Market",
 "0xf859A1AD94BcF445A406B892eF0d3082f4174088".lower(): "Compound: Contract 1",
  "0x92be6adb6a12da0ca607f9d87db2f9978cd6ec3e".lower(): "Zapper.Fi: Yearn yVault Zap In",
    "0x67b66c99d3eb37fa76aa3ed1ff33e8e39f0b9c7a".lower(): "Alpha Finance Lab: ibETH Token",
}


token_names_df = pd.read_pickle("data/token_hash_name")


def load_ether_data() -> pd.DataFrame:
    """
    ETL for manually downloaded general transactions' data files
    :return:
    """
    data1 = pd.read_csv("data/transactions_ether/data1.csv")  # from 2022-08-04 to 2021-09-12
    data2 = pd.read_csv("data/transactions_ether/data2.csv")  # from 2021-09-12 to 2022-04-24
    new_cols = data1.reset_index().columns.tolist()
    new_cols.remove("index")
    df1 = data1.reset_index().drop(columns=['Method'])
    df2 = data2.reset_index().drop(columns=['Method'])
    df1.columns = new_cols
    df2.columns = new_cols
    df = pd.concat([df1, df2])\
        .drop_duplicates()\
        .sort_values("UnixTimestamp", ascending=False)\
        .drop(columns=['UnixTimestamp', 'ContractAddress'])

    # Rename main contracts
    df['From'] = df['From'] \
        .map(contract_hash_dict) \
        .fillna(df['From'])
    df['To'] = df['To'] \
        .map(contract_hash_dict) \
        .fillna(df['To'])

    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['Quantity'] = df[['Value_IN(ETH)', 'Value_OUT(ETH)']].max(axis=1)
    df['Quantity'] = np.where(df['From'] == 'user', -df['Quantity'], df['Quantity'])
    df['Value_USD'] = df['Quantity'] * df['Historical $Price/Eth']
    return df.sort_values("DateTime")


def load_token_data() -> pd.DataFrame:
    """
    ETL for manually downloaded token data files
    :return:
    """
    trans_token_df = []
    for file_tr_tkn in glob.glob("data/transactions_tokens/*.csv"):
        df0 = pd.read_csv(file_tr_tkn)
        df0['token'] = file_tr_tkn.split(".")[0].split("/")[-1]
        trans_token_df.append(df0)
    trans_token_df = pd.concat(trans_token_df).sort_values("DateTime")
    trans_token_df['Quantity'] = pd.to_numeric(trans_token_df['Quantity'].str.replace(",", ""))
    trans_token_df['DateTime'] = pd.to_datetime(trans_token_df['DateTime'])

    price_token_df = []
    for file_tr_tkn in glob.glob("data/price_tokens/*.csv"):
        df0 = pd.read_csv(file_tr_tkn)
        df0['token'] = file_tr_tkn.split("_Price")[0].split("/")[-1]
        price_token_df.append(df0)
    price_token_df = pd.concat(price_token_df)
    price_token_df['Date'] = pd.to_datetime(price_token_df['Date'])

    # Get average price between low and high
    price_token_df['Price'] = .5 * (price_token_df['High'] + price_token_df['Low'])

    # Merge transactions and price
    trans_token_df['Date'] = pd.to_datetime(trans_token_df['DateTime'].apply(lambda x: x.date()))
    token_df = trans_token_df.merge(price_token_df[['token', 'Date', 'Volume', 'Market Cap', 'Price']],
                                    how='left', on=['token', "Date"])

    # Rename main contracts
    token_df['From'] = token_df['From'] \
        .map(contract_hash_dict) \
        .fillna(token_df['From'])
    token_df['To'] = token_df['To'] \
        .map(contract_hash_dict) \
        .fillna(token_df['To'])

    token_df["Price"] = np.where(token_df['token'] == 'Noodle', 0.000048, token_df['Price'])
    token_df["Price"] = np.where(token_df['token'] == 'stETH', 2887.76, token_df['Price'])
    token_df["Price"] = np.where(token_df['Price'].isna(), 1, token_df['Price'])

    token_df['Quantity'] = np.where(token_df['From'] == 'user', -token_df['Quantity'], token_df['Quantity'])

    token_df['Value_USD'] = token_df['Quantity'] * token_df['Price']

    token_df = token_df.set_index("DateTime")

    return token_df


def load_transaction_token_df(transactions_df: pd.DataFrame) -> pd.DataFrame:
    """
    :param transactions_df:
    :return:
    """
    transactions_transfers_df = pd.read_pickle("data/transactions_transfers_df")
    float_cols = ['usd', 'amount', 'transfer_amount']
    for fl_col in float_cols:
        transactions_transfers_df[fl_col] = pd.to_numeric(transactions_transfers_df[fl_col], errors='coerce')
    transactions_transfers_df = transactions_transfers_df \
        .dropna(subset=['token_hash']) \
        .merge(token_names_df.drop(columns=['token_long_name']), on=['token_hash'], how='left') \
        .replace({"0x99fd1378ca799ed6772fe7bcdc9b30b389518962": "user"}) \
        .rename(columns={"from": 'From', 'to': 'To'}) \
        .query("(From == 'user') | (To == 'user')") \
        .merge(transactions_df[['Txhash', 'DateTime']], on=['Txhash'], how='left') \
        .sort_values("DateTime") \
        .assign(Quantity=lambda x: np.where(x['From'] == 'user', -x['amount'], x['amount']),
                Value_USD=lambda x: np.where(x['From'] == 'user', -x['usd'], x['usd']))[
         ['DateTime', 'From', 'To', 'token_short_name', 'Quantity', 'Value_USD',
          'transfer_amount', 'transfer_from', 'transfer_to', 'Txhash', 'token_hash']]
    return transactions_transfers_df


@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def load_ether_data_st():
    """
    Load data with cache in streamlit app
    :return:
    """
    return load_ether_data()


@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def load_token_data_st():
    """
    Load data with cache in streamlit app
    :return:
    """
    return load_token_data()


