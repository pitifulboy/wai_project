# 指数成分

import requests
import pandas as pd

# 获取指数成分股，并存入mysql。
from sqlalchemy import create_engine

from mytoken.token_str import get_waizao_token


def get_zscfg_df(zscf_type):
    # zscf_type=1，获取【沪深300】
    # zscf_type=2，获取【上证50】
    # zscf_type=3，获取【中证500】
    # zscf_type=4，获取【科创50】
    token = get_waizao_token()
    url_str = "http://api.waizaowang.com/doc/getZhiShuChengFenGu?mtype=%s&export=5&token=%s&fields=mtype,code," \
              "indexname,name,secucode" % (zscf_type, token)
    # 获取数据
    response = requests.get(url_str)
    # 整理数据
    data = pd.DataFrame(response.json()['data'])
    data.columns = ["指数类别", "股票代码", "指数名称", "股票名称", "股票安全代码"]
    # 预览数据
    print(data)
    # 返回数据
    return data


def get_all_zscfg_df():
    data1 = get_zscfg_df(1)
    data2 = get_zscfg_df(2)
    data3 = get_zscfg_df(3)
    data4 = get_zscfg_df(4)
    data_all = pd.concat([data1, data2, data3, data4], axis=0)
    print(data_all)
    return data_all


def write_all_zscfg_to_mysql(df):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/waizao_data', encoding='utf8')
    df.to_sql('zscfg', con=conn, if_exists='replace', index=False)

# 更新主要指数成分
# write_all_zscfg_to_mysql(get_all_zscfg_df())
