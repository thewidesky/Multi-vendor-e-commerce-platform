import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dao.manager_dao import ManagerDAO
from dao.Vendor_dao import VendorDAO
from dao.product_dao import ProductDAO
from dao.product_search_dao import ProductSearchDAO
from dao.purchase_dao import PurchaseDAO


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



def get_products_by_tag_id(tag_id):
    """根据标签ID获取产品信息
    Args:
        tag_id (int): 标签ID
    Returns:
        list: 包含产品信息元组的列表，每个元组包含(ProductID、VendorID、CategoryID、ProductName、Price、Stock)
    """
    product_search_dao = ProductSearchDAO()
    products = product_search_dao.get_products_by_tag(tag_id)
    return [(p.p_id, p.v_id, p.category_id, p.p_name, float(p.price), p.stock)
            for p in products]



def get_product_by_id(product_id):
    """根据产品ID获取产品信息
    Args:
        product_id (int): 产品ID
    Returns:
        list: 包含产品信息元组的列表，每个元组包含(ProductID、VendorID、CategoryID、ProductName、Price、Stock)
    """
    product_dao = ProductDAO()
    product = product_dao.get_product_by_id(product_id)
    if product:
        return [(product.p_id, product.v_id, product.category_id, product.p_name, float(product.price), product.stock)]
    return []



def get_vendor_data_by_id(vendor_id):
    """根据供应商ID获取供应商信息
    Args:
        vendor_id (int): 供应商ID
    Returns:
        list: 包含供应商信息元组的列表，每个元组包含(VendorID、Business Name、Location、Account、Secret)
    """
    vendor_dao = VendorDAO()
    vendor = vendor_dao.get_vendor_by_id(vendor_id)
    if vendor:
        return [(vendor.v_id, vendor.business_name, vendor.geo_presence, vendor.v_account, vendor.v_secret)]
    return []


# 测试代码
def test_get_vendor_data():
    print("\n测试根据ID获取供应商数据:")
    # 测试存在的供应商ID
    test_vendor_id = 20001
    data = get_vendor_data_by_id(test_vendor_id)
    print("供应商{0}的数据: {1}".format(test_vendor_id, data))
    
    # 测试不存在的供应商ID
    test_vendor_id = 9999
    data = get_vendor_data_by_id(test_vendor_id)
    print("不存在的供应商{0}的数据: {1}".format(test_vendor_id, data))


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
    # from dao.manager_dao import ManagerDAO
    # from dao.Vendor_dao import VendorDAO

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



# 测试代码
def test_get_products_by_tag():
    print("\n测试根据标签获取产品:")
    # 测试标签ID为1的产品
    data = get_products_by_tag_id(1)
    print("标签1的产品数据: {0}".format(data))
    
    # 测试标签ID为2的产品
    data = get_products_by_tag_id(2)
    print("标签2的产品数据: {0}".format(data))



# 测试代码
def test_get_product_by_id():
    print("\n测试根据产品ID获取产品:")
    # 测试产品ID为1的产品
    data = get_product_by_id(1)
    print("产品1的数据: {0}".format(data))
    
    # 测试不存在的产品ID
    data = get_product_by_id(9999)
    print("不存在的产品数据: {0}".format(data))



def get_purchase_records_by_user(user_id):
    """根据用户ID获取购买记录
    Args:
        user_id (int): 用户ID
    Returns:
        list: 包含购买记录元组的列表，每个元组包含(RecordID、ShippingID、TotalMoney、Status、DateTime)
    """
    # from dao.purchase_dao import PurchaseDAO
    
    # 创建DAO实例并获取用户的购买记录
    purchase_dao = PurchaseDAO()
    records = purchase_dao.get_purchases_by_customer(user_id)
    
    # 转换为指定格式的元组列表
    return [(r.r_id, r.s_id, float(r.toal), r.r_status, r.r_date) 
            for r in records]


# 测试代码
def test_get_purchase_records():
    print("\n测试获取用户购买记录:")
    # 测试用户ID为1的购买记录
    test_user_id = 1
    records = get_purchase_records_by_user(test_user_id)
    print("用户{0}的购买记录: {1}".format(test_user_id, records))
    
    # 测试不存在的用户ID
    test_user_id = 9999
    records = get_purchase_records_by_user(test_user_id)
    print("不存在用户{0}的购买记录: {1}".format(test_user_id, records))


if __name__ == "__main__":
    test_get_data()
    test_get_products_by_tag()
    test_get_product_by_id()
    test_get_purchase_records()
    test_get_vendor_data()
