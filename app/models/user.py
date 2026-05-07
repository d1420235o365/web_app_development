from datetime import datetime
from . import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='borrower')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    borrow_records = db.relationship('BorrowRecord', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    @classmethod
    def create(cls, username, password_hash, role='borrower'):
        user = cls(username=username, password_hash=password_hash, role=role)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
