class Manager:
    def __init__(self, m_name, m_secret, m_id=None):
        self.m_id = m_id
        self.m_name = m_name
        self.m_secret = m_secret

    def to_dict(self):
        return {
            'm_id': self.m_id,
            'm_name':self.m_name,
            'm_secret': self.m_secret
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            m_name=data['m_name'],
            m_secret=data['m_secret'],
            m_id=data.get('m_id')
        )