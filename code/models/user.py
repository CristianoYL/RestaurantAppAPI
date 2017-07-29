from db import db

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(50))

    def __init__(self,_id,phone,password):
        self.id = _id
        self.phone = phone
        self.password = password

    def json(self):
        return {
            "id" : self.id,
            "phone" : self.phone,
            "password" : self.password
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_phone(cls,phone):
        return cls.query.filter_by(phone=phone).first()

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):   ## upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):   ## delete
        db.session.delete(self)
        db.session.commit()
