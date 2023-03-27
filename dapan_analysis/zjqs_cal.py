# 每日计划，并写入mysql
import pandas as pd
from sqlalchemy import create_engine

from from_mysql.mysql_table_column import get_columnlist_from_mysql
from from_mysql.mysql_table_df import select_share_by_date

# 判断是否已经计算，如果未计算，则计算到最新日期。
from get_data.dailyMarkent import update_daily_market_to_today
from my_funcs.date_funcs import generate_datelist_by_start_end, get_today_date


def judge_cal_amount_or_not(update_date):
    # 判断查询日期的数据是否存在
    # 获取存在的交易日
    tdate_list = get_columnlist_from_mysql('result_daily_amount', '交易时间')
    if update_date in tdate_list:
        print(update_date + "日，交易额数据已经计算")
    else:
        print(update_date + "日，交易额数据计算中")
        cal_daily_amount(update_date)


def cal_daily_amount(querydate):
    # 今日总交易额
    df_all = select_share_by_date(querydate)

    if len(df_all) > 0:
        # 触板（含涨停和炸板）
        df_cb = df_all.loc[df_all['最高价（元）'] == df_all['涨停价（元）']]
        df_zt = df_cb.loc[df_cb['最新价（元）'] == df_cb['涨停价（元）']]
        df_zb = df_cb.loc[df_cb['最新价（元）'] != df_cb['涨停价（元）']]

        amount_all = df_all['成交额（元）'].sum() / 100000000
        amount_zt = df_zt['成交额（元）'].sum() / 100000000
        amount_zb = df_zb['成交额（元）'].sum() / 100000000

        df = pd.DataFrame(data=[[querydate, amount_all, amount_zt, amount_zb]],
                          columns=['交易时间', '总成交额', '涨停金额', '炸板金额'])
        df_result = df.round(0)
        print(df_result)

        conn = create_engine('mysql+pymysql://root:123456@localhost:3306/waizao_data', encoding='utf8')
        df_result.to_sql('result_daily_amount', con=conn, if_exists='append', index=False)
    else:
        print(querydate + '日，无数据')


# 按日调用。
def update_cal_daily_amount_by_datelist(startdate, enddate):
    datelist = generate_datelist_by_start_end(startdate, enddate)
    for i in datelist:
        judge_cal_amount_or_not(i)


def update_dcal_daily_amount_to_today():

    tdate_list = get_columnlist_from_mysql('result_daily_amount', '交易时间')
    max_date = tdate_list[-1]
    today = get_today_date()
    update_cal_daily_amount_by_datelist(max_date, today)


# cal_daily_amount('2022-06-01')
# update_daily_market_to_today()

'''# 日期，大盘交易额，涨停交易额，涨停数，炸板交易额，炸板数,跌停交易额，跌停数
datalist = [querday, total_df_amount, zhangtingban_df_amount, n_zhangtingban_df, zhaban_df_amount,
            n_zha_df, dieting_df_amount, n_dieting_df]'''
