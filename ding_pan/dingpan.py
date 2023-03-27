import datetime
import time
import requests
import pandas as pd
from sqlalchemy import create_engine


def get_dingpan_data():
    response = requests.get(
        # 涨幅大于1%
        "http://api.waizaowang.com/doc/getWatchStockTimeKLine?type=1&code=all&export=5&token"
        "=5b98e82a71a2afd3b84c5d14ad192c57&filter=zdfd>1&fields=code,tdate,price,zdfd,zded,cjl,cje,zhfu,hslv,name,"
        "high,low,open,zrspj,zsz,ltsz,ssdate,z50,z52,z53,ztj,dtj")
    data = pd.DataFrame(response.json()['data'])

    print(data.head(5))

    # "zh":["股票代码","交易时间","最新价（元）","涨跌幅度（%）","涨跌额度（元）","成交量（手）","成交额（元）","振幅（%）","换手率（%）","股票名称","最高价（元）","最低价（元）","今日开盘价（元）","昨日收盘价（元）","总市值（元）","流通市值（元）","上市日期","归属行业板块名称","归属地域板块名称","归属概念板块名称","涨停价（元）","跌停价（元）"],"en":["code","tdate","price","zdfd","zded","cjl","cje","zhfu","hslv","name","high","low","open","zrspj","zsz","ltsz","ssdate","z50","z52","z53","ztj","dtj"]

    data.columns = ["股票代码", "交易时间", "最新价（元）", "涨跌幅度（%）", "涨跌额度（元）", "成交量（手）", "成交额（元）", "振幅（%）", "换手率（%）", "股票名称",
                    "最高价（元）", "最低价（元）", "今日开盘价（元）", "昨日收盘价（元）", "总市值（元）", "流通市值（元）", "上市日期", "归属行业板块名称", "归属地域板块名称",
                    "归属概念板块名称", "涨停价（元）", "跌停价（元）"]

    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/waizao_data', encoding='utf8')
    data.to_sql('dingpan', con=conn, if_exists='append', index=False)


def my_loop():
    i = 0
    while i < 10000:
        i = i + 1
        print("第" + str(i) + "次调用")
        get_dingpan_data()
        time.sleep(30)


def check_trade_or_not():
    nowtime = datetime.datetime.now()
    nowtime_hm = nowtime.strftime("%H%M")
    if (915 < int(nowtime_hm) < 1130) or (1300 < int(nowtime_hm) < 1500):
        tradestate = 1
    else:
        tradestate = 0
    return tradestate


def start_dingpan():
    if check_trade_or_not():
        my_loop()
    else:
        print('不在交易时间')


start_dingpan()
