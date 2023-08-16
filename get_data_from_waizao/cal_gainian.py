import pandas as pd


def get_gainian_df(df):
    # 代码
    df_code = df["股票代码"]
    # 概念
    df_gn = df["归属概念板块名称"].str.split(",", expand=True).fillna("")
    # 生成  代码，概念  的df

    result = pd.concat([df_code, df_gn], axis=1)
    mylist = result.values

    new_list = []
    for i in range(0, len(mylist)):
        code = mylist[i][0]
        for j in range(1, len(mylist[i])):
            if mylist[i][j] != "":
                new_list.append([code, mylist[i][j]])

    df_code_gn = pd.DataFrame(new_list, columns=["股票代码", "概念名称"])

    # path = r'D:\00 量化交易\\概念分析.xlsx'
    # df_code_gn.to_excel(path, sheet_name='1', engine='openpyxl')

    return df_code_gn
