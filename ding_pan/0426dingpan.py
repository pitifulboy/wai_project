import time
from datetime import datetime

import numpy as np
import pandas as pd
import requests
import datetime
import time
import requests
import pandas as pd
from sqlalchemy import create_engine

from from_mysql.judge_table_exist import check_table_exist
from from_mysql.mysql_table_column import get_columnlist_from_mysql, get_max_from_mysql


# 首次获取盯盘数据，获取全部信息。
def get_dingpan_data_full():
    response = requests.get(
        "http://api.waizaowang.com/doc/getWatchStockTimeKLine?type=1&code=all&export=5&token"
        "=5b98e82a71a2afd3b84c5d14ad192c57&fields=code,tdate,price,zdfd,zded,cjl,cje,zhfu,hslv,name,"
        "high,low,open,zrspj,zsz,ltsz,ssdate,z50,z52,z53,ztj,dtj")
    data = pd.DataFrame(response.json()['data'])
    data.columns = ["股票代码", "交易时间", "最新价（元）", "涨跌幅度（%）", "涨跌额度（元）", "成交量（手）", "成交额（元）", "振幅（%）", "换手率（%）", "股票名称",
                    "最高价（元）", "最低价（元）", "今日开盘价（元）", "昨日收盘价（元）", "总市值（元）", "流通市值（元）", "上市日期", "归属行业板块名称", "归属地域板块名称",
                    "归属概念板块名称", "涨停价（元）", "跌停价（元）"]

    data['Date_HM'] = data['交易时间'].str.slice(11, 17).str.replace(':', '').astype('int')
    # 筛选价格为正
    df_trade = data[data['最新价（元）'] > 0]

    # print(df_trade.head(5))
    return df_trade


# 非首次获取盯盘数据，获取筛选后的数据
def get_dingpan_data_part():
    response = requests.get(
        "http://api.waizaowang.com/doc/getWatchStockTimeKLine?type=1&code=all&export=5&token"
        "=5b98e82a71a2afd3b84c5d14ad192c57&fields=code,tdate,price,zdfd,cje")
    data = pd.DataFrame(response.json()['data'])
    data.columns = ["股票代码", "交易时间", "最新价（元）", "涨跌幅度（%）", "成交额（元）"]
    data['Date_HM'] = data['交易时间'].str.slice(11, 17).str.replace(':', '').astype('int')
    # 筛选价格为正
    df_trade = data[data['最新价（元）'] > 0]

    print(df_trade.head(5))
    return df_trade


# 盯盘开始

def dingpan_time_flow():
    trade_type = check_trade_time()
    # 判断是否集合竞价。竞价异动时间 9:20-9:25
    if trade_type == "集合竞价":
        pass

    elif trade_type == "上午竞价" or trade_type == "下午竞价":
        print(trade_type)
        # 正在交易中
        df_first = get_dingpan_data_full()
        df_first_info = df_first[["股票代码", "昨日收盘价（元）", "总市值（元）", "流通市值（元）", "上市日期", "归属行业板块名称", "归属地域板块名称",
                                  "归属概念板块名称", "涨停价（元）", "跌停价（元）"]]
        df_first_part = df_first[["股票代码", "交易时间", "最新价（元）", "涨跌幅度（%）", "成交额（元）", 'Date_HM']]
        # 判断数据是否存在，如果不存在写入mysql
        # 判断表是否存在，如果存在，从mysql中获取时间
        if check_table_exist("dingpan_minute_data"):
            mysql_max_Date_HM = get_max_from_mysql("dingpan_minute_data", 'Date_HM')
            time_first = df_first_part['Date_HM'].mean()
            if mysql_max_Date_HM != time_first:
                # 如果存在数据，首次写入的数据需要处理。
                # 获取数据库全部数据，计算前面数据之和。todo
                df_from_mysql = deal_all_minute_date()
                df_period=calculate_data_between_times(df_from_mysql, df_first_part)

                write_minute_data_to_mysql(df_period)
            else:
                print(str(time_first) + "分钟数据已经存在")
        else:
            # 表不存在，直接写入数据
            write_minute_data_to_mysql(df_first_part)

        # 循环获取数据：
        i = 0
        while i < 99999:
            # 间隔30秒再获取数据
            time.sleep(30)
            df_latest_part = get_dingpan_data_part()

            # 根据数据中的时间，判断数据是否重复
            time_first = df_first_part['Date_HM'].mean()
            time_latest = df_latest_part['Date_HM'].mean()
            if time_latest == time_first:
                print('数据未更新')
            else:
                # 将新旧数据汇总
                df_to_sql = calculate_data_between_times(df_first_part, df_latest_part)
                write_minute_data_to_mysql(df_to_sql.round(2))
                # 计算两者之间的交易数据
                # analysis_minute_data(df_first_info)
            i = i + 1
            # 更新前值数据。
            df_first_part = df_latest_part

    else:
        print("其他时间")
        time.sleep(15)


# 分析数据
def analysis_minute_data(df_first_info):
    # 1分钟，3分钟，5分钟，10分钟，30分钟涨幅榜
    # 涨停，炸板，跌停榜单
    # 量比榜单。交易量与昨日占比榜
    # 板块涨幅榜单
    pass


def check_trade_time():
    nowtime = datetime.datetime.now()
    nowtime_hm = nowtime.strftime("%H%M")
    if 919 < int(nowtime_hm) < 926:
        trade_type = "集合竞价"
    elif 929 < int(nowtime_hm) < 1131:
        trade_type = "上午竞价"
    elif 1259 < int(nowtime_hm) < 1501:
        trade_type = "下午竞价"
    else:
        trade_type = "其他时间"
    return trade_type


def write_minute_data_to_mysql(df):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/waizao_data', encoding='utf8')
    df.to_sql('dingpan_minute_data', con=conn, if_exists='append', index=False)


def get_all_minute_data_from_mysql():
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/waizao_data', encoding='utf8')
    mysql_1 = "SELECT  * FROM dingpan_minute_data "
    df = pd.read_sql(mysql_1, conn)
    return df


def calculate_data_between_times(df_first, df_last):
    df_merge = pd.merge(left=df_first, right=df_last, on='股票代码')
    # 计算中间时间的数据.
    df_merge['成交额（元）'] = df_merge['成交额（元）_y'] - df_merge['成交额（元）_x']
    df_merge["涨跌幅度（%）"] = df_merge['涨跌幅度（%）_y'] - df_merge['涨跌幅度（%）_x']
    df_to_sql = df_merge[["股票代码", "交易时间_y", "最新价（元）_y", "涨跌幅度（%）", "成交额（元）", 'Date_HM_y']]
    df_to_sql.columns = ["股票代码", "交易时间", "最新价（元）", "涨跌幅度（%）", "成交额（元）", 'Date_HM']
    return df_to_sql


def deal_all_minute_date():
    df = get_all_minute_data_from_mysql()
    df_povit = pd.pivot_table(df, index='股票代码',
                              values=['交易时间', '最新价（元）', '涨跌幅度（%）', '成交额（元）', 'Date_HM'],
                              aggfunc={'交易时间': np.max, '最新价（元）': np.mean, '涨跌幅度（%）': np.sum,
                                       '成交额（元）': np.sum, 'Date_HM': np.max})
    df_new = df_povit.reset_index()
    df_result = df_new[['股票代码', '交易时间', '最新价（元）', '涨跌幅度（%）', '成交额（元）', 'Date_HM']]

    return df_result


dingpan_time_flow()

