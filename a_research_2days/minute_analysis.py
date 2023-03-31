import pandas as pd
from pyecharts.charts import Page

from from_mysql.mysql_table_df import select_share_by_date, select_minute_data
from mytestfolderr.mykline import draw_charts, split_data

date = '2023-03-28'
# 获取当日交易数据，以便筛选数据，减小数据量。
data = select_share_by_date(date)
# 最大涨幅
df_zhangfu = data.sort_values(by='涨跌幅度（%）', ascending=False)
# 按照当日涨幅，保留最大涨幅的top500个
df_500 = df_zhangfu.head(500)
print(df_500.keys())
codelist = df_500['股票代码'].tolist()
print(codelist)

# 获取分钟数据
minute_data = select_minute_data()
# 拆分时间字段，获取日期和时间。
print(minute_data.head(5))
df_date = minute_data['分时时间'].str.split('T', expand=True)
df_date.columns = ['日期', '时间']
df_time = df_date['时间'].str.split('.', expand=True)
df_time.columns = ['时间', '秒']
print(df_date.head(5))
print(df_time.head(5))

result = pd.concat([minute_data, df_date['日期'], df_time['时间']], axis=1)

# 按日期，个股查询
re_df_date = result[result['日期'] == '2023-03-28']

re_df_date['时间'] = re_df_date['时间'].str.replace(':', '').astype('int')
re_df_date['成交额（元）'] = re_df_date['成交额（元）'] / 100000

chart_list = []
for i in range(0, 50):
    # 个股信息
    this_share = codelist[i]
    # 个股交易信息
    print(df_500[df_500['股票代码'] == this_share])
    df_this_share = re_df_date[re_df_date['股票代码'] == this_share]

    df_draw = df_this_share.loc[:, ['时间', '开盘价', '收盘价', '最高价', '最低价', '成交额（元）']].values.tolist()

    print(df_draw)

    chart_data = split_data(data=df_draw)
    mygrid = draw_charts(chart_data, this_share)
    chart_list.append(mygrid)





