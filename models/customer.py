class Customer:
    def __init__(self, c_name, geo_presence, c_account, c_secret, c_id=None):
        self.c_id = c_id
        self.c_name = c_name
        self.geo_presence = geo_presence
        self.c_account = c_account
        self.c_secret = c_secret

    def to_dict(self):
        return {
            'c_id': self.c_id,
            'c_name': self.c_name,
            'geo_presence': self.geo_presence,
            'c_account': self.c_account,
            'c_secret': self.c_secret
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            c_name=data['c_name'],
            geo_presence=data['geo_presence'],
            c_account=data['c_account'],
            c_secret=data['c_secret'],
            c_id=data.get('c_id')
        )