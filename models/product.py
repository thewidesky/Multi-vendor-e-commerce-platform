import decimal

class Product:
    def __init__(self, v_id, category_id, p_name, price, stock, 
                 p_status=None, p_picture=None, p_id=None):
        self.p_id = p_id
        self.v_id = v_id
        self.category_id = category_id
        self.p_name = p_name
        self.price = price  # 应使用decimal.Decimal类型
        self.stock = stock
        self.p_status = p_status
        self.p_picture = p_picture

        # 数据校验
        if stock < 0:
            raise ValueError("Stock cannot be negative")

    def to_dict(self):
        return {
            'p_id': self.p_id,
            'v_id': self.v_id,
            'category_id': self.category_id,
            'p_name': self.p_name,
            'price': float(self.price),
            'stock': self.stock,
            'p_status': self.p_status,
            'p_picture': self.p_picture
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            v_id=data['v_id'],
            category_id=data['category_id'],
            p_name=data['p_name'],
            price=decimal.Decimal(str(data['price'])),
            stock=data['stock'],
            p_status=data.get('p_status'),
            p_picture=data.get('p_picture'),
            p_id=data.get('p_id')
        )