from from_mysql.mysql_table_column import get_columnlist_from_mysql
from from_mysql.mysql_table_df import select_share_by_startdate_type
from pyecharts.charts import Bar, Grid
from pyecharts import options as opts
from operator import itemgetter


def cal_lbtt(querydate):
    # 获取30天的交易数据
    # 暂时手动指定开始时间.2023-01-01后，涨停的交易数据
    df = select_share_by_startdate_type('2023-01-01', '涨停')
    # 有交易的日期list
    tradedate_list = get_columnlist_from_mysql('daily_market', '交易时间')
    # 已有交易数据中，最大的日期
    # max_date = tradedate_list[-1]
    # 获取待计算日的交易数据，并获取当日涨停的个股代码
    df_max_date_zt = df.loc[df['交易时间'] == querydate]
    max_date_zt_codelist = df_max_date_zt['股票代码'].tolist()

    lbtt_data_list = []

    # 连板数

    for i in range(0, len(max_date_zt_codelist)):
        df_code = df.loc[df['股票代码'] == max_date_zt_codelist[i]]

        n = 0
        for j in range(0, len(tradedate_list)):
            # 倒序时间，如果当天有涨停数据
            if len(df_code.loc[df_code['交易时间'] == tradedate_list[-j - 1]]) > 0:
                n = n + 1
            else:
                break

        if n > 1:
            lbtt_data_list.append([querydate, df_code.loc[:, '股票名称'].tolist()[-1], max_date_zt_codelist[i], n])

    lbtt_ordered = sorted(lbtt_data_list, key=itemgetter(3), reverse=False)
    print(querydate + '日，连板数据')
    print(lbtt_ordered)

    return lbtt_ordered


# 绘制连板天梯
def draw_lbtt(querydate):
    lbtt_ordered = cal_lbtt(querydate)
    # 隐藏 部分代码，名称信息
    # name = [x[0][3:11] for x in lbtt_ordered]
    # 完整显示 代码 和名称
    name = [x[1] for x in lbtt_ordered]
    num = [x[3] for x in lbtt_ordered]

    # 作图
    mybar = (
        Bar()
        .add_xaxis(name)
        .add_yaxis("连板数", num)
        .reversal_axis()
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True, font_size=18, color="#000000", position='right'),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=querydate + "连板天梯", pos_top='5%',
                                      pos_left='10%', title_textstyle_opts=opts.TextStyleOpts(font_size=36), ),
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=18)),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    mygrid = Grid(opts.InitOpts(bg_color='white', width="1600px", height="900px"))
    mygrid.add(mybar, grid_opts=opts.GridOpts(pos_left='30%', pos_top='10%'))
    # mygrid.render(querydate + "LBTT.html")

    return mygrid

# draw_lbtt('2023-03-24')
