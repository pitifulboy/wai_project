# 将多个图表在同一个网页展示

from pyecharts.charts import Page
from chaoduan_analysis.lian_ban import draw_lbtt
from chaoduan_analysis.zt_dt_zb import draw_zt_zb_dt_table
from dapan_analysis.gainian_analysis import draw_bk_table
from dapan_analysis.zdfb import draw_zhangdie_fenbu_bar
from dapan_analysis.zjqs import draw_pic_amounts
from dapan_analysis.zjqs_cal import update_dcal_daily_amount_to_today
from from_mysql.mysql_table_df import select_share_by_date
from get_data_from_waizao.dailyMarkent import update_daily_market_to_today
from my_funcs.date_funcs import get_today_date
from qushi.gao_biao import newest_GB

# 获取交易数据
update_daily_market_to_today()
update_dcal_daily_amount_to_today()

querydate = get_today_date()


# querydate = '2023-06-13'


def page_simple_layout():
    data = select_share_by_date(querydate)

    # 保存数据
    # path = r'D:\00 量化交易\\' + str(querydate) + '日交易数据.xlsx'
    # 取2位小数，并导出数据
    # data.round(2).to_excel(path, sheet_name='1', engine='openpyxl')

    page = Page(layout=Page.SimplePageLayout)
    page.add(
        # 资金趋势
        draw_zhangdie_fenbu_bar(data),
        draw_lbtt(querydate, "no_st_share"),
        draw_pic_amounts(15),
        draw_zt_zb_dt_table(data, '涨停'),
        draw_zt_zb_dt_table(data, '炸板'),
        draw_zt_zb_dt_table(data, '跌停'),
        # 查询3日高标，top100复盘
        newest_GB(3),
        newest_GB(5),
        newest_GB(7),
        draw_bk_table(data, '概念名称'),
        draw_bk_table(data, '归属行业板块名称'),
        draw_bk_table(data, '归属地域板块名称'),

    )
    page.render(querydate + "my_report.html")


if __name__ == "__main__":
    # update数据
    page_simple_layout()
