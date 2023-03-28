import pandas as pd
import requests
from pyecharts.charts import Page

from chaoduan_analysis.zt_dt_zb import draw_zt_zb_dt_table, oneday_zt_zb_dt
from dapan_analysis.zdfb import draw_zhangdie_fenbu_bar
from my_funcs.date_funcs import get_today_date
from my_pyecharts.draw_table import draw_table_by_df


def analysis_dingpan(data):
    today_date = get_today_date()

    df_zt = oneday_zt_zb_dt(data, '涨停')

    df_zb = oneday_zt_zb_dt(data, '炸板')
    df_dt = oneday_zt_zb_dt(data, '跌停')

    page = Page(layout=Page.SimplePageLayout)
    page.add(
        # 资金趋势
        draw_zhangdie_fenbu_bar(data),
        draw_table_by_df(df_zt, '涨停个股'),
        draw_table_by_df(df_zb, '炸板个股'),
        draw_table_by_df(df_dt, '跌停个股'),

    )
    page.render(today_date + "盯盘.html")

'''
def get_dingpan_data():
    response = requests.get(

        "http://api.waizaowang.com/doc/getWatchStockTimeKLine?type=1&code=all&export=5&token"
        "=5b98e82a71a2afd3b84c5d14ad192c57&fields=code,tdate,price,zdfd,zded,cjl,cje,zhfu,hslv,name,"
        "high,low,open,zrspj,zsz,ltsz,ssdate,z50,z52,z53,ztj,dtj")
    data = pd.DataFrame(response.json()['data'])
    data.columns = ["股票代码", "交易时间", "最新价（元）", "涨跌幅度（%）", "涨跌额度（元）", "成交量（手）", "成交额（元）", "振幅（%）", "换手率（%）", "股票名称",
                    "最高价（元）", "最低价（元）", "今日开盘价（元）", "昨日收盘价（元）", "总市值（元）", "流通市值（元）", "上市日期", "归属行业板块名称", "归属地域板块名称",
                    "归属概念板块名称", "涨停价（元）", "跌停价（元）"]

    print(data.head(5))
    return data
'''

#analysis_dingpan(get_dingpan_data())
