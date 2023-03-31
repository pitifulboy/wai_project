# 获取近2日分钟线。分析超短数据
# 1，分析当日分钟线。当日涨幅>5%(最大涨幅>5%)
from sqlalchemy import create_engine

from from_mysql.mysql_table_df import select_share_by_date
import requests
import pandas as pd

date = '2023-03-28'
data = select_share_by_date(date)
# 最大涨幅
df_zhangfu = data.sort_values(by='涨跌幅度（%）', ascending=False)

df_500 = df_zhangfu.head(500)
codelist = df_500['股票代码'].tolist()
print(codelist)

for i in range(0, 10):
    mylist = codelist[0 + i * 50:50 + i * 50]
    str = ','.join(mylist)
    print(str)

    response = requests.get(
        "http://api.waizaowang.com/doc/getMinuteKLine?type=1&code=" + str + "&startDate=2023-03-29&endDate=2023-03-30&export=5&token=5b98e82a71a2afd3b84c5d14ad192c57&fields=all");
    data = pd.DataFrame(response.json()['data'])
    print(data)

    data.columns = ["股票代码", "分时时间", "开盘价", "收盘价", "最高价", "最低价", "成交量（手）", "成交额（元）", "成交均价"]

    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/waizao_data', encoding='utf8')
    data.to_sql('minute_data', con=conn, if_exists='append', index=False)
