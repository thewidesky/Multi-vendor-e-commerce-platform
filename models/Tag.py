class Tag:
    def __init__(self, tag_name, t_id=None):
        self.t_id = t_id
        self.tag_name = tag_name

    def to_dict(self):
        return {
            't_id': self.t_id,
            'tag_name': self.tag_name
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            tag_name=data['tag_name'],
            t_id=data.get('t_id')
        )