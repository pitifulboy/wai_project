# 指定日期，获取指定日期（包含）前n天的交易数据。
from from_mysql.mysql_table_column import get_max_from_mysql
from from_mysql.mysql_table_df import select_share_by_start_end, select_trade_date
from my_funcs.date_funcs import get_today_date, generate_tradedate_df
from my_pyecharts.draw_table import draw_table_by_df


# 指定开始交易日和结束交易日
def cal_GB_start_end(startdate, endate):
    # 获取日期内的交易数据
    df = select_share_by_start_end(startdate, endate)
    # 最后一天的交易个股list

    analy = df.groupby(['股票代码', "股票名称", "归属行业板块名称", "归属地域板块名称", "上市日期"]).agg(
        {"总市值（元）": "mean", "流通市值（元）": "mean", "涨跌幅度（%）": "sum", "成交额（元）": "mean"})

    analy["总市值（元）"] = analy["总市值（元）"] / 100000000
    analy["流通市值（元）"] = analy["流通市值（元）"] / 100000000
    analy["成交额（元）"] = analy["成交额（元）"] / 100000000

    analy.columns = ["平均市值", "平均流值", "累计涨幅", "平均成交额"]

    # 排序

    analy_sorted = analy.sort_values(by="累计涨幅", ascending=False)
    result = analy_sorted.reset_index().round(2)

    print(startdate + "日-" + endate + '日,最大涨幅统计如下：')
    print(result)

    return result


def newest_GB(ndays):
    # 获取最新的交易日期
    max_tradedate = get_max_from_mysql('daily_market', '交易时间')
    # 计算交易日历
    df_tradedate = generate_tradedate_df(max_tradedate, ndays)
    # 计算最早交易日
    min_tradedate = df_tradedate['交易时间'].min()
    # 计算高标数据
    result = cal_GB_start_end(min_tradedate, max_tradedate)
    # 插入编号
    result.insert(0, '序号', range(1, 1 + len(result)))

    # 保存数据
    # path = r'D:\00 量化交易\\' + max_tradedate + '日'+str(ndays)+'天高标动态.xlsx'
    # 取2位小数，并导出数据
    # result.head(100).round(2).to_excel(path, sheet_name='1', engine='openpyxl')

    # 绘制图表
    table = draw_table_by_df(result.head(100), max_tradedate + '日，' + str(ndays) + '天高标动态')
    return table




# print(newest_GB(3))
