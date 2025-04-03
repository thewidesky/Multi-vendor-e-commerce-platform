# manager_dao.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG
import pymysql
from pymysql import cursors
from models.Manager import Manager  # 假设存在Manager模型类
from models.customer import Customer  # 假设存在Manager模型类

class ManagerDAO:
    def __init__(self):
        self.db_config = {
            "host": DB_CONFIG["host"],
            "user": DB_CONFIG["user"],
            "password": DB_CONFIG["password"],
            "database": DB_CONFIG["database"],
            "charset": "utf8mb4",
            "cursorclass": cursors.DictCursor
        }

    def _get_connection(self):
        """获取数据库连接（Python 3.5兼容）"""
        return pymysql.connect(**self.db_config)

    # 功能1：获取所有管理员
    def get_all_managers(self):
        """返回Manager对象列表"""
        sql = "SELECT M_ID as m_id, M_Name as m_name, M_Secret as m_secret FROM Manager"
        managers = []
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    managers.append(Manager.from_dict({
                        "m_id": row["m_id"],
                        "m_name": row["m_name"],
                        "m_secret": row["m_secret"]
                    }))
            return managers
        except Exception as e:
            raise RuntimeError("获取管理员列表失败: {0}".format(str(e)))
        finally:
            if conn:
                conn.close()

    # 功能2：根据ID查询管理员
    def get_manager_by_id(self, m_id):
        """返回Manager对象或None"""
        sql = "SELECT M_ID as m_id, M_Name as m_name, M_Secret as m_secret FROM Manager WHERE M_ID = %s"
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(sql, (m_id,))
                result = cursor.fetchone()
                return Manager.from_dict(result) if result else None
        except Exception as e:
            raise RuntimeError("查询管理员失败: {0}".format(str(e)))
        finally:
            if conn:
                conn.close()

    # 功能3：更新管理员信息
    def update_manager(self, manager):
        """更新管理员密钥"""
        sql = "UPDATE Manager SET M_Secret = %s WHERE M_ID = %s"
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                affected = cursor.execute(sql, (
                    manager.m_secret,
                    manager.m_id
                ))
                conn.commit()
                if affected == 0:
                    raise ValueError("管理员ID {0} 不存在".format(manager.m_id))
                return manager
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError("更新失败: {0}".format(str(e)))
        finally:
            if conn:
                conn.close()

    # 功能4：删除管理员
    def delete_manager(self, m_id):
        """删除指定管理员"""
        sql = "DELETE FROM Manager WHERE M_ID = %s"
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                affected = cursor.execute(sql, (m_id,))
                conn.commit()
                if affected == 0:
                    raise ValueError("管理员ID {0} 不存在".format(m_id))
        except pymysql.err.IntegrityError as e:
            if conn:
                conn.rollback()
            raise RuntimeError("存在关联数据无法删除: {0}".format(e.args[1]))
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError("删除失败: {0}".format(str(e)))
        finally:
            if conn:
                conn.close()

    # 功能5：创建管理员
    def create_manager(self, manager):
        """创建新管理员，返回包含M_ID的对象"""
        sql = "INSERT INTO Manager (M_Name, M_Secret) VALUES (%s, %s)"
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(sql, (manager.m_name, manager.m_secret))
                conn.commit()
                manager.m_id = cursor.lastrowid
                return manager
        except pymysql.err.IntegrityError as e:
            if conn:
                conn.rollback()
            error_code = e.args[0]
            if error_code == 1062:
                raise ValueError("密钥已存在")
            raise RuntimeError("数据库错误: {0}".format(e.args[1]))
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError("创建失败: {0}".format(str(e)))
        finally:
            if conn:
                conn.close()
    
    # 功能6：获取所有使用者的信息
    def get_all_customer(self):
        """返回Customer对象列表"""
        sql = "SELECT C_ID as c_id, C_Name as c_name, Geo_Presence as geo_presence, C_Account as c_account, C_Secret as c_secret FROM Customer;"
        customer = []
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    customer.append(Customer.from_dict({
                        "c_id": row["c_id"],
                        "c_name": row["c_name"],
                        "geo_presence":row["geo_presence"],
                        "c_account":row["c_account"],
                        "c_secret":row["c_secret"]
                    }))
            return customer
        except Exception as e:
            raise RuntimeError("获取用户列表失败: {0}".format(str(e)))
        finally:
            if conn:
                conn.close()

# 测试代码
if __name__ == "__main__":
    def test_manager_dao():
        dao = ManagerDAO()
        test_manager = None
        
        try:
            # 测试创建
            new_manager = Manager(m_name="test_admin", m_secret="admin123")
            created = dao.create_manager(new_manager)
            print("[创建成功] ID: {0}".format(created.m_id))
            test_manager = created

            # 测试查询单个
            found = dao.get_manager_by_id(test_manager.m_id)
            if found:
                print("[查询成功] 找到管理员: {0}".format(found.to_dict()))
            else:
                print("[查询失败] 未找到管理员")

            # 测试查询所有管理者
            all_managers = dao.get_all_managers()
            print("All Managers:", [m.to_dict() for m in all_managers])
            print("[查询全部] 共{0}条记录".format(len(all_managers)))

            # 测试查询所有用户
            all_customer = dao.get_all_customer()
            print("All Customers:", [m.to_dict() for m in all_customer])
            print("[查询全部] 共{0}条记录".format(len(all_customer)))

            # 测试更新
            test_manager.m_secret = "newsecret456"
            updated = dao.update_manager(test_manager)
            print("[更新成功] 新密钥: {0}".format(updated.m_secret))

            # 验证更新
            check = dao.get_manager_by_id(test_manager.m_id)
            if check and check.m_secret == "newsecret456":
                print("[验证成功] 密钥已更新")
            else:
                print("[验证失败] 密钥未更新")

        except Exception as e:
            print("[测试失败] 发生错误: {0}".format(str(e)))
        finally:
            # 清理测试数据
            if test_manager and test_manager.m_id:
                try:
                    dao.delete_manager(test_manager.m_id)
                    print("[清理完成] 已删除测试数据")
                except Exception as e:
                    print("[清理失败] 无法删除数据: {0}".format(str(e)))

    test_manager_dao()