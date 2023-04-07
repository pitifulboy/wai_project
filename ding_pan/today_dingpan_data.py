import datetime
import time
import requests
import pandas as pd
from sqlalchemy import create_engine

from from_mysql.mysql_table_column import get_columnlist_from_mysql


# 获取盯盘数据
def get_dingpan_data():
    # 简化数据内容，不需要个股的固有属性
    response = requests.get(
        "http://api.waizaowang.com/doc/getWatchStockTimeKLine?type=1&code=all&export=5&token"
        "=5b98e82a71a2afd3b84c5d14ad192c57&fields=code,tdate,price,cjl,cje,open,zrspj,ztj,dtj")
    data = pd.DataFrame(response.json()['data'])
    data.columns = ["股票代码", "交易时间", "最新价（元）", "成交量（手）", "成交额（元）", "今日开盘价（元）", "昨日收盘价（元）", "涨停价（元）", "跌停价（元）"]
    # 整理时间，新增HM列（时分）
    data['HM'] = data['交易时间'].str.slice(11, 16).str.replace(':', '').astype('int')
    print(data.head(5))
    return data


# 将数据写入mysql
def write_to_mysql(data):
    # 判断HM是否重复，如果重复，则不写入
    HM = int(data['HM'].mean())
    HM_list = get_columnlist_from_mysql('dingpan_today', 'HM')
    print(HM_list)
    # 清空表，不要删除表
    if len(HM_list) == 0 or HM not in HM_list:
        print("正在写入" + str(HM) + "分钟数据")
        # 获取今日数据，计算最新一分钟内的交易额
        conn = create_engine('mysql+pymysql://root:123456@localhost:3306/waizao_data', encoding='utf8')
        data.to_sql('dingpan_today', con=conn, if_exists='append', index=False)

    else:
        print(str(HM) + "分钟数据已经存在")


# 开始盯盘
def start_dingpan():
    # todo 首次调用时，删除表
    i = 0
    while i < 2000:
        if check_trade_or_not():
            print("第" + str(i) + "次调用")
            data = get_dingpan_data()
            write_to_mysql(data)
            print('正在计算最新数据')
            # 分析计算
            # TODO 判断数据是否存在，如果存在，则不更新。采样间隔60秒
            # TODO：
            print('计算完成')
            time.sleep(30)
        else:
            print('不在交易时间')
            time.sleep(60)
        i = i + 1


# 判断本机时间，是否已经开市
def check_trade_or_not():
    nowtime = datetime.datetime.now()
    nowtime_hm = nowtime.strftime("%H%M")
    if (915 < int(nowtime_hm) < 1131) or (1259 < int(nowtime_hm) < 1500):
        tradestate = 1
    else:
        tradestate = 0
    return tradestate


start_dingpan()
