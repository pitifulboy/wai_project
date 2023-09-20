import numpy as np
import pandas as pd

from from_mysql.mysql_table_df import select_share_by_date


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

    # path = r'D:\00 量化交易\\概念分析.xlsx'
    # df_code_gn.to_excel(path, sheet_name='1', engine='openpyxl')

    return df_code_gn


def expand_gainian_df(df):
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
    # 将概念数据匹配交易数据
    df_code_gn_merge_trade_data = pd.merge(left=df_code_gn, right=data, on='股票代码', how='inner')

    # path = r'D:\00 量化交易\\概念分析.xlsx'
    # df_code_gn.to_excel(path, sheet_name='1', engine='openpyxl')

    return df_code_gn_merge_trade_data


def analysis_gainian_df(df):
    # 透视,统计上榜次数和金额
    df_povit = pd.pivot_table(df, index=['概念名称', '交易时间'],
                              aggfunc={'股票代码': np.count_nonzero, '成交额（元）': np.sum, '流通市值（元）': np.sum,
                                       '涨跌幅度（%）': np.average})
    # 转换单位，新增列
    df_povit['成交额（亿）'] = df_povit['成交额（元）'] / 100000000
    df_povit['流通市值（亿）'] = df_povit['流通市值（元）'] / 100000000

    # 排序,按照买入交易额降序
    df_povit_sorted = df_povit.sort_values(by='成交额（亿）', ascending=False)
    # 取部分数值
    df_povit_sorted_result = df_povit_sorted[['股票代码', '成交额（亿）', '流通市值（亿）', '涨跌幅度（%）']]
    df_povit_sorted_result.columns = ['股票数量', '成交额（亿）', '流通市值（亿）', '平均涨幅（%）']

    return df_povit_sorted_result.round(2)


querydate = '2023-08-16'
data = select_share_by_date(querydate)
print(expand_gainian_df(data).keys())
df = analysis_gainian_df(expand_gainian_df(data))
print(df)
print(df.sort_values(by='平均涨幅（%）', ascending=False))
