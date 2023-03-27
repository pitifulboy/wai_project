from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts


# 通过df 生成pyecharts表格
def draw_table_by_df(df, tablename):
    headers = df.columns.values.tolist()
    rows = df.values.tolist()

    table = Table()

    table.add(headers, rows)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(title=tablename)
    )
    table.render(tablename + ".html")
    return table
