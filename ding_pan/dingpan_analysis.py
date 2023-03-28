from pyecharts.charts import Page

from chaoduan_analysis.zt_dt_zb import draw_zt_zb_dt_table
from dapan_analysis.zdfb import draw_zhangdie_fenbu_bar
from my_funcs.date_funcs import get_today_date


def analysis_dingpan(data):
    today_date = get_today_date()

    page = Page(layout=Page.SimplePageLayout)
    page.add(
        # 资金趋势
        draw_zhangdie_fenbu_bar(data),
        draw_zt_zb_dt_table(data, '涨停'),
        draw_zt_zb_dt_table(data, '炸板'),
        draw_zt_zb_dt_table(data, '跌停'),

    )
    page.render(today_date + "盯盘.html")
