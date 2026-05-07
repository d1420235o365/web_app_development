from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    from .user import User
    from .book import Book
    from .borrow_record import BorrowRecord
    with app.app_context():
        db.create_all()
