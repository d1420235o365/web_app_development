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
        """建立借閱紀錄"""
        try:
            record = cls(user_id=user_id, book_id=book_id)
            db.session.add(record)
            db.session.commit()
            return record
        except Exception as e:
            db.session.rollback()
            print(f"Error creating borrow record: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有借閱紀錄列表"""
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting all borrow records: {e}")
            return []

    @classmethod
    def get_by_id(cls, record_id):
        """依據 ID 取得借閱紀錄"""
        try:
            return cls.query.get(record_id)
        except Exception as e:
            print(f"Error getting borrow record by id: {e}")
            return None

    @classmethod
    def get_active_by_user(cls, user_id):
        """取得特定使用者的當前借閱中紀錄"""
        try:
            return cls.query.filter_by(user_id=user_id, status='Active').all()
        except Exception as e:
            print(f"Error getting active records for user: {e}")
            return []

    def mark_as_returned(self):
        """標記書籍為已歸還"""
        try:
            self.return_date = datetime.utcnow()
            self.status = 'Returned'
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error marking record as returned: {e}")
            return False

    def update(self, **kwargs):
        """更新紀錄資訊"""
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating borrow record: {e}")
            return False

    def delete(self):
        """刪除借閱紀錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting borrow record: {e}")
            return False
