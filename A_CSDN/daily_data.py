import requests
import pandas as pd

# 填入自己的token
mytoken = '5b98e*****************7hbjh'
# 设置数据的开始日期
startdate = '2023-06-12'
# 设置数据的结束日期
enddate = '2023-06-12'
# 设置数据的个股范围，默认获取全部A股
code = 'all'
# 设置数据中的字段，默认选择全部数据
filed = 'all'

response = requests.get(
    "http://api.waizaowang.com/doc/getStockHSADailyMarket?code=%s&startDate=%s&endDate=%s&export=5&token=%s&fields=%s" % (
        code, startdate, enddate, mytoken, filed))
# 将数据调整为dataframe格式
data = pd.DataFrame(response.json()['data'])

# 设置字段的中文名称
data.columns = ["股票代码", "交易时间", "股票名称", "最新价（元）", "涨跌幅度（%）", "涨跌额度（元）", "成交量（手）", "成交额（元）", "振幅（%）", "换手率（%）", "市净率（%）",
                "市盈率（动态）", "市盈率（静）", "市盈率（TTM）", "涨停价（元）", "跌停价（元）", "均价（元）", "量比", "最高价（元）", "最低价（元）", "今日开盘价（元）",
                "昨日收盘价（元）", "上市日期", "委比（%）", "外盘（手）", "内盘（手）", "ROE", "总股本（股）", "流通股本（股）", "流通市值（元）", "总市值（元）",
                "每股收益（元）", "5日涨幅（%）", "10日涨幅（%）", "20日涨幅（%）", "60日涨幅（%）", "今年以来涨幅（%）", "总营收（元）", "总营收同比（%）", "净资产",
                "净利润", "毛利率", "净利率", "负债率", "每股未分配利润", "每股净资产", "每股公积金（元）", "今日主力净流入（元）", "今日超大单流入（元）", "今日超大单流出（元）",
                "今日超大单净流入（元）", "今日大单流入（元）", "今日大单流出（元）", "今日大单净流入（元）", "今日中单流入（元）", "今日中单流出（元）", "今日中单净流入（元）",
                "今日小单流入（元）", "今日小单流出（元）", "今日小单净流入（元）"]
# 打印预览数据
print(data)

# 将数据保存到本地的excel中。
path = r'C:\Users\123\Desktop\\' + startdate + '日A股交易数据.xlsx'
data.round(2).to_excel(path, sheet_name='1', engine='openpyxl')
