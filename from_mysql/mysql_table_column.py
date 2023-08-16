# 选出日常交易中，最大日期，便于更新日常数据
import pandas as pd
from sqlalchemy import create_engine

from my_settings import get_my_database_sql


def get_max_from_mysql(table_name, column_name):
    conn = create_engine(get_my_database_sql(), encoding='utf8')
    mysql = "SELECT MAX(`" + column_name + "`) FROM " + table_name
    df = pd.read_sql(mysql, conn)
    return df.iloc[0, 0]


# 获取列的去重数据
def get_columnlist_from_mysql(table_name, column_name):
    conn = create_engine(get_my_database_sql(), encoding='utf8')
    mysql = "SELECT DISTINCT(`" + column_name + "`) FROM " + table_name

    df = pd.read_sql(mysql, conn)
    df_to_list = df[column_name].sort_values(ascending=True).tolist()
    return df_to_list

# print(get_columnlist_from_mysql('daily_market', 'tdate'))

# print(get_max_from_mysql(db_name='waizao_data', table_name='share_list', column_name='update_date'))
