class Shipping:
    def __init__(self, c_id, s_location, s_is_default=False, s_id=None):
        self.s_id = s_id
        self.c_id = c_id
        self.s_location = s_location
        self.s_is_default = s_is_default

    def to_dict(self):
        return {
            's_id': self.s_id,
            'c_id': self.c_id,
            's_location': self.s_location,
            's_is_default': self.s_is_default
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            c_id=data['c_id'],
            s_location=data['s_location'],
            s_is_default=data.get('s_is_default', False),
            s_id=data.get('s_id')
        )
