import pandas as pd
from from_mysql.mysql_table_df import select_share_by_date
from sqlalchemy import create_engine

from my_funcs.get_share_markets import get_SH_SZ_BJ_sharedata
from my_settings import get_my_database_sql


# 交易额，涨幅
def cal_daily(querydate='2022-06-01'):
    # 判断是否已经计算，避免重复计算
    pass
    # 获取今日对交易数据.
    df_all = select_share_by_date(querydate)
    # 判断数据是否为空
    pass

    print(df_all.keys())

    market_type = ['ALL', 'SZ', 'SH', 'BJ', 'KC', 'CY']
    for i in range(0, len(market_type)):
        df_maket = get_SH_SZ_BJ_sharedata(df_all, column_name='股票代码', return_type=market_type[i])
        print(df_maket)

        # 获取交易额，平均涨幅，涨跌分布.涨停数量，涨停金额

å
cal_daily()
'''
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

        conn = create_engine(get_my_database_sql(), encoding='utf8')
        df_result.to_sql('result_daily_amount', con=conn, if_exists='append', index=False)
    else:
        print(querydate + '日，无数据')
        
        '''
