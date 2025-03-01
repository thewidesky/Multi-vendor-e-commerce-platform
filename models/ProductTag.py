class ProductTag:
    """商品标签关联表（多对多关系）"""
    def __init__(self, p_id, t_id):
        self.p_id = p_id
        self.t_id = t_id

    def to_dict(self):
        return {
            'p_id': self.p_id,
            't_id': self.t_id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            p_id=data['p_id'],
            t_id=data['t_id']
        )