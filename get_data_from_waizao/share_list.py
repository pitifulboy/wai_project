import requests
import pandas as pd
from sqlalchemy import create_engine
from mytoken.token_str import get_waizao_token


# 每周更新一次/手动更新。

def update_share_message():
    mytoken = get_waizao_token()
    # 按照网站模板，拼接。
    requests_str = "http://api.waizaowang.com/doc/getBaseInfo?type=1&code=all&export=5&token=" + mytoken + "&fields=all"
    response = requests.get(requests_str)
    data = pd.DataFrame(response.json()['data'])
    # ["股票代码","股票名称","股票类型，1：深证股票，2：上证股票，3：北证股票，4：港股","沪深港通，1：沪股通（港>沪）、
    # 2：深股通（港>深）、3：港股通（沪>港）、4：港股通（深>港）、5：港股通（深>港或沪>港）","所属板块，个股包括主板、创业板、科创板",
    # "ROE","总股本（股）","流通股本（股）","流通市值（元）","总市值（元）","上市日期","归属行业板块名称","归属地域板块名称","归属概念板块名称"]
    data.columns = ["code", "name", "stype", "hsgt", "bk", "roe", "zgb", "ltgb", "ltsz", "zsz", "ssdate", "z50", "z52",
                    "z53"]

    print(data)
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/waizao_data', encoding='utf8')
    data.to_sql('share_list', con=conn, if_exists='replace', index=False)

