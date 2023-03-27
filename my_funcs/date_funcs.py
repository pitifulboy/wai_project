# 获取今天的日期
import pandas as pd

from from_mysql.mysql_table_df import select_trade_date


def get_today_date():
    # 今天
    today_1 = pd.Timestamp.now()
    today_tushare_format = today_1.strftime('%Y-%m-%d')
    date_str = today_tushare_format

    return date_str


# 指定起始结束日期，生成日期list
def generate_datelist_by_start_end(startdate, enddate):
    t = pd.period_range(start=startdate, end=enddate)
    new_list = []
    for i in range(0, len(t)):
        new_list.append(t[i].strftime('%Y-%m-%d'))

    return new_list


# print(generate_datelist_by_start_end('2023-01-01', '2023-03-03'))

# 生产交易日期list
def generate_tradedate_df(maxdate, ndays):
    df_tradedate = select_trade_date()
    df_tradedate_open = df_tradedate[df_tradedate['is_open'] == 1]
    df_tradedate_remain = df_tradedate_open[df_tradedate_open['cal_date'] <= maxdate]
    df_tradedate_remain_result = df_tradedate_remain[-ndays:]
    return df_tradedate_remain_result
