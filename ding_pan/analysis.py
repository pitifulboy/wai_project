from ding_pan.lastday_data import get_lastday_data
# 获取昨日数据
from from_mysql.mysql_table_column import get_columnlist_from_mysql
from from_mysql.mysql_table_df import select_today_dp_data

df_lastday = get_lastday_data()
# 获取今日盯盘数据
df = select_today_dp_data().sort_values(by=['HM', '股票代码'])

# print(df['HM'].min())

share_list = get_columnlist_from_mysql('dingpan_today', '股票代码')
share_list_len = len(share_list)

df['last_价格'] = df['最新价（元）'].shift(-share_list_len)
df['last_成交额（元）'] = df['成交额（元）'].shift(-share_list_len)
# 分钟涨幅
df['m_chg_pct'] = ((df['last_价格'] - df['最新价（元）']) / df['昨日收盘价（元）']) * 100
df['m_成交额(万）'] = (df['last_成交额（元）'] - df['成交额（元）']) / 10000

print(df.keys())
df_short = df[['股票代码', '跌停价（元）', 'HM', 'last_价格', 'last_成交额（元）', 'm_chg_pct', 'm_成交额(万）']]
# 取第二个时间段开始
print(df_short.head(5))

path = r'D:\00 量化交易\\tttttt.xlsx'
df_short.to_excel(path, sheet_name='1', engine='openpyxl')
