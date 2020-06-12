import os
import sys
import json
import pymysql
from prettytable import PrettyTable
from config import HostUtil, DatabaseUtil
from utils import gen_password

usage = """List HOSTS: python3 mysql-manage.py hosts
Add HOST: python3 mysql-manage.py add-host
List Databases for host: python3 mysql-manage.py {hostname} list
Create Database for host: python3 mysql-manage.py {hostname} create {database_name}
"""


def get_mysql_connection(config_data):
    connect = pymysql.Connect(
        host=config_data['host'],
        port=config_data['port'],
        user=config_data['user'],
        passwd=config_data['pass'],
        charset='utf8mb4'
    )
    return connect


def database_exists(__host_id__, __db_name__):
    if not HostUtil.host_exists(__host_id__):
        print('Host ID not exists. [%s]' % __host_id__)
        exit(-1)
    hosts = HostUtil.load_hosts()
    config_data = None
    for host in hosts:
        if host['host_id'] == __host_id__:
            config_data = host
    cursor = get_mysql_connection(config_data).cursor()
    sql = 'show databases'
    cursor.execute(sql)
    for row in cursor.fetchall():
        db_name = row[0].strip()
        if db_name == __db_name__:
            return True
    return False


def list_hosts():
    x = PrettyTable(field_names=["Host ID", "Host", "Port", "User", "Pass"])
    x.align["Host ID"] = "l"
    x.align["Host"] = "l"
    x.align["Port"] = "l"
    x.align["User"] = "l"
    x.align["Pass"] = "l"
    x.padding_width = 1  # 填充宽度
    hosts = HostUtil.load_hosts()
    for host in hosts:
        x.add_row([host['host_id'], host['host'], host['port'], host['user'], host['pass']])
    print(x)


def add_host():
    host_id = input('Host ID: ')
    host = input('Host: ')
    port = int(input('Port: '))
    username = input('Username: ')
    password = input('Password: ')
    hosts = HostUtil.load_hosts()
    for host in hosts:
        if host['host_id'] == host_id:
            print('Host ID already exists. [%s]' % host_id)
            exit(-1)
    HostUtil.add_host({
        'host_id': host_id,
        'host': host,
        'port': port,
        'user': username,
        'pass': password
    })


def list_databases(__host_id__):
    all_databases = DatabaseUtil.load_databases()
    databases = []
    if __host_id__ in all_databases:
        databases = all_databases[__host_id__]
    x = PrettyTable(field_names=["Name", "Username", "Password"])
    x.align["Name"] = "l"
    x.align["Username"] = "l"
    x.align["Password"] = "l"
    x.padding_width = 1  # 填充宽度
    for db in databases:
        x.add_row([db['name'], db['username'], db['password']])
    print(x)


# :param __db_name__:
# :return:
def database_create(__host_id__, __db_name__):
    if database_exists(__host_id__, __db_name__):
        print('Database already exists. [%s]' % __db_name__)
        exit(-1)
    db_pass = gen_password(8)
    hosts = HostUtil.load_hosts()
    config_data = None
    for host in hosts:
        if host['host_id'] == __host_id__:
            config_data = host
    if config_data is None:
        print('Can not load config data. [%s]' % __host_id__)
    conn = get_mysql_connection(config_data)
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
    DatabaseUtil.add_database(__host_id__, {
        'name': __db_name__,
        'username': __db_name__,
        'password': db_pass
    })


def main():
    if len(sys.argv) < 2:
        print(usage)
        exit(-1)

    # List HOSTS
    if sys.argv[1] == 'hosts':
        list_hosts()
        exit(0)

    # Add HOST
    if sys.argv[1] == 'add-host':
        add_host()
        exit(0)

    # Assert host_id is exists
    host_id = sys.argv[1]
    if not HostUtil.host_exists(host_id):
        print('Host ID not exists. [%s]' % host_id)
        exit(-1)

    # List Database for host
    if sys.argv[2] == 'list':
        list_databases(host_id)
        exit(0)

    # Create Database for host
    if sys.argv[2] == 'create':
        database_create(host_id, sys.argv[3])
        exit(0)


if __name__ == '__main__':
    main()
