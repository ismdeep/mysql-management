import os
import json
from prettytable import PrettyTable

if __name__ == '__main__':
    database_json_path = "databases.json"
    data = json.load(open(database_json_path))
    x = PrettyTable(field_names=["Name", "Username", "Password"])
    x.align["Name"] = "l"
    x.align["Username"] = "l"
    x.align["Password"] = "l"
    x.padding_width = 1  # 填充宽度
    for db in data['databases']:
        x.add_row([db['name'], db['username'], db['password']])
    print(x)
