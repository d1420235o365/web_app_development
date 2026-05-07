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
        """新增書籍到館藏"""
        try:
            book = cls(title=title, author=author, isbn=isbn, category=category)
            db.session.add(book)
            db.session.commit()
            return book
        except Exception as e:
            db.session.rollback()
            print(f"Error creating book: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有書籍列表"""
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting all books: {e}")
            return []

    @classmethod
    def get_by_id(cls, book_id):
        """依據 ID 取得書籍詳情"""
        try:
            return cls.query.get(book_id)
        except Exception as e:
            print(f"Error getting book by id: {e}")
            return None

    def update(self, **kwargs):
        """更新書籍資訊"""
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating book: {e}")
            return False

    def delete(self):
        """從館藏中刪除書籍"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting book: {e}")
            return False
