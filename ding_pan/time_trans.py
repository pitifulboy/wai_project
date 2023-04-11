# 获取今日盯盘数据
from from_mysql.mysql_table_df import select_today_dp_data

data = select_today_dp_data().sort_values(by=['HM', '股票代码'])
data['Date_HM'] = data['交易时间'].str.slice(0, 19).str.replace('T', ' ').astype('datetime64')
print(data['Date_HM'])
