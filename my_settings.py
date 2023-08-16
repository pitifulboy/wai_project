def get_my_database_sql():
    mysql_admin_name = 'root'
    mysql_admin_psw = '12345678'
    mysql_address = 'localhost'
    mysql_port = '3306'
    mysql_db_name = 'waizao_data'

    # 'mysql+pymysql://root:123456@localhost:3306/waizao_data'
    sql_sentence = 'mysql+pymysql://%s:%s@%s:%s/%s' % (
        mysql_admin_name, mysql_admin_psw, mysql_address, mysql_port, mysql_db_name)
    # print(sql_sentence)
    return sql_sentence


