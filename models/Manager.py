class Manager:
    def __init__(self, m_secret, m_id=None):
        self.m_id = m_id
        self.m_secret = m_secret

    def to_dict(self):
        return {
            'm_id': self.m_id,
            'm_secret': self.m_secret
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            m_secret=data['m_secret'],
            m_id=data.get('m_id')
        )