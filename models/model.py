class AbstractModel:
    def __init__(self, validator, db, adapter):
        self.validator = validator
        self.db = db
        self.adaptor = adapter
        self.collection_name = ''

        self.fields = {}
        self.create_required_fields = []
        self.create_optional_fields = []
        self.update_required_fields = []
        self.update_optional_fields = []

    def create(self, entity):
        try:
            self.validator.validate(entity, self.fields, self.create_required_fields, self.create_optional_fields)
            self.adaptor.adapt(entity)
            res = self.db.insert_one(entity, self.collection_name)
            return True
        except Exception as e:
            return False

    def find(self, entity):  # find all
        return self.db.find(entity, self.collection_name)

    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)

    def update(self, id, entity):
        self.validator.validate(entity, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, entity, self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
