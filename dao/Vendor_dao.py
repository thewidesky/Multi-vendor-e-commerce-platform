import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG
import pymysql
from models.Vendor import Vendor


class VendorDAO:
    def __init__(self):
        # 存储数据库连接配置（非连接对象）
        self.db_config = {
            "host": DB_CONFIG["host"],
            "user": DB_CONFIG["user"],
            "password": DB_CONFIG["password"],
            "db": DB_CONFIG["database"],
            "charset": 'utf8mb4',
            "cursorclass": pymysql.cursors.DictCursor
        }

    def _get_connection(self):
        """获取新的数据库连接"""
        return pymysql.connect(**self.db_config)

    def get_all_vendors(self):
        """获取所有供应商信息"""
        sql = "SELECT V_ID as v_id, Business_Name as business_name, " \
              "Geo_Presence as geo_presence, V_Account as v_account, " \
              "V_Secret as v_secret FROM Vendor"
        vendors = []
        
        try:
            conn = self._get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    for row in result:
                        # 显式转换字段名（解决大小写敏感问题）
                        converted = {
                            'v_id': row['v_id'],
                            'business_name': row['business_name'],
                            'geo_presence': row['geo_presence'],
                            'v_account': row['v_account'],
                            'v_secret': row['v_secret']
                        }
                        vendors.append(Vendor.from_dict(converted))
            finally:
                conn.close()
        except Exception as e:
            print("获取供应商列表出错: {0}".format(e))
            raise
        return vendors

    def create_vendor(self, vendor):
        """插入新供应商"""
        sql = """INSERT INTO Vendor 
                (Business_Name, Geo_Presence, V_Account, V_Secret)
                VALUES (%s, %s, %s, %s)"""
        
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                data = (
                    vendor.business_name,
                    vendor.geo_presence,
                    vendor.v_account,
                    vendor.v_secret
                )
                cursor.execute(sql, data)
                conn.commit()
                vendor.v_id = cursor.lastrowid
                return vendor
        except pymysql.err.IntegrityError as e:
            error_msg = "唯一性约束冲突: {0}".format(e.args[1])
            raise ValueError(error_msg)
        except Exception as e:
            if conn:
                conn.rollback()
            print("创建供应商失败: {0}".format(e))
            raise
        finally:
            if conn:
                conn.close()

    def delete_vendor(self, vendor_id):
        """根据ID删除供应商"""
        sql = "DELETE FROM Vendor WHERE V_ID = %s"
        
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                affected = cursor.execute(sql, (vendor_id,))
                conn.commit()
                if affected == 0:
                    raise ValueError("供应商ID {0} 不存在".format(vendor_id))
        except pymysql.err.IntegrityError as e:
            error_msg = "存在关联数据无法删除: {0}".format(e.args[1])
            raise RuntimeError(error_msg)
        except Exception as e:
            if conn:
                conn.rollback()
            print("删除失败: {0}".format(e))
            raise
        finally:
            if conn:
                conn.close()

    def update_vendor(self, vendor):
        """更新供应商信息"""
        sql = """UPDATE Vendor SET
                Business_Name = %s,
                Geo_Presence = %s,
                V_Account = %s,
                V_Secret = %s
                WHERE V_ID = %s"""
        
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                data = (
                    vendor.business_name,
                    vendor.geo_presence,
                    vendor.v_account,
                    vendor.v_secret,
                    vendor.v_id
                )
                affected = cursor.execute(sql, data)
                conn.commit()
                if affected == 0:
                    raise ValueError("供应商ID {0} 不存在".format(vendor.v_id))
                return vendor
        except pymysql.err.IntegrityError as e:
            error_msg = "账号冲突: {0}".format(e.args[1])
            raise ValueError(error_msg)
        except Exception as e:
            if conn:
                conn.rollback()
            print("更新失败: {0}".format(e))
            raise
        finally:
            if conn:
                conn.close()

# 测试代码调整
if __name__ == "__main__":
    def test_dao():
        """测试方法"""
        dao = VendorDAO()        
        all_v = []  # 初始化避免未绑定错误

        # 测试创建
        try:
            v = Vendor(
                business_name="测试供应商",
                geo_presence="北京",
                v_account="test@vendor.com",
                v_secret="123456"
            )
            created = dao.create_vendor(v)
            print("创建成功，ID:", created.v_id)
        except Exception as e:
            print("创建测试失败:", str(e))

        # 测试查询
        try:
            all_v = dao.get_all_vendors()
            print("查询到{0}条记录".format(len(all_v)))
            if all_v:
                print("第一条记录:", all_v[0].to_dict())
        except Exception as e:
            print("查询测试失败:", str(e))
            all_v = []  # 确保变量已赋值

        # 测试更新
        if all_v:
            try:
                target = all_v[-1]  # 使用最后一条记录测试
                target.business_name = "新名称"
                dao.update_vendor(target)
                print("更新成功")
            except Exception as e:
                print("更新测试失败:", str(e))
        else:
            print("无供应商记录，跳过更新测试")

        # 测试删除
        if all_v:
            try:
                dao.delete_vendor(all_v[-1].v_id)
                print("删除成功")
            except Exception as e:
                print("删除测试失败:", str(e))
        else:
            print("无供应商记录，跳过删除测试")

    test_dao()