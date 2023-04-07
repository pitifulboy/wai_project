# 获取昨日的交易数据。方便后续分析
# 主要根据盯盘异动分析。
from from_mysql.mysql_table_df import select_trade_date, select_share_by_date
from my_funcs.date_funcs import get_today_date


def get_lastday_data():
    # 交易日时，获取当天日期
    today_date = get_today_date()
    # 获取交易日历
    trade_cal = select_trade_date()
    # 获取当前交易日
    df_today_date = trade_cal[trade_cal['cal_date'] == today_date]
    last_trade_date = df_today_date['pretrade_date'].tolist()[0]
    # 获取上个交易日的交易数据
    data_lastday = select_share_by_date(last_trade_date)
    #print(data_lastday.keys())
    df_lastday = data_lastday[['股票代码', '交易时间', '成交量（手）', '股票名称', '上市日期', '流通股本（股）']]
    # print(df_lastday)
    return df_lastday


#print(get_lastday_data())
