from flask import Blueprint

def register_blueprints(app):
    from .main import main_bp
    from .auth import auth_bp
    from .borrow import borrow_bp
    from .admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(borrow_bp)
    app.register_blueprint(admin_bp)
