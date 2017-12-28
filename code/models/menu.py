from db import db

class MenuModel(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    name = db.Column(db.String(30), unique=True)
    price = db.Column(db.Float(precision=2))
    category = db.Column(db.String(20))
    description = db.Column(db.String(300))
    spicy = db.Column(db.Integer)
    isAvailable = db.Column(db.Boolean)
    isRecommended = db.Column(db.Boolean)

    def __init__(self,_id,rid,name,price,category,description,spicy,isAvailable,isRecommended):
        self.id = _id
        self.rid=rid
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.spicy = spicy
        self.isAvailable = isAvailable
        self.isRecommended = isRecommended

    def json(self):
        return {
            'id': self.id,
            'rid': self.rid,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'description': self.description,
            'spicy': self.spicy,
            'isAvailable': self.isAvailable,
            'isRecommended': self.isRecommended
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls,mid):
        return cls.query.filter_by(id=mid).first()

    @classmethod
    def find_by_restaurant(cls,rid):
        return cls.query.filter_by(rid=rid)

    @classmethod
    def find_by_name(cls,rid,name):
        return cls.query.filter_by(rid=rid,name=name).first()

    @classmethod
    def find_like_name(cls,rid,name):
        return cls.query.filter_by(rid=rid).filter(cls.name.like(mid))

    @classmethod
    def find_by_category(cls,rid,category):
        return cls.query.filter_by(rid=rid,category=category)

    def save_to_db(self):   ## upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):   ## delete
        db.session.delete(self)
        db.session.commit()
