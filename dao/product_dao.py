import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG
import pymysql
from pymysql import cursors
from models.Product import Product  # 确保模型类存在

class ProductDAO:
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
        """获取数据库连接(兼容Python 3.5)"""
        return pymysql.connect(**self.db_config)

    # 功能1：根据供应商ID获取所有产品
    def get_products_by_vendor(self, vendor_id):
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
                WHERE p.V_ID = %s"""
        
        products = []
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(sql, (vendor_id,))
                results = cursor.fetchall()
                for row in results:
                    converted = {
                        'p_id': row['p_id'],
                        'v_id': row['v_id'],
                        'category_id': row['category_id'],
                        'p_name': row['p_name'],
                        'price': float(row['price']) if row['price'] else 0.0,
                        'stock': row['stock'],
                        'p_status': row['p_status'],
                        'p_picture': row['p_picture']
                    }
                    products.append(Product.from_dict(converted))
            return products
        except Exception as e:
            raise RuntimeError("获取供应商产品失败: {0}".format(str(e)))
        finally:
            if conn:
                conn.close()

    # 功能2：创建新产品
    def create_product(self, product):
        sql = """INSERT INTO Product 
                (V_ID, Category_ID, P_Name, Price, Stock, P_Status, P_Picture)
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                # Python 3.5兼容的元组参数
                data = (
                    product.v_id,
                    product.category_id,
                    product.p_name,
                    float(product.price),
                    product.stock,
                    product.p_status,
                    product.p_picture
                )
                cursor.execute(sql, data)
                conn.commit()
                product.p_id = cursor.lastrowid
                return product
        except pymysql.err.IntegrityError as e:
            error_code = e.args[0]
            if error_code == 1452:
                msg = "供应商或分类不存在"
            else:
                msg = "数据库约束冲突: {0}".format(e.args[1])
            raise ValueError(msg)
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError("创建产品失败: {0}".format(str(e)))
        finally:
            if conn:
                conn.close()

    # 功能3：根据产品ID获取详细信息
    def get_product_by_id(self, product_id):
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
                WHERE p.P_ID = %s"""
        
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(sql, (product_id,))
                result = cursor.fetchone()
                if result:
                    # 显式类型转换处理
                    converted = {
                        'p_id': result['p_id'],
                        'v_id': result['v_id'],
                        'category_id': result['category_id'],
                        'p_name': result['p_name'],
                        'price': float(result['price']),
                        'stock': result['stock'],
                        'p_status': result['p_status'],
                        'p_picture': result['p_picture']
                    }
                    return Product.from_dict(converted)
                return None
        except Exception as e:
            raise RuntimeError("获取产品详情失败: {0}".format(str(e)))
        finally:
            if conn:
                conn.close()

    # 功能4：根据产品ID删除产品
    def delete_product(self, product_id):
        sql = "DELETE FROM Product WHERE P_ID = %s"
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                affected = cursor.execute(sql, (product_id,))
                conn.commit()
                if affected == 0:
                    raise ValueError("产品ID {} 不存在".format(product_id))
        except pymysql.err.IntegrityError as e:
            error_code = e.args[0]
            if error_code == 1451:  # 外键约束错误
                msg = "存在关联订单无法删除"
            else:
                msg = "数据库约束冲突: {}".format(e.args[1])
            raise RuntimeError(msg)
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError("删除产品失败: {}".format(str(e)))
        finally:
            if conn:
                conn.close()

    
    # 功能5：更新产品信息
    def update_product(self, product):
        sql = """UPDATE Product SET
                V_ID = %s,
                Category_ID = %s,
                P_Name = %s,
                Price = %s,
                Stock = %s,
                P_Status = %s,
                P_Picture = %s
                WHERE P_ID = %s"""
        
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                data = (
                    product.v_id,
                    product.category_id,
                    product.p_name,
                    float(product.price),
                    product.stock,
                    product.p_status,
                    product.p_picture,
                    product.p_id  # WHERE条件放在最后
                )
                affected = cursor.execute(sql, data)
                conn.commit()
                if affected == 0:
                    raise ValueError("产品ID {} 不存在".format(product.p_id))
                return product
        except pymysql.err.IntegrityError as e:
            error_code = e.args[0]
            if error_code == 1452:  # 外键约束
                msg = "供应商或分类不存在"
            else:
                msg = "数据库约束冲突: {}".format(e.args[1])
            raise ValueError(msg)
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError("更新产品失败: {}".format(str(e)))
        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    def test_product_dao():
        dao = ProductDAO()
        test_product = None
        
        # 测试创建
        try:
            test_product = Product(
                v_id=20001,
                category_id=10001,
                p_name="测试商品",
                price=99.99,
                stock=100,
                p_status=1,
                p_picture="test.jpg"
            )
            created = dao.create_product(test_product)
            print("创建成功，产品ID: {0}".format(created.p_id))
            test_product = created  # 保存用于后续测试
        except Exception as e:
            print("创建测试失败: {0}".format(str(e)))
            return

        # 测试查询供应商产品
        try:
            products = dao.get_products_by_vendor(20001)
            print("供应商20001共有{0}个产品".format(len(products)))
            if products:
                print("首个产品: {0}".format(products[0].to_dict()))
        except Exception as e:
            print("查询供应商产品失败: {0}".format(str(e)))

        # 测试查询单个产品
        if test_product and hasattr(test_product, 'p_id'):
            try:
                found = dao.get_product_by_id(test_product.p_id)
                if found:
                    print("查询到产品: {0}".format(found.to_dict()))
                else:
                    print("未找到测试产品")
            except Exception as e:
                print("查询单个产品失败: {0}".format(str(e)))

        
        # 测试更新功能
        if test_product and test_product.p_id:
            try:
                # 修改产品属性
                test_product.p_name = "更新后的名称"
                test_product.price = 199.99
                updated = dao.update_product(test_product)
                
                # 验证更新结果
                check_product = dao.get_product_by_id(test_product.p_id)
                if check_product and check_product.p_name == "更新后的名称":
                    print("更新测试成功")
                else:
                    print("更新测试失败")
            except Exception as e:
                print("更新测试失败: {0}".format(str(e)))
        
        
        # 测试删除功能
        if test_product and test_product.p_id:
            try:
                dao.delete_product(test_product.p_id)
                # 验证删除结果
                deleted_product = dao.get_product_by_id(test_product.p_id)
                if deleted_product is None:
                    print("删除测试成功")
                else:
                    print("删除测试失败")
            except Exception as e:
                print("删除测试失败: {0}".format(str(e)))

    test_product_dao()