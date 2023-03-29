import numpy as np
import pandas as pd
from get_data.cal_gainian import get_gainian_df
from my_pyecharts.draw_table import draw_table_by_df


def bankuai_analysis(tradedata, bk_type):
    # 获取代码-概念 对应关系
    df = get_gainian_df(tradedata)
    # 整理数据
    df_formate = pd.merge(left=df, right=tradedata, how="inner", on='股票代码')
    # 透视分析
    df_povit = pd.pivot_table(df_formate, values=['成交额（元）', '涨跌幅度（%）', '股票代码', '总市值（元）', '流通市值（元）'], index=bk_type,
                              aggfunc={'总市值（元）': np.sum, '流通市值（元）': np.sum, '成交额（元）': np.sum, '涨跌幅度（%）': np.mean,
                                       '股票代码': np.count_nonzero})

    df_povit['总市值（元）'] = df_povit['总市值（元）'] / 100000000
    df_povit['流通市值（元）'] = df_povit['流通市值（元）'] / 100000000
    df_povit['成交额（元）'] = df_povit['成交额（元）'] / 100000000

    df_povit.columns = ['总市值（亿）', '成交额（亿）', '流通市值（亿）', '平均涨幅（%）', '成分股数']
    # 排序。按交易额
    df_povit_sorted = df_povit.sort_values(by='平均涨幅（%）', ascending=False).round(2)
    result = df_povit_sorted.reset_index()

    # 插入编号
    result.insert(0, '序号', range(1, 1 + len(df_povit_sorted)))
    print(result)
    return result


def draw_bk_table(tradedata, bk_type):
    result = bankuai_analysis(tradedata, bk_type)
    table = draw_table_by_df(result.head(10), bk_type)
    return table


# 获取交易数据
'''data = get_dingpan_data()
bankuai_analysis(data, '概念名称')
bankuai_analysis(data, '归属行业板块名称')
bankuai_analysis(data, '归属地域板块名称')'''

# path = r'D:\00 量化交易\\概念分析.xlsx'    result.to_excel(path, sheet_name='1', engine='openpyxl')
