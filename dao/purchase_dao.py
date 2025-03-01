import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG
import pymysql
from pymysql import cursors
from models.Records import Records
from models.RecordsDetail import RecordsDetail

class PurchaseDAO:
    def __init__(self):
        self.db_config = {
            "host": DB_CONFIG["host"],
            "user": DB_CONFIG["user"],
            "password": DB_CONFIG["password"],
            "database": DB_CONFIG["database"],
            "charset": 'utf8mb4',
            "cursorclass": cursors.DictCursor
        }

    def _get_connection(self):
        """获取数据库连接"""
        return pymysql.connect(**self.db_config)

    # 功能1：创建购买记录（事务操作）
    def create_purchase(self, record, details):
        """
        参数: 
            record - Record对象
            details - RecordDetail对象列表
        返回: 包含R_ID的Record对象
        异常: 事务失败时回滚
        """
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                # 插入主记录
                record_sql = """INSERT INTO Records 
                            (R_ID, S_ID, C_ID, Toal, R_Status, R_Date)
                            VALUES (%s, %s, %s, %s, %s, %s)"""
                record_data = (
                    record.r_id,
                    record.s_id,
                    record.c_id,
                    float(record.toal),
                    record.r_status,
                    record.r_date
                )
                cursor.execute(record_sql, record_data)

                # 插入明细记录
                detail_sql = """INSERT INTO `Records Detail`
                            (R_ID, P_ID, Price, Quantity, Subtotal)
                            VALUES (%s, %s, %s, %s, %s)"""
                detail_data = [
                    (
                        record.r_id,
                        detail.p_id,
                        float(detail.price),
                        detail.quantity,
                        float(detail.subtotal)
                    ) for detail in details
                ]
                cursor.executemany(detail_sql, detail_data)

                conn.commit()
                return record
        except pymysql.err.IntegrityError as e:
            if conn:
                conn.rollback()
            error_code = e.args[0]
            if error_code == 1452:
                raise ValueError("外键约束失败: {}".format(e.args[1]))
            raise RuntimeError("数据库约束错误: {}".format(str(e)))
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError("创建购买记录失败: {}".format(str(e)))
        finally:
            if conn:
                conn.close()

    # 功能2：查询购买记录
    def get_purchases_by_customer(self, c_id):
        """
        参数: c_id - 客户ID
        返回: 包含明细的Record对象列表
        """
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                # 查询主记录
                record_sql = """SELECT 
                            R_ID as r_id,
                            S_ID as s_id,
                            C_ID as c_id,
                            Toal as toal,
                            R_Status as r_status,
                            R_Date as r_date
                            FROM Records
                            WHERE C_ID = %s"""
                cursor.execute(record_sql, (c_id,))
                records = []
                for row in cursor.fetchall():
                    # 转换主记录
                    record = Records.from_dict({
                        'r_id': row['r_id'],
                        's_id': row['s_id'],
                        'c_id': row['c_id'],
                        'toal': float(row['toal']),
                        'r_status': row['r_status'],
                        'r_date': row['r_date'].strftime('%Y-%m-%d')  # 日期格式转换
                    })

                    # 查询明细
                    detail_sql = """SELECT 
                                RD_ID as rd_id,
                                R_ID as r_id,
                                P_ID as p_id,
                                Price as price,
                                Quantity as quantity,
                                Subtotal as subtotal
                                FROM `Records Detail`
                                WHERE R_ID = %s"""
                    cursor.execute(detail_sql, (record.r_id,))
                    details = []
                    for detail_row in cursor.fetchall():
                        details.append(RecordsDetail.from_dict({
                            'rd_id': detail_row['rd_id'],
                            'r_id': detail_row['r_id'],
                            'p_id': detail_row['p_id'],
                            'price': float(detail_row['price']),
                            'quantity': detail_row['quantity'],
                            'subtotal': float(detail_row['subtotal'])
                        }))
                    record.details = details
                    records.append(record)
                return records
        except Exception as e:
            raise RuntimeError("查询购买记录失败: {}".format(str(e)))
        finally:
            if conn:
                conn.close()

    # 功能3：修改购买记录以及购买记录细节
    def update_purchase(self, record, details):
        """
        参数: 
            record - 更新后的Record对象
            details - 更新后的RecordDetail对象列表（必须与现有记录完全匹配）
        """
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                # 第一部分：更新主记录
                main_update_sql = """UPDATE Records SET
                                S_ID = %s,
                                Toal = %s,
                                R_Status = %s,
                                R_Date = %s
                                WHERE R_ID = %s"""
                cursor.execute(main_update_sql, (
                    record.s_id,
                    float(record.toal),
                    record.r_status,
                    record.r_date,
                    record.r_id
                ))

                # 第二部分：验证并更新明细记录
                # Step 1. 获取当前所有明细记录
                cursor.execute(
                    "SELECT RD_ID, P_ID FROM `Records Detail` WHERE R_ID = %s",
                    (record.r_id,)
                )
                existing_details = {row['P_ID']: row['RD_ID'] for row in cursor.fetchall()}
                
                # Step 2. 校验明细记录数量一致性
                if len(existing_details) != len(details):
                    raise ValueError("明细记录数量不匹配，预期{}条，实际{}条".format(
                        len(existing_details), len(details)
                    ))

                # Step 3. 批量更新明细记录
                update_params = []
                for detail in details:
                    if detail.p_id not in existing_details:
                        raise ValueError("发现未知商品ID: {}".format(detail.p_id))
                    
                    update_params.append((
                        float(detail.price),
                        detail.quantity,
                        float(detail.subtotal),
                        existing_details[detail.p_id]
                    ))

                # Step 4. 执行批量更新
                update_detail_sql = """UPDATE `Records Detail` SET
                                    Price = %s,
                                    Quantity = %s,
                                    Subtotal = %s
                                    WHERE RD_ID = %s"""
                cursor.executemany(update_detail_sql, update_params)

                conn.commit()
        except ValueError as ve:
            if conn:
                conn.rollback()
            raise RuntimeError("数据校验失败: {}".format(str(ve)))
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError("更新操作失败: {}".format(str(e)))
        finally:
            if conn:
                conn.close()


    # 功能4：删除购买记录
    def delete_purchase(self, r_id):
        """
        参数: r_id - 记录ID
        说明: 由于外键约束设置为ON DELETE CASCADE，明细会自动删除
        """
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                sql = "DELETE FROM Records WHERE R_ID = %s"
                affected = cursor.execute(sql, (r_id,))
                conn.commit()
                if affected == 0:
                    raise ValueError("记录ID {} 不存在".format(r_id))
        except pymysql.err.IntegrityError as e:
            if conn:
                conn.rollback()
            raise RuntimeError("存在关联数据无法删除: {}".format(e.args[1]))
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError("删除失败: {}".format(str(e)))
        finally:
            if conn:
                conn.close()


# 测试代码
if __name__ == "__main__":
    def test_purchase_dao():
        dao = PurchaseDAO()
        
        # 测试数据准备
        test_record = Records(
            r_id=1001,  # 需要确保不冲突
            s_id=1,
            c_id=1,
            toal=199.99,
            r_status=True,
            r_date="2023-01-01"
        )
        
        test_details = [
            RecordsDetail(
                r_id=test_record.r_id,
                p_id=1,
                price=99.99,
                quantity=2,
                subtotal=199.98
            ),
            RecordsDetail(
                r_id=test_record.r_id,
                p_id=2,
                price=50.00,
                quantity=1,
                subtotal=50.00
            )
        ]

        # 测试创建
        try:
            created = dao.create_purchase(test_record, test_details)
            print("创建记录成功，R_ID: {}".format(created.r_id))
        except Exception as e:
            print("创建测试失败: {}".format(str(e)))
            return

        # 测试查询
        try:
            records = dao.get_purchases_by_customer(1)
            print("客户1共有{}笔订单".format(len(records)))
            if records:
                first = records[0]
                print("查询后的记录为：",first.details)
                print("首笔订单总金额: {}".format(first.toal))
                print("包含{}个商品".format(len(first.details)))
        except Exception as e:
            print("查询测试失败: {}".format(str(e)))

        # 测试更新
        if records:
            try:
                record = test_record
                record.toal = 250.00
                new_details = [RecordsDetail(r_id=test_record.r_id,p_id=1, price=100, quantity=2, subtotal=200),
                                RecordsDetail(r_id=test_record.r_id,p_id=2, price=100, quantity=2, subtotal=200)
                                ]
                dao.update_purchase(record, new_details)
                print("更新测试成功")
            except Exception as e:
                print("更新测试失败: {}".format(str(e)))

        # 测试删除
        if records:
            try:
                # dao.delete_purchase(records[0].r_id)
                dao.delete_purchase(test_record.r_id)
                print("删除测试成功")
            except Exception as e:
                print("删除测试失败: {}".format(str(e)))

    test_purchase_dao()