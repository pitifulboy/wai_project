from dapan_analysis.zdfb import draw_zhangdie_fenbu_bar
from my_funcs.date_funcs import get_today_date


def analysis_dingpan():
    today_date = get_today_date()
    draw_zhangdie_fenbu_bar(today_date, '盯盘')
