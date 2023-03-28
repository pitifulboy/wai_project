from from_mysql.mysql_table_df import select_amount
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line


# 绘制交易额组合图。大盘交易额+涨停交易额+炸板交易额
def draw_pic_amounts(ndays):
    df = select_amount()
    # 最近7日数据
    df_ndays = df[-ndays:]

    # 获取pyecharts所需数据
    date_list = df_ndays['交易时间'].tolist()
    zhangting_amount_list = df_ndays['涨停金额'].tolist()
    zhaban_amount_list = df_ndays['炸板金额'].tolist()
    # 大盘交易额
    dapan_amount_list = df_ndays['总成交额'].tolist()

    mybar = (
        Bar()
        .add_xaxis(date_list)
        .add_yaxis("涨停交易额", zhangting_amount_list, stack="stack1",
                   itemstyle_opts=opts.ItemStyleOpts(color="#ff0000"), z=0)
        .add_yaxis("炸板交易额", zhaban_amount_list, stack="stack1", itemstyle_opts=opts.ItemStyleOpts(color="#00ff00"), z=0)
        .extend_axis(yaxis=opts.AxisOpts(is_show=False))
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True, position='inside', font_size=16, font_weight='lighter',
                                      color='#000000'))
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90, font_size=16)),
            yaxis_opts=opts.AxisOpts(is_show=False),
            title_opts=opts.TitleOpts(
                title=date_list[-1] + "日资金趋势", pos_left='10%',
                title_textstyle_opts=opts.TextStyleOpts(font_size=36), pos_top='10%',
            ),
        )
    )

    myLine = (
        Line()
        .add_xaxis(date_list)
        .add_yaxis(
            "大盘交易额",
            dapan_amount_list,
            yaxis_index=1,
        )
        .set_series_opts(
            linestyle_opts=opts.LineStyleOpts(width=4),
            label_opts=opts.LabelOpts(position='top', font_size=24, font_weight='lighter', color='#000000'))
    )
    overlap_bar_line = mybar.overlap(myLine)

    mygrid = Grid(opts.InitOpts(bg_color='white', width="1600px", height="900px"))
    mygrid.add(overlap_bar_line, grid_opts=opts.GridOpts(pos_bottom='10%', pos_top='10%'), is_control_axis_index=True)
    #mygrid.render(date_list[-1] + "ZJQS.html")

    return mygrid
