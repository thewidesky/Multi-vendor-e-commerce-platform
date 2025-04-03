import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dao.manager_dao import ManagerDAO
from dao.Vendor_dao import VendorDAO
from dao.product_dao import ProductDAO

def get_data_by_user(username, password):
    """根据用户名和密码获取相应的数据
    Args:
        username (str): 用户名
        password (str): 密码
    Returns:
        list: 包含元组的列表，每个元组包含相应的数据字段
    """
    # 获取用户类型和ID
    user_type, user_id = check_user_type(username, password)
    
    if user_type == 'Password Error':
        return []
    
    # 根据用户类型返回不同的数据
    if user_type == 'Customer':
        # 获取所有产品信息
        product_dao = ProductDAO()
        products = product_dao.get_all_products()
        return [(p.p_id, p.v_id, p.category_id, p.p_name, float(p.price), p.stock) 
                for p in products]
    
    elif user_type == 'Manager':
        # 获取所有供应商信息
        vendor_dao = VendorDAO()
        vendors = vendor_dao.get_all_vendors()
        return [(v.v_id, v.business_name, v.geo_presence) 
                for v in vendors]
    
    elif user_type == 'Vendor':
        # 获取该供应商的所有产品
        product_dao = ProductDAO()
        products = product_dao.get_products_by_vendor(user_id)
        return [(p.p_id, p.p_name, float(p.price), p.stock, p.p_status) 
                for p in products]
    
    return []

# 测试代码
def test_get_data():
    # 测试管理员登录
    print("\n测试管理员登录:")
    data = get_data_by_user("Manger", "secret009")
    print("管理员数据: {0}".format(data))
    
    # 测试供应商登录
    print("\n测试供应商登录:")
    data = get_data_by_user("Alice Johnson", "secret001")
    print("供应商数据: {0}".format(data))
    
    # 测试用户登录
    print("\n测试用户登录:")
    data = get_data_by_user("Alice Johnson", "secret001")
    print("用户数据: {0}".format(data))
    
    # 测试错误登录
    print("\n测试错误登录:")
    data = get_data_by_user("wrong", "wrong")
    print("错误登录数据: {0}".format(data))


# 检查用户类型
def check_user_type(username, password):
    """根据用户名和密码判断用户类型
    Args:
        username (str): 用户名
        password (str): 密码
    Returns:
        tuple: (user_type, user_id) 其中user_type为'Manager', 'Customer', 'Vendor'或'Password Error'，
              user_id为对应的用户ID，当验证失败时为None
    """
    from dao.manager_dao import ManagerDAO
    from dao.Vendor_dao import VendorDAO

    # 创建DAO实例
    manager_dao = ManagerDAO()
    vendor_dao = VendorDAO()

    # 检查是否为管理员
    managers = manager_dao.get_all_managers()
    for manager in managers:
        if str(manager.m_name) == username:
            if str(manager.m_secret) == password:
                return ('Manager', manager.m_id)
            return ('Password Error', None)

    # 检查是否为普通用户
    customers = manager_dao.get_all_customer()
    for customer in customers:
        if customer.c_name == username:
            if str(customer.c_secret) == password:
                return ('Customer', customer.c_id)
            return ('Password Error', None)

    # 检查是否为供应商
    vendors = vendor_dao.get_all_vendors()
    for vendor in vendors:
        if vendor.business_name == username:
            if str(vendor.v_secret) == password:
                return ('Vendor', vendor.v_id)
            return ('Password Error', None)

    return ('Password Error', None)

if __name__ == "__main__":
    test_get_data()
