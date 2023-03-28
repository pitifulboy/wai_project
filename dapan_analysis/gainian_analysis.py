import numpy as np
import pandas as pd

from ding_pan.dingpan import get_dingpan_data

# 获取交易数据
from get_data.cal_gainian import get_gainian_df

# 获取交易数据
data = get_dingpan_data()
print(data.keys())
# 获取代码-概念 对应关系
df = get_gainian_df(data)

# 整理数据
df_formate = pd.merge(left=df, right=data, how="inner", on='股票代码')
print(df_formate)

# 透视分析
df_povit = pd.pivot_table(df_formate, values=['成交额（元）', '涨跌幅度（%）', '股票代码', '总市值（元）', '流通市值（元）'], index="概念名称",
                          aggfunc={'总市值（元）': np.sum, '流通市值（元）': np.sum, '成交额（元）': np.sum, '涨跌幅度（%）': np.mean,
                                   '股票代码': np.count_nonzero})

df_povit['总市值（元）'] = df_povit['总市值（元）'] / 100000000
df_povit['流通市值（元）'] = df_povit['流通市值（元）'] / 100000000
df_povit['成交额（元）'] = df_povit['成交额（元）'] / 100000000

df_povit.columns = ['总市值（亿）', '成交额（亿）', '流通市值（亿）', '平均涨幅（%）', '成分股数']
# 排序。按交易额
df_povit_sorted = df_povit.sort_values(by='平均涨幅（%）', ascending=False).round(2)

print(df_povit_sorted)

path = r'D:\00 量化交易\\概念分析.xlsx'
df_povit_sorted.to_excel(path, sheet_name='1', engine='openpyxl')
