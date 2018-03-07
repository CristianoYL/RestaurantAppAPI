from db import db


class MenuModel(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    restaurantID = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    name = db.Column(db.String(30), unique=True)
    price = db.Column(db.Float(precision=2))
    category = db.Column(db.String(20))
    description = db.Column(db.String(300))
    spicy = db.Column(db.Integer)
    isAvailable = db.Column(db.Boolean)
    isRecommended = db.Column(db.Boolean)
    image = db.Column(db.String(2000))

    restaurant = db.relationship('RestaurantModel')

    def __init__(self, _id, restaurantID, name, price, category, description, spicy, isAvailable, isRecommended, image):
        self.id = _id
        self.restaurantID = restaurantID
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.spicy = spicy
        self.isAvailable = isAvailable
        self.isRecommended = isRecommended
        self.image = image

    def json(self):
        return {
            'id': self.id,
            'restaurantID': self.restaurantID,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'description': self.description,
            'spicy': self.spicy,
            'isAvailable': self.isAvailable,
            'isRecommended': self.isRecommended,
            'image': self.image
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, mid):
        return cls.query.filter_by(id=mid).first()

    @classmethod
    def find_by_name(cls, restaurantID, name):
        return cls.query.filter_by(restaurantID=restaurantID, name=name).first()

    @classmethod
    def find_like_name(cls, restaurantID, name):
        return cls.query.filter_by(restaurantID=restaurantID).filter(cls.name.like(name))

    @classmethod
    def find_by_category(cls, restaurantID, category):
        return cls.query.filter_by(restaurantID=restaurantID, category=category)

    def save_to_db(self):  # upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):  # delete
        db.session.delete(self)
        db.session.commit()
