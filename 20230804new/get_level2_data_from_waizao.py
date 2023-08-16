import requests
import pandas as pd

if __name__ == '__main__':
    response = requests.get(
        "http://api.waizaowang.com/doc/getLevel2TimeDeal?type=1&code=000002&startDate=2023-08-08&endDate=2023-08-08"
        "&export=5&token=5b98e82a71a2afd3b84c5d14ad192c57&fields=code,tdate,price,cjl")
    data = pd.DataFrame(response.json()['data'])
    # 相对于上个价位走势，1表示下跌或持平，2表示上涨或持平
    data.columns = ["股票代码", "分时时间", "成交价", "成交量（手）"]
    print(data)
