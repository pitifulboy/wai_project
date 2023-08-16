
def get_SH_SZ_BJ_sharedata(df_data='', column_name='股票代码', return_type='SH'):
    df_data['代码首位'] = df_data[column_name].str.slice(0, 1, 1)
    df_data['代码前2位'] = df_data[column_name].str.slice(0, 2, 1)

    if return_type == 'SH':
        result = df_data[df_data['代码首位'] == '6']
    elif return_type == 'SZ':
        result = df_data[df_data['代码首位'].isin(['0', '3'])]
    elif return_type == 'BJ':
        result = df_data[df_data['代码首位'].isin(['4', '8'])]
    elif return_type == 'CY':
        result = df_data[df_data['代码首位'] == '3']
    elif return_type == 'KC':
        result = df_data[df_data['代码前2位'] == '68']
    elif return_type=='ALL':
        result=df_data
    else:
        print('计算有误，请检查')
    return result

# querydate = '2023-08-14'
# data = select_share_by_date(querydate)
# print(get_SH_SZ_BJ_sharedata(data, return_type='CY'))
