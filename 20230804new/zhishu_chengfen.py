# 指数成分。获取指数成分，生成表格储存。

import requests
import pandas as pd

from mytoken_fun import get_my_waizao_token

if __name__ == '__main__':
    # 上证指数000001，深圳指数，创业399006，科创，北交所。上证50 000016，沪深300 000300，科创50 000688，中证500  000905，中证1000 000852
    index_type = '000001'
    mytoken = get_my_waizao_token()
    response = requests.get(
        "http://api.waizaowang.com/doc/getZhiShuChengFenGuZhongZhen?code=%s&export=5&token=%s&fields=all" % (
            index_type, mytoken))
    data = pd.DataFrame(response.json()['data'])
    data.columns = ["指数代码", "指数名称", "股票名称", "股票代码", "成分股权重"]
    print(data)
