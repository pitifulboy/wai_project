import requests
import pandas as pd
from sqlalchemy import create_engine

from my_funcs.date_funcs import get_nextyear_firstday
from my_settings import get_my_database_sql
from mytoken_fun import get_my_waizao_token


def get_tradedate_from_waizao(startdate, enddate, mytoken):
    response = requests.get(
        "http://api.waizaowang.com/doc/getTradeDate?mtype=1&startDate=%s&endDate=%s&export=5&token=%s&fields=all" % (
            startdate, enddate, mytoken))
    data = pd.DataFrame(response.json()['data'])
    # ，是否休市:1：半天休市，2：全体休市，3：交易
    data.columns = ["市场类型", "交易时间", "是否休市", "市场名称", "休市原因", "前一个交易日", "后一个交易日"]
    return data


# 预设参数。自动计算完整的交易日期。
def get_tradedate_auto():
    startdate = '2019-01-01'
    # 结束日设置为明年的第一天
    enddate = get_nextyear_firstday()
    mytoken = get_my_waizao_token()

    my_tradedate = get_tradedate_from_waizao(startdate, enddate, mytoken)
    print(my_tradedate)
    return my_tradedate


def update_tradedate_to_mysql():
    df = get_tradedate_auto()
    conn = create_engine(get_my_database_sql(), encoding='utf8')
    df.to_sql('trade_date', con=conn, if_exists='replace', index=False)


update_tradedate_to_mysql()
