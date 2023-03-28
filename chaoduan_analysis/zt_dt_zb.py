# 今日涨停，炸板，跌停，涨幅超过10%
import pandas as pd

from from_mysql.mysql_table_df import select_share_by_date
from my_pyecharts.draw_table import draw_table_by_df


def oneday_zt_zb_dt(data, ana_type):
    global result

    # 调整格式.成交额，流通市值
    data['成交额（亿）'] = (data['成交额（元）'] / 100000000).round(2)
    data['流通市值（亿）'] = (data['流通市值（元）'] / 100000000).round(2)

    # 剔除未交易的数据
    df_trade = data[data['最新价（元）'] > 0]
    # 触板（含涨停和炸板）
    df_cb = df_trade.loc[df_trade['最高价（元）'] == df_trade['涨停价（元）']]

    if ana_type == '涨停':
        # 涨停，最高价=涨停价
        result = df_cb.loc[df_cb['最新价（元）'] == df_cb['涨停价（元）']]
    elif ana_type == '炸板':
        # 炸板。最高价=涨停价，收盘价<>涨停价
        result = df_cb.loc[df_cb['最新价（元）'] != df_cb['涨停价（元）']]
    elif ana_type == '跌停':
        # 跌停。收盘价=跌停价
        result = df_trade.loc[df_trade['最新价（元）'] == df_trade['跌停价（元）']]
    elif ana_type == '全部':
        result = df_trade

    # 修改列名称

    result = result.loc[:,
             ["交易时间", "股票代码", "股票名称", "涨跌幅度（%）", "振幅（%）", "换手率（%）", "成交额（亿）", "流通市值（亿）", "上市日期", "归属行业板块名称",
              "归属地域板块名称"]]

    # 排序
    result = result.sort_values(by=["涨跌幅度（%）", "成交额（亿）"], ascending=False)
    # 插入编号
    result.insert(0, '序号', range(1, 1 + len(result)))

    return result


def draw_zt_zb_dt_table(data, ana_type):

    # 计算
    result = oneday_zt_zb_dt(data, ana_type)
    # 画表
    table = draw_table_by_df(result,  ana_type)
    return table


'''today = get_today_date()
oneday_zt_zb_dt(today, '涨停')'''
# oneday_zt_zb_dt('2022-06-02', '涨停')
