# 选出一天的所有交易数据
import pandas as pd
from sqlalchemy import create_engine


# 按交易日获取daily_market中数据
def select_share_by_date(tradedate):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/waizao_data', encoding='utf8')
    mysql = "SELECT  * FROM daily_market WHERE `交易时间` = '" + tradedate + "' "
    df = pd.read_sql(mysql, conn)
    return df


# 按交易日，筛选类型，获取daily_market中数据
def select_share_by_startdate_type(startdate, querytype):
    global mysql
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/waizao_data', encoding='utf8')

    if querytype == '涨停':
        mysql = "SELECT  * FROM daily_market WHERE `交易时间` >= '" + startdate + "' AND `最新价（元）` = `涨停价（元）` AND `最新价（元）` > 0  "

    df = pd.read_sql(mysql, conn)
    return df


# 按起始日结束日,获取daily_market中数据
def select_share_by_start_end(startdate, enddate):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/waizao_data', encoding='utf8')
    mysql = "SELECT  * FROM daily_market WHERE `交易时间` >= '" + startdate + "' AND `交易时间` <= '" + enddate + "'"
    df = pd.read_sql(mysql, conn)
    return df


# print(select_share_by_start_end('2023-03-20', '2023-03-22'))


# 获取dingpan中数据
def select_dingpan():
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/waizao_data', encoding='utf8')
    mysql_1 = "SELECT  * FROM dingpan "
    df = pd.read_sql(mysql_1, conn)
    return df


# 获取dingpan中数据
def select_amount():
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/waizao_data', encoding='utf8')
    mysql_1 = "SELECT  * FROM result_daily_amount "
    df = pd.read_sql(mysql_1, conn)
    return df


# 获取trade_date中数据
def select_trade_date():
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/waizao_data', encoding='utf8')
    mysql_1 = "SELECT  * FROM trade_date "
    df = pd.read_sql(mysql_1, conn)
    return df

