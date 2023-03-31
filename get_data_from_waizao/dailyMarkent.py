import time
import requests
import pandas as pd
from sqlalchemy import create_engine
from from_mysql.mysql_table_column import get_columnlist_from_mysql
from my_funcs.date_funcs import get_today_date, generate_datelist_by_start_end
from mytoken.token_str import get_waizao_token


def judge_update_or_not(update_date):
    # 判断查询日期的数据是否存在
    # 获取存在的交易日
    tdate_list = get_columnlist_from_mysql('daily_market', '交易时间')
    if update_date in tdate_list:
        print(update_date + "日，数据已经存在")
    else:
        print(update_date + "日，数据更新中")
        update_daily_market(update_date, update_date)


# 直接调用
def update_daily_market(startdate, enddate):
    mytoken = get_waizao_token()

    response = requests.get(
        "http://api.waizaowang.com/doc/getDailyMarket?type=1&code=all&startDate=" + startdate + "&endDate=" + enddate + "&export=5&token=" + mytoken + "&fields=code,tdate,price,zdfd,cjl,cje,hslv,dsyl,name,zgj,zdj,jrkpj,zrspj,zsz,ltsz,ssdate,zgb,ltgb,z50,z52,z53,z197,ztj,dtj,zhfu")

    data = pd.DataFrame(response.json()['data'])

    if len(data) == 0:
        print(startdate + '日，无交易数据')
    else:
        data.columns = ["股票代码", "交易时间", "最新价（元）", "涨跌幅度（%）", "成交量（手）", "成交额（元）", "换手率（%）", "市盈率（动态）",
                        "股票名称", "最高价（元）", "最低价（元）", "今日开盘价（元）", "昨日收盘价（元）", "总市值（元）", "流通市值（元）", "上市日期",
                        "总股本（股）", "流通股本（股）", "归属行业板块名称", "归属地域板块名称", "归属概念板块名称", "行业代码", "涨停价（元）",
                        "跌停价（元）", "振幅（%）"]

        print(data.head(5))
        conn = create_engine('mysql+pymysql://root:123456@localhost:3306/waizao_data', encoding='utf8')
        data.to_sql('daily_market', con=conn, if_exists='append', index=False)


# 按日调用。
def update_daily_market_by_datelist(startdate, enddate):
    datelist = generate_datelist_by_start_end(startdate, enddate)
    for i in datelist:
        judge_update_or_not(i)
        # 调用一次休息
        time.sleep(15)


# 更新到今天
def update_daily_market_to_today():
    tdate_list = get_columnlist_from_mysql('daily_market', '交易时间')
    max_date = tdate_list[-1]
    today = get_today_date()
    update_daily_market_by_datelist(max_date, today)


# 指定日期更新
# update_daily_market_by_datelist('2022-06-01', '2023-03-23')

# update_daily_market_to_today()

# update_daily_market('2022-06-01', '2022-06-01')
