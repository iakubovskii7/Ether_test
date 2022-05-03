import pandas as pd
import numpy as np


def pivot_tables(df: pd.DataFrame, group_cols: str, agg_cols: str, threshold_share: float = 0) -> pd.DataFrame:
    return df.groupby([group_cols])[agg_cols].sum() \
        .to_frame("value") \
        .query("value > 0") \
        .eval("Total = value.sum()") \
        .eval("Share_of_total = 100 * (value / Total)") \
        .sort_values("value", ascending=False) \
        .query(f"Share_of_total >= {threshold_share}")\
        .style.format({"value": '{:.1f}', "Total": '{:.1f}', "Share_of_total": '{:.1f}'})


def create_time_series(df: pd.DataFrame, group_col: str, agg_cols: str):
    """
    This function created daily time series data in needed column name
    :param df:
    :param group_col:
    :param agg_cols:
    :return:
    """
    result_df = df\
        .groupby(["DateTime", group_col])[agg_cols].sum().reset_index() \
        .pivot_table(index='DateTime', columns=group_col, values=group_col, aggfunc=np.abs).resample("D").sum()
    return result_df
