from db import db

dishes = db.table('dishes',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
    db.Column('menu_id', db.Integer, db.ForeignKey('menu.id'))
)

class OrderModel(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    originalAmount = db.Column(db.Float(precision=2))
    finalAmount = db.Column(db.Float(precision=2))
    # TODO menu list

    menus = db.relationship('Menu', secondary = dishes,
                            backref = db.backref('orders', lazy = 'dynamic'))

    status = closeTime = db.Column(db.String(10))
    time = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    deliverAddress = db.Column(db.String(200))



    def __init__(self,oid, uid, originalAmount, finalAmount, status, time, phone, deliverAddress):
        self.id = oid
        self.uid = uid
        self.originalAmount = originalAmount
        self.finalAmount = finalAmount
        self.status = status
        self.time = time
        self.phone = phone
        self.deliverAddress = deliverAddress

    def json(self):
        return {
            'oid' : self.id,
            'uid' : self.uid,
            'originalAmount' self.originalAmount,
            'finalAmount' : self.finalAmount,
            'status': self.status,
            'time' : self.time,
            'phone' : self.phone,
            'deliverAddress' : self.deliverAddress,
            'midList': [menu.id for menu in menus]
        }

    def json_extend(self):
        return {
            'oid' : self.id,
            'uid' : self.uid,
            'originalAmount' self.originalAmount,
            'finalAmount' : self.finalAmount,
            'status': self.status,
            'time' : self.time,
            'phone' : self.phone,
            'deliverAddress' : self.deliverAddress,
            'menu_list': [menu.json() for menu in menus]
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_user_id(cls, uid):
        return cls.query.filter_by(id=id).all()

    def save_to_db(self):   # upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):   # delete
        db.session.delete(self)
        db.session.commit()
