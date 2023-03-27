import pandas as pd
import tushare as ts
from sqlalchemy import create_engine


def get_trade_df():
    pro = ts.pro_api()
    # tushare 交易日历数据接口
    df = pro.trade_cal(exchange='')
    # 转化列值格式
    df['cal_date'] = pd.to_datetime(df['cal_date'])
    df['pretrade_date'] = pd.to_datetime(df['pretrade_date'])
    # 指定目标时间格式
    df['cal_date'] = df['cal_date'].dt.strftime('%Y-%m-%d')
    df['pretrade_date'] = df['pretrade_date'].dt.strftime('%Y-%m-%d')

    # 升序排列
    df.sort_values(by="cal_date", inplace=True, ascending=True)

    # 去掉最开始的一天
    df_new = df[1:]

    return df_new


def update_tradedate_from_tushare():
    df = get_trade_df()
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/waizao_data', encoding='utf8')
    df.to_sql('trade_date', con=conn, if_exists='replace', index=False)


# 手动更新即可
update_tradedate_from_tushare()
