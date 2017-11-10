from db import db

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    stripeID = db.Column(db.String(50),unique=True)
    email = db.Column(db.String(256), unique=True)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(30))

    # length of stripeID is not specified in official document,
    # it should be less than 20 according to observation,
    # but we leave it 50 just in case

    def __init__(self,_id,stripeID,email,phone,password):
        self.id = _id
        self.stripeID = stripeID
        self.email = email
        self.phone = phone
        self.password = password

    def json(self):
        return {
            "id" : self.id,
            "stripeID" : self.stripeID,
            "email" : self.email,
            "phone" : self.phone,
            "password" : self.password
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_stripe_id(cls,stripeID):
        return cls.query.filter_by(stripeID=stripeID).first()


    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_phone(cls,phone):
        return cls.query.filter_by(phone=phone).all()

    def save_to_db(self):   ## upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):   ## delete
        db.session.delete(self)
        db.session.commit()
