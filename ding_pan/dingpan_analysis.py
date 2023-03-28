from pyecharts.charts import Page

from dapan_analysis.zdfb import draw_zhangdie_fenbu_bar
from from_mysql.mysql_table_df import select_dingpan
from my_funcs.date_funcs import get_today_date


def analysis_dingpan(data):
    today_date = get_today_date()

    page = Page(layout=Page.SimplePageLayout)
    page.add(
        # 资金趋势
        draw_zhangdie_fenbu_bar(data)

    )
    page.render(today_date + "盯盘.html")
