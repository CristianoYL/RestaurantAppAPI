from db import db

class TestModel(db.Model):
    __tablename__ = 'test'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))

    def __init__(self,_id,name):
        self.id = _id
        self.name = name

    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
