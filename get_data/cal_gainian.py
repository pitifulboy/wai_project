import pandas as pd
from sqlalchemy import create_engine

from ding_pan.dingpan import get_dingpan_data


def get_gainian_df(df):
    # 代码
    df_code = df["股票代码"]
    # 概念
    df_gn = df["归属概念板块名称"].str.split(",", expand=True).fillna("")
    # 生成  代码，概念  的df

    result = pd.concat([df_code, df_gn], axis=1)
    mylist = result.values

    new_list = []
    for i in range(0, len(mylist)):
        code = mylist[i][0]
        for j in range(1, len(mylist[i])):
            if mylist[i][j] != "":
                new_list.append([code, mylist[i][j]])

    df_code_gn = pd.DataFrame(new_list, columns=["股票代码", "概念名称"])

    return df_code_gn
