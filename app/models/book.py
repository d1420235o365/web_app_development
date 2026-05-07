from datetime import datetime
from . import db

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    isbn = db.Column(db.String(20))
    category = db.Column(db.String(50))
    status = db.Column(db.String(20), nullable=False, default='Available')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    borrow_records = db.relationship('BorrowRecord', backref='book', lazy=True)

    def __repr__(self):
        return f'<Book {self.title}>'

    @classmethod
    def create(cls, title, author=None, isbn=None, category=None):
        book = cls(title=title, author=author, isbn=isbn, category=category)
        db.session.add(book)
        db.session.commit()
        return book

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, book_id):
        return cls.query.get(book_id)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
