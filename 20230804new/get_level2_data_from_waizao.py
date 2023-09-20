import requests
import pandas as pd
from sqlalchemy import create_engine

from from_mysql.mysql_table_df import select_share_by_date
from my_settings import get_my_database_sql
from mytoken_fun import get_my_waizao_token


# 获取股票一天的数据，不超过50个股。
def get_level2_data_from_waizao(share_code_str='000001', one_date='2023-08-18'):
    mytoken = get_my_waizao_token()
    startdate = one_date + ' 09:30:00'
    enddate = one_date + ' 15:00:00'
    response = requests.get(
        "http://api.waizaowang.com/doc/getLevel2TimeDeal?type=1&code=%s&startDate=%s&endDate=%s&export=5&token=%s&fields=code,tdate,price,cjl" % (
            share_code_str, startdate, enddate, mytoken))
    data = pd.DataFrame(response.json()['data'])
    data.columns = ["股票代码", "分时时间", "成交价", "成交量（手）"]
    # print(data)
    return data


def store_level2_data_to_mysql(data):
    conn = create_engine(get_my_database_sql(), encoding='utf8')
    data.to_sql('level2_data', con=conn, if_exists='append', index=False)


# get_level2_data_from_waizao()
def store_lotsof_level2_data(df_series):
    # 每次获取个股数量
    step_len = 8
    loop_times = len(df_series) // step_len + 1
    print(loop_times)
    for i in range(0, loop_times):
        code_list_str = ','.join(df_series.iloc[step_len * i:step_len * i + step_len])
        print(code_list_str)
        store_level2_data_to_mysql(get_level2_data_from_waizao(share_code_str=code_list_str))


''')
store_lotsof_level2_data(data['股票代码'].iloc[0:61])
'''
