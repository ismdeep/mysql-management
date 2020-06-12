import pymysql
import sys
from utils import gen_password
from config import load_config, load_data_path
import json


def show_help_msg():
    print("""Usage: python3 mysql-create.py {db_name}""")


def get_mysql_connection():
    config_data = load_config()
    connect = pymysql.Connect(
        host=config_data['host'],
        port=config_data['port'],
        user=config_data['user'],
        passwd=config_data['pass'],
        charset='utf8mb4'
    )
    return connect


def database_exists(__db_name__):
    cursor = get_mysql_connection().cursor()
    sql = 'show databases'
    cursor.execute(sql)
    for row in cursor.fetchall():
        db_name = row[0].strip()
        if db_name == __db_name__:
            return True
    return False


# :param __db_name__:
# :return:
def database_create(__db_name__):
    db_pass = gen_password(8)
    conn = get_mysql_connection()
    cursor = conn.cursor()
    sql_create_db = "CREATE DATABASE `%s` default character set utf8mb4 collate utf8mb4_unicode_ci" % __db_name__
    sql_create_user = "CREATE USER '%s'@'%%' IDENTIFIED BY '%s'" % (__db_name__, db_pass)
    sql_grant_privileges = "grant all privileges on %s.* to '%s'@'%%'" % (__db_name__, __db_name__)
    sql_flush_privileges = "flush privileges"
    sql_set_native_password = "ALTER USER '%s'@'%%' IDENTIFIED WITH mysql_native_password BY '%s'" % (
        __db_name__, db_pass)
    cursor.execute(sql_create_db)
    cursor.execute(sql_create_user)
    cursor.execute(sql_grant_privileges)
    cursor.execute(sql_flush_privileges)
    cursor.execute(sql_set_native_password)
    cursor.execute(sql_flush_privileges)
    print("Database Create Successfully.\n"
          "DB_DATABASE=%s\n"
          "DB_USERNAME=%s\n"
          "DB_PASSWORD=%s\n"
          % (__db_name__, __db_name__, db_pass)
          )
    # 写入 databases.json 配置文件
    databases_json = json.load(open(load_data_path() + '/databases.json'))
    databases_json['databases'].append({
        'name': __db_name__,
        'username': __db_name__,
        'password': db_pass
    })
    json_file = open(load_data_path() + "/databases.json", "w")
    json.dump(databases_json, json_file, indent=4, ensure_ascii=False)
    json_file.close()


def main():
    if len(sys.argv) < 2:
        show_help_msg()
        exit(-1)
    db_name = sys.argv[1]
    if database_exists(db_name):
        print('''Database exists. [%s]''' % db_name)
        exit(-1)
    print("Start to creating database. [%s]" % db_name)
    database_create(db_name)


if __name__ == '__main__':
    main()
