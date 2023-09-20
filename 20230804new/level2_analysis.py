from from_mysql.mysql_table_df import select_share_by_date
from get_level2_data_from_waizao import store_lotsof_level2_data

querydate = '2023-08-11'
data = select_share_by_date(querydate)
print(data)

store_lotsof_level2_data(data['股票代码'].iloc[0:61])

'''querydate_tomorrow = '2023-08-18'
data_tomorrow = select_share_by_date(querydate_tomorrow)
print(data)
'''
# 获取当日的n日涨幅榜，获取其n天前的level2数据

# 8月11日的数据
