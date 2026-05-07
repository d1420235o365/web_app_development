from datetime import datetime
from . import db

class BorrowRecord(db.Model):
    __tablename__ = 'borrow_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Active')

    def __repr__(self):
        return f'<BorrowRecord User:{self.user_id} Book:{self.book_id}>'

    @classmethod
    def create(cls, user_id, book_id):
        record = cls(user_id=user_id, book_id=book_id)
        db.session.add(record)
        db.session.commit()
        return record

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, record_id):
        return cls.query.get(record_id)

    @classmethod
    def get_active_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id, status='Active').all()

    def mark_as_returned(self):
        self.return_date = datetime.utcnow()
        self.status = 'Returned'
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
