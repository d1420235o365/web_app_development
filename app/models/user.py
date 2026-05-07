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
        """建立新使用者並存入資料庫"""
        try:
            user = cls(username=username, password_hash=password_hash, role=role)
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有使用者列表"""
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []

    @classmethod
    def get_by_id(cls, user_id):
        """依據 ID 取得單一使用者"""
        try:
            return cls.query.get(user_id)
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None

    @classmethod
    def get_by_username(cls, username):
        """依據使用者名稱取得單一使用者"""
        try:
            return cls.query.filter_by(username=username).first()
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None

    def update(self, **kwargs):
        """更新使用者資料"""
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating user: {e}")
            return False

    def delete(self):
        """從資料庫刪除該使用者"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting user: {e}")
            return False
