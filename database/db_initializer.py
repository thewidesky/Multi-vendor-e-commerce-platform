import subprocess
import os
from config import DB_CONFIG

def initialize_database():
    # 通过mysql命令行执行schema.sql
    command = [
        "mysql",
        "-h", DB_CONFIG["host"],
        "-u", DB_CONFIG["user"],
        "-p" + DB_CONFIG["password"],
        "-e",
        "source {};".format(os.path.abspath('database/schema.sql'))
        
    ]
    print("command命令是:",command)
    subprocess.run(command, check=True)