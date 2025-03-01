import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG
import pymysql
from pymysql import cursors
from models.Feedback import Feedback


class FeedbackDAO:
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
        """获取数据库连接"""
        return pymysql.connect(**self.db_config)

    # 功能1：根据顾客ID获取评论
    def get_feedback_by_customer(self, c_id):
        """
        参数: c_id - 顾客ID
        返回: Feedback对象列表
        """
        sql = """SELECT 
                C_ID as c_id,
                V_ID as v_id,
                Comment as comment,
                Rating as rating
                FROM Feedback
                WHERE C_ID = %s"""
        
        feedbacks = []
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(sql, (c_id,))
                results = cursor.fetchall()
                for row in results:
                    feedbacks.append(Feedback.from_dict(row))
            return feedbacks
        except Exception as e:
            raise RuntimeError("获取顾客评论失败: {0}".format(str(e)))
        finally:
            if conn:
                conn.close()

    # 功能2：根据商家ID获取评论
    def get_feedback_by_vendor(self, v_id):
        """
        参数: v_id - 商家ID
        返回: Feedback对象列表
        """
        sql = """SELECT 
                C_ID as c_id,
                V_ID as v_id,
                Comment as comment,
                Rating as rating
                FROM Feedback
                WHERE V_ID = %s"""
        
        feedbacks = []
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(sql, (v_id,))
                results = cursor.fetchall()
                for row in results:
                    feedbacks.append(Feedback.from_dict(row))
            return feedbacks
        except Exception as e:
            raise RuntimeError("获取商家评论失败: {0}".format(str(e)))
        finally:
            if conn:
                conn.close()

# 测试代码
if __name__ == "__main__":
    def test_feedback_dao():
        dao = FeedbackDAO()
        
        # 测试数据准备（需先存在顾客ID=1和商家ID=1）
        test_c_id = 1
        test_v_id = 20001
        
        try:
            # 测试顾客评论查询
            customer_feedbacks = dao.get_feedback_by_customer(test_c_id)
            print("顾客{0}的评论数: {1}".format(test_c_id, len(customer_feedbacks)))
            if customer_feedbacks:
                print("首条评论内容: {0}".format(customer_feedbacks[0].comment))

            # 测试商家评论查询
            vendor_feedbacks = dao.get_feedback_by_vendor(test_v_id)
            print("商家{0}的评论数: {1}".format(test_v_id, len(vendor_feedbacks)))
            if vendor_feedbacks:
                print("首条评分: {0}".format(vendor_feedbacks[0].rating))

        except Exception as e:
            print("测试失败: {0}".format(str(e)))

    test_feedback_dao()