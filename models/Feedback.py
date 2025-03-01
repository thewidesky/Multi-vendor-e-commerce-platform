class Feedback:
    def __init__(self, c_id, v_id, comment=None, rating=None):
        self.c_id = c_id
        self.v_id = v_id
        self.comment = comment
        self.rating = rating

        # 数据校验
        if rating and (rating < 0 or rating > 5):
            raise ValueError("Rating must be between 0-5")

    def to_dict(self):
        return {
            'c_id': self.c_id,
            'v_id': self.v_id,
            'comment': self.comment,
            'rating': self.rating
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            c_id=data['c_id'],
            v_id=data['v_id'],
            comment=data.get('comment'),
            rating=data.get('rating')
        )