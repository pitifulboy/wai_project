# 分析指定群组的个股集合
from from_mysql.mysql_table_df import select_share_by_date

date = '2023-10-20'
data = select_share_by_date(date)
print(data)
print(data.keys())

# 指定分析对象。
# 指定分析周期
# 获取周期内交易数据。
# 提取待分析数据

# 根据"概念板块名称"，提取待分析的概念板块。
