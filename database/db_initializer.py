import subprocess
import os
from config import DB_CONFIG

# 通过schema.sql来初始化MySQL数据库
def initialize_database():
    command = [
        DB_CONFIG["mysql_path"],
        "-h", DB_CONFIG["host"],
        "-u", DB_CONFIG["user"],
        "--password={}".format(DB_CONFIG['password']),
        DB_CONFIG["database"],
        "--execute=SOURCE {}".format(os.path.abspath('database/schema.sql'))
    ]
    
    # 打印命令用于调试
    # print("Executing command:", " ".join(command))
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error initializing database: {}".format(e))



if __name__ == "__main__":
    initialize_database()