# 将多个图表在同一个网页展示

from pyecharts.charts import Bar, Grid, Page, Tab

from chaoduan_analysis.lian_ban import draw_lbtt
from chaoduan_analysis.zt_dt_zb import oneday_zt_zb_dt, draw_zt_zb_dt_table
from dapan_analysis.zdfb import draw_zhangdie_fenbu_bar
from dapan_analysis.zjqs import draw_pic_amounts
from dapan_analysis.zjqs_cal import update_dcal_daily_amount_to_today
from from_mysql.mysql_table_df import select_share_by_date
from get_data.dailyMarkent import update_daily_market_to_today
from my_funcs.date_funcs import get_today_date
from qushi.gao_biao import newest_GB

update_daily_market_to_today()
update_dcal_daily_amount_to_today()

querydate = get_today_date()


# querydate = '2022-06-02'


def page_simple_layout():
    today_trade_df_origin = select_share_by_date(querydate)

    page = Page(layout=Page.SimplePageLayout)
    page.add(
        # 资金趋势
        draw_zhangdie_fenbu_bar(today_trade_df_origin),
        draw_lbtt(querydate),
        draw_pic_amounts(15),
        draw_zt_zb_dt_table(querydate, '涨停'),
        draw_zt_zb_dt_table(querydate, '炸板'),
        draw_zt_zb_dt_table(querydate, '跌停'),
        newest_GB(7),

    )
    page.render(querydate + "my_report.html")


if __name__ == "__main__":
    # update数据
    page_simple_layout()
