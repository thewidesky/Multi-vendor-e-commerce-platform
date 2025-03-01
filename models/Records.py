import decimal
from datetime import datetime

class Records:
    def __init__(self, r_id, s_id, c_id, toal, r_status, r_date):
        self.r_id = r_id
        self.s_id = s_id
        self.c_id = c_id
        self.toal = decimal.Decimal(str(toal))
        self.r_status = r_status
        self.r_date = r_date  # 期望是datetime.date对象

        # 数据校验
        if self.toal < 0:
            raise ValueError("Total amount cannot be negative")

    def to_dict(self):
        return {
            'r_id': self.r_id,
            's_id': self.s_id,
            'c_id': self.c_id,
            'toal': float(self.toal),
            'r_status': self.r_status,
            'r_date': self.r_date.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        date_str = data.get('r_date')
        if isinstance(date_str, str):
            r_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        return cls(
            r_id=data['r_id'],
            s_id=data['s_id'],
            c_id=data['c_id'],
            toal=data['toal'],
            r_status=data['r_status'],
            r_date=r_date
        )