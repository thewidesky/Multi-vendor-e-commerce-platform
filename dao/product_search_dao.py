import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG
import pymysql
from pymysql import cursors
from models.Product import Product
from models.Tag import Tag

class ProductSearchDAO:
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
        """获取数据库连接（Python 3.5兼容）"""
        return pymysql.connect(**self.db_config)

    # 功能1：根据标签ID获取产品列表
    def get_products_by_tag(self, tag_id):
        """
        参数: tag_id - 标签ID (int)
        返回: Product对象列表
        异常: 当数据库查询失败时抛出RuntimeError
        """
        sql = """SELECT 
                p.P_ID as p_id,
                p.V_ID as v_id,
                p.Category_ID as category_id,
                p.P_Name as p_name,
                p.Price as price,
                p.Stock as stock,
                p.P_Status as p_status,
                p.P_Picture as p_picture
                FROM Product p
                INNER JOIN Product_Tag pt ON p.P_ID = pt.P_ID
                WHERE pt.T_ID = %s"""
        
        products = []
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(sql, (tag_id,))
                results = cursor.fetchall()
                for row in results:
                    # 处理Python 3.5的float转换
                    converted = {
                        'p_id': row['p_id'],
                        'v_id': row['v_id'],
                        'category_id': row['category_id'],
                        'p_name': row['p_name'],
                        'price': float(row['price']),
                        'stock': row['stock'],
                        'p_status': row['p_status'],
                        'p_picture': row['p_picture']
                    }
                    products.append(Product.from_dict(converted))
            return products
        except Exception as e:
            raise RuntimeError("获取标签产品失败: {0}".format(str(e)))
        finally:
            if conn:
                conn.close()

    # 功能2：根据产品ID获取标签列表
    def get_tags_by_product(self, product_id):
        """
        参数: product_id - 产品ID (int)
        返回: Tag对象列表
        异常: 当数据库查询失败时抛出RuntimeError
        """
        sql = """SELECT 
                t.T_ID as t_id,
                t.Tag_Name as tag_name
                FROM Tag t
                INNER JOIN Product_Tag pt ON t.T_ID = pt.T_ID
                WHERE pt.P_ID = %s"""
        
        tags = []
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(sql, (product_id,))
                results = cursor.fetchall()
                for row in results:
                    converted = {
                        't_id': row['t_id'],
                        'tag_name': row['tag_name']
                    }
                    tags.append(Tag.from_dict(converted))
            return tags
        except Exception as e:
            raise RuntimeError("获取产品标签失败: {0}".format(str(e)))
        finally:
            if conn:
                conn.close()

# 测试代码
if __name__ == "__main__":
    def test_product_search():
        dao = ProductSearchDAO()
        
        # 测试数据准备（需要预先存在测试数据）
        test_tag_id = 1
        test_product_id = 1
        
        # 测试功能1
        try:
            products = dao.get_products_by_tag(test_tag_id)
            print("标签{0}关联的产品数量: {1}".format(test_tag_id, len(products)))
            if products:
                print("首个产品信息: {0}".format(products[0].to_dict()))
        except Exception as e:
            print("标签查询产品测试失败: {0}".format(str(e)))
        
        # 测试功能2
        try:
            tags = dao.get_tags_by_product(test_product_id)
            print("产品{0}关联的标签数量: {1}".format(test_product_id, len(tags)))
            if tags:
                print("首个标签信息: {0}".format(tags[0].to_dict()))
        except Exception as e:
            print("产品查询标签测试失败: {0}".format(str(e)))

    test_product_search()