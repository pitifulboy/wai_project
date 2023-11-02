import time
from datetime import datetime
from pydoc import text

import numpy as np
import datetime
import time
import requests
import pandas as pd
from pyecharts.charts import Page
from sqlalchemy import create_engine

from from_mysql.judge_table_exist import check_table_exist
from from_mysql.mysql_table_column import get_columnlist_from_mysql, get_max_from_mysql

# 首次获取盯盘数据，获取全部信息。
from my_pyecharts.draw_table import draw_table_by_df
from my_settings import get_my_database_sql
from mytoken_fun import get_my_waizao_token


def get_dingpan_data_full():
    mytoken = get_my_waizao_token()

    response = requests.get(
        "http://api.waizaowang.com/doc/getWatchStockTimeKLine?type=1&code=all&export=5&token=" + mytoken + "&fields=code,tdate,price,zdfd,zded,cjl,cje,zhfu,hslv,name,"
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
    today_date = get_today_date_str()
    # 数据库表名称：日期+盯盘。例如20230509dingpan
    dingpan_table_name = today_date + "dingpan"

    # 循环
    t = 0
    while t < 9999:

        # 判断当前时间的交易状态
        trade_type = check_trade_time()
        if trade_type == "开市前" or trade_type == "集合竞价":
            # 休息60秒
            time.sleep(60)
            print("未开市")

        elif trade_type == "上午竞价" or trade_type == "下午竞价":
            # 获取交易数据
            df_first = get_dingpan_data_full()
            df_first_part = df_first[["股票代码", "交易时间", "最新价（元）", "涨跌幅度（%）", "成交额（元）", 'Date_HM']]
            # 获取首次获取数据的时间
            time_first = df_first_part['Date_HM'].mean()

            # 首次调用，历史数据使用数据库数据。非首次，使用保留的上次数据，计算区间数据。
            print(t)
            if t == 0:
                print("首次调用")
                # 判断表是否存在，如果存在，从mysql中获取数据
                if check_table_exist(dingpan_table_name):
                    # 获取数据库最新时间
                    df_all_from_mysql = get_all_minute_data_from_mysql(dingpan_table_name)
                    mysql_max_Date_HM = df_all_from_mysql['Date_HM'].max()
                    # 将数据库中的数据汇总。作为历史数据
                    df_history = deal_all_minute_date(df_all_from_mysql)
                    # 判断最新数据是否在数据库中。
                    if mysql_max_Date_HM == time_first:
                        print(str(time_first) + "分钟数据已经存在")
                    else:
                        # 生成区间数据
                        df_period = calculate_data_between_times(df_history, df_first_part)
                        # 将区间数据，写入数据库中。
                        write_minute_data_to_mysql(df_period.round(2), dingpan_table_name)
                else:
                    # 将区间数据，写入数据库中。
                    write_minute_data_to_mysql(df_first_part, dingpan_table_name)

                # 将最新数据保存。
                df_history = df_first_part

            else:
                # 非首次调用,计算区间交易数据
                # 判断数据是否更新
                print("非首次调用")
                time_history = df_history['Date_HM'].mean()
                if time_history == time_first:
                    print(str(time_first) + "分钟数据已经存在")
                else:
                    df_period = calculate_data_between_times(df_history, df_first_part)
                    # 写入最新数据
                    write_minute_data_to_mysql(df_period.round(2), dingpan_table_name)
                    # 分析数据
                    analysis_minute_data(dingpan_table_name)
                    # 更新历史数据
                    df_history = df_first_part

            t = t + 1
            time.sleep(20)


        else:
            print("其他时间")
            time.sleep(15)


# 根据时间，判断交易状态
def check_trade_time():
    nowtime = datetime.datetime.now()
    nowtime_hm = nowtime.strftime("%H%M")
    if int(nowtime_hm) < 915:
        trade_type = "开市前"
    elif 915 <= int(nowtime_hm) < 930:
        trade_type = "集合竞价"
    elif 930 <= int(nowtime_hm) < 1130:
        trade_type = "上午竞价"
    elif 1130 <= int(nowtime_hm) < 1300:
        trade_type = "中午休息"
    elif 1300 <= int(nowtime_hm) < 1541:
        trade_type = "下午竞价"
    else:
        trade_type = "其他时间"
    return trade_type


# 将数据写入指定表种。
def write_minute_data_to_mysql(df, tablename):
    conn = create_engine(get_my_database_sql(), encoding='utf8')
    df.to_sql(tablename, con=conn, if_exists='append', index=False)


# 获取当日全部数据
def get_all_minute_data_from_mysql(tablename):
    conn = create_engine(get_my_database_sql(), encoding='utf8')
    mysql_1 = "SELECT  * FROM " + tablename
    df = pd.read_sql(mysql_1, conn)
    return df


# 计算区间数据
def calculate_data_between_times(df_first, df_last):
    df_merge = pd.merge(left=df_first, right=df_last, on='股票代码')
    # 计算中间时间的数据.
    df_merge['成交额（元）'] = df_merge['成交额（元）_y'] - df_merge['成交额（元）_x']
    df_merge["涨跌幅度（%）"] = df_merge['涨跌幅度（%）_y'] - df_merge['涨跌幅度（%）_x']
    df_to_sql = df_merge[["股票代码", "交易时间_y", "最新价（元）_y", "涨跌幅度（%）", "成交额（元）", 'Date_HM_y']]
    df_to_sql.columns = ["股票代码", "交易时间", "最新价（元）", "涨跌幅度（%）", "成交额（元）", 'Date_HM']
    return df_to_sql


# povit minute data 透视分钟数据
def deal_all_minute_date(df):
    df_povit = pd.pivot_table(df, index='股票代码',
                              values=['交易时间', '最新价（元）', '涨跌幅度（%）', '成交额（元）', 'Date_HM'],
                              aggfunc={'交易时间': np.max, '最新价（元）': np.mean, '涨跌幅度（%）': np.sum,
                                       '成交额（元）': np.sum, 'Date_HM': np.max})
    df_new = df_povit.reset_index()
    df_result = df_new[['股票代码', '交易时间', '最新价（元）', '涨跌幅度（%）', '成交额（元）', 'Date_HM']]

    return df_result


# 分析数据
def analysis_minute_data(tablename):
    df_now = get_dingpan_data_full()

    # 1分钟，3分钟，5分钟，10分钟，30分钟涨幅榜
    # 获取全部分钟数据
    df_from_mysql = get_all_minute_data_from_mysql(tablename)
    time_list = df_from_mysql['Date_HM'].sort_values(ascending=True).drop_duplicates().tolist()
    print(time_list)
    minute_list = [1, 3, 10]
    # 根据存在的数据，选择性计算
    if len(time_list) < 3:
        minute_list = [1]
    elif len(time_list) < 11:
        minute_list = [1, 3]
    # 加载到pyecharts上
    page = Page(layout=Page.SimplePageLayout)

    for minute in minute_list:
        #  1分钟榜，聚焦快速上涨
        if minute == 1:
            df_mins = df_from_mysql[df_from_mysql['Date_HM'] == time_list[-1]]
        else:
            # 几分钟榜单
            df_min_peroid = df_from_mysql[df_from_mysql['Date_HM'].isin(time_list[-minute - 1:-1])]
            df_mins = deal_all_minute_date(df_min_peroid)

        result = df_mins.sort_values(by='涨跌幅度（%）', ascending=False).head(10)
        # 完善数据
        result_full = pd.merge(left=result, right=df_now, on='股票代码', how='left')
        # 筛选上涨个股
        result_full_up = result_full[result_full['涨跌幅度（%）_y'] > 0]
        # 筛选部分数据
        result_selected = result_full_up[
            ['股票代码', '涨跌幅度（%）_x', '涨跌幅度（%）_y', '股票名称', '流通市值（元）', '归属行业板块名称', 'Date_HM_y']].copy()
        result_selected['流通市值（元）'] = result_selected['流通市值（元）'] / 100000000
        result_selected.columns = ['股票代码', '区间涨幅', '今日涨幅', '股票名称', '流通市值（亿）', '归属行业板块名称', '时间']

        min_table = draw_table_by_df(result_selected.round(2), str(minute) + '分涨幅榜')
        # 加载到page中
        page.add(min_table)

    page.render("盯盘.html")
    print('盯盘数据已经分析完毕')

    # 涨停，炸板，跌停榜单
    # 量比榜单。交易量与昨日占比榜
    # 板块涨幅榜单


# 删除表
def delete_table_dingpan_minute_data():
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/waizao_data', encoding='utf8')
    sql = 'DROP TABLE IF EXISTS dingpan_minute_data;'
    conn.execute(sql)


# 根据时间，判断交易状态
def get_today_date_str():
    my_today = datetime.datetime.now().strftime("%Y%m%d")
    return my_today


dingpan_time_flow()
