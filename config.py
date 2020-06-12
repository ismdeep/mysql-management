import json
import os


def load_data_path():
    return os.path.expanduser('~') + '/.mysql-management'


class HostUtil:
    FILE_NAME = "hosts.json"

    @staticmethod
    def check_and_init():
        if not os.path.exists(load_data_path() + "/" + HostUtil.FILE_NAME):
            with open(load_data_path() + "/" + HostUtil.FILE_NAME, 'w') as hosts_file:
                json.dump([], hosts_file, indent=4, ensure_ascii=False)

    @staticmethod
    def load_hosts():
        HostUtil.check_and_init()
        try:
            with open(load_data_path() + "/" + HostUtil.FILE_NAME, "r") as hosts_file:
                hosts = json.load(hosts_file)
                return hosts
        except:
            return []

    @staticmethod
    def add_host(__host__):
        HostUtil.check_and_init()
        hosts = HostUtil.load_hosts()
        hosts.append(__host__)
        with open(load_data_path() + "/" + HostUtil.FILE_NAME, "w") as hosts_file:
            json.dump(hosts, hosts_file, indent=4, ensure_ascii=False)

    @staticmethod
    def host_exists(__host_id__):
        hosts = HostUtil.load_hosts()
        for host in hosts:
            if host['host_id'] == __host_id__:
                return True
        return False


class DatabaseUtil:
    FILE_NAME = "databases.json"

    @staticmethod
    def check_and_init():
        if not os.path.exists(load_data_path() + "/" + DatabaseUtil.FILE_NAME):
            with open(load_data_path() + "/" + DatabaseUtil.FILE_NAME, 'w') as hosts_file:
                json.dump({}, hosts_file, indent=4, ensure_ascii=False)

    @staticmethod
    def load_databases():
        DatabaseUtil.check_and_init()
        try:
            with open(load_data_path() + "/" + DatabaseUtil.FILE_NAME, 'r') as databases_file:
                databases = json.load(databases_file)
                return databases
        except:
            return {}

    @staticmethod
    def add_database(__host_id__, __database__):
        DatabaseUtil.check_and_init()
        all_databases = DatabaseUtil.load_databases()
        if __host_id__ not in all_databases:
            all_databases[__host_id__] = []
        all_databases[__host_id__].append(__database__)
        with open(load_data_path() + "/" + DatabaseUtil.FILE_NAME, "w") as databases_file:
            json.dump(all_databases, databases_file, indent=4, ensure_ascii=True)
