class Category:
    def __init__(self, category_name, description=None, category_id=None):
        self.category_id = category_id
        self.category_name = category_name
        self.description = description

    def to_dict(self):
        return {
            'category_id': self.category_id,
            'category_name': self.category_name,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            category_name=data['category_name'],
            description=data.get('description'),
            category_id=data.get('category_id')
        )