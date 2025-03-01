class Vendor:
    def __init__(self, business_name, geo_presence, v_account, v_secret, v_id=None):
        self.v_id = v_id  # 自增ID创建时可为None
        self.business_name = business_name
        self.geo_presence = geo_presence
        self.v_account = v_account
        self.v_secret = v_secret

    def to_dict(self):
        return {
            'v_id': self.v_id,
            'business_name': self.business_name,
            'geo_presence': self.geo_presence,
            'v_account': self.v_account,
            'v_secret': self.v_secret
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            business_name=data['business_name'],
            geo_presence=data['geo_presence'],
            v_account=data['v_account'],
            v_secret=data['v_secret'],
            v_id=data.get('v_id')  # 允许v_id不存在（新建时）
        )