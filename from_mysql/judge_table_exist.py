# 选出日常交易中，最大日期，便于更新日常数据
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine


def check_table_exist(table_name):
    # 配置引擎，创建sqlalchemy和数据库的链接
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/waizao_data', encoding='utf8')
    # 判断数据库是否存在，不存在则创建
    rusult = sa.inspect(conn).has_table(table_name)
    return rusult
