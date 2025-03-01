import decimal


class RecordsDetail:
    def __init__(self, r_id, p_id, price, quantity, subtotal, rd_id=None):
        self.rd_id = rd_id
        self.r_id = r_id
        self.p_id = p_id
        self.price = decimal.Decimal(str(price))
        self.quantity = quantity
        self.subtotal = decimal.Decimal(str(subtotal))

        # 数据校验
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.subtotal != self.price * self.quantity:
            raise ValueError("Subtotal must equal price multiplied by quantity")

    def to_dict(self):
        return {
            'rd_id': self.rd_id,
            'r_id': self.r_id,
            'p_id': self.p_id,
            'price': float(self.price),
            'quantity': self.quantity,
            'subtotal': float(self.subtotal)
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            r_id=data['r_id'],
            p_id=data['p_id'],
            price=data['price'],
            quantity=data['quantity'],
            subtotal=data['subtotal'],
            rd_id=data.get('rd_id')
        )