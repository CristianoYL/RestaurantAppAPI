from db import db

class RestaurantModel(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    fee = db.Column(db.Float(precision=2))
    limit = db.Column(db.Float(precision=2))
    address = db.Column(db.String(200))
    openTime = db.Column(db.String(10))
    closeTime = db.Column(db.String(10))
    isOpen = db.Column(db.Boolean)
    logo = db.Column(db.String(200))
    promo = db.Column(db.String(100))
    phone = db.Column(db.String(20))


    def __init__(self,_id,name,fee,limit,address,openTime,closeTime,isOpen,logo,promo,phone):
        self.id = _id
        self.name = name
        self.fee = fee
        self.limit = limit
        self.address = address
        self.openTime = openTime
        self.closeTime = closeTime
        self.isOpen = isOpen
        self.logo = logo
        self.promo = promo
        self.phone = phone

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'fee': self.fee,
            'limit': self.limit,
            'address': self.address,
            'openTime': self.openTime,
            'closeTime': self.closeTime,
            'isOpen': self.isOpen,
            'logo': self.logo,
            'promo': self.promo,
            'phone': self.phone
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()


    def save_to_db(self):   # upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):   # delete
        db.session.delete(self)
        db.session.commit()
