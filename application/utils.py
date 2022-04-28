import pandas as pd


def pivot_tables(df, group_cols, agg_cols):
    return df.groupby([group_cols])[agg_cols].sum() \
        .to_frame("value") \
        .query("value > 0") \
        .eval("Total = value.sum()") \
        .eval("Share_of_total = 100 * (value / Total)") \
        .sort_values("value", ascending=False) \
        .style.format({"value": '{:.1f}', "Total": '{:.1f}', "Share_of_total": '{:.1f}'})
