import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.Vendor import Vendor
from models.Product import Product
from models.Feedback import Feedback
from models.RecordsDetail import RecordsDetail
from models.Records import Records
from models.Manager import Manager
import decimal
import datetime

def main():
    # 测试Vendor类
    vendor = Vendor(
        business_name="Test Vendor",
        geo_presence="Beijing",
        v_account="vendor@test.com",
        v_secret="123456"
    )
    print("\n[Vendor测试]")
    print("对象字段值:", vars(vendor))
    print("字典转换:", vendor.to_dict())

    # 测试Product类
    try:
        bad_product = Product(
            v_id=1,
            category_id=1,
            p_name="Invalid Product",
            price=decimal.Decimal("-10.00"),  # 触发价格验证
            stock=100
        )
    except ValueError as e:
        print("\n[Product异常测试] 捕获预期错误:", e)

    valid_product = Product(
        v_id=1,
        category_id=2,
        p_name="Python编程书",
        price=decimal.Decimal("99.99"),
        stock=50
    )
    print("\n[Product正常测试]")
    print("价格类型:", type(valid_product.price))  # 验证Decimal类型

    # 测试Feedback评分限制
    try:
        Feedback(c_id=1, v_id=1, rating=6)  # 无效评分
    except ValueError as e:
        print("\n[Feedback异常测试] 捕获评分错误:", e)

    # 测试Manager类
    print("\n[Manager测试]")
    manager = Manager(m_secret="securePassword123")
    print("管理员默认ID:", manager.m_id)
    print("密码字段验证:", manager.m_secret == "securePassword123")

    # 测试RecordsDetail计算逻辑
    try:
        RecordsDetail(
            r_id=1,
            p_id=1,
            price=decimal.Decimal("25.00"),
            quantity=3,
            subtotal=decimal.Decimal("75.00")  # 正确计算
        )
        print("\n[RecordsDetail正常测试] 小计验证通过")

        RecordsDetail(
            r_id=1,
            p_id=1,
            price=decimal.Decimal("20.00"),
            quantity=2,
            subtotal=decimal.Decimal("50.00")  # 错误计算
        )
    except ValueError as e:
        print("\n[RecordsDetail异常测试] 捕获小计错误:", e)

    # 测试日期处理
    record = Records(
        r_id=1001,
        s_id=1,
        c_id=1,
        toal=decimal.Decimal("199.99"),
        r_status=True,
        r_date=datetime.date.today()
    )
    print("\n[Records日期测试]")
    print("日期对象类型:", type(record.r_date))
    print("日期值:", record.r_date)

if __name__ == "__main__":
    main()