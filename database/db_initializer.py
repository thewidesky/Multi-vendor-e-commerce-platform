import pymysql
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG

def initialize_database(file_path):
    sql_file = os.path.abspath(file_path)
    
    try:
        # 建立数据库连接
        connection = pymysql.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            db=DB_CONFIG["database"],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        sql_statements = []
        current_statement = []
        
        for line in sql_script.splitlines():
            line = line.split('--')[0].strip()
            if not line:
                continue
                
            current_statement.append(line)
            
            if ';' in line:
                full_statement = ' '.join(current_statement).replace(';', '')
                if full_statement:
                    sql_statements.append(full_statement)
                current_statement = []

        with connection.cursor() as cursor:
            for idx, statement in enumerate(sql_statements, 1):
                try:
                    cursor.execute(statement)
                    print("Executed statement #{}: {}...".format(
                        idx, statement[:50]))
                except pymysql.Error as e:
                    print("Error executing statement #{}:".format(idx))
                    print("SQL: {}".format(statement))
                    print("Error: {}".format(e.args[1] if e.args else e))
                    raise
                    
            connection.commit()
            print("Database initialized successfully!")

    except IOError as e:  # 统一处理文件错误
        print("File error: {}".format(str(e)))
    except pymysql.Error as e:
        print("Database error ({}): {}".format(e.args[0], e.args[1]))
    except Exception as e:
        print("Unexpected error: {}".format(str(e)))
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

if __name__ == "__main__":
    # file_path = 'CreateAllTable.sql'
    file_path = 'Init_Insert.sql'
    # file_path = 'DeleteAllTable.sql'
    initialize_database(file_path)