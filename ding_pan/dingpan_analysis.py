# df['time'] = df['datetime'].str[11:]
from from_mysql.mysql_table_df import select_dingpan

df = select_dingpan()
# 调整时间格式
df['timeint'] = df['交易时间'].str[11:19].str.replace(':', '').astype('int32')
print(df)
