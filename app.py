import os
from flask import Flask
from dotenv import load_dotenv
from app.models import db, init_db
from app.routes import register_blueprints

# 載入環境變數
load_dotenv()

def create_app():
    app = Flask(__name__, 
                instance_relative_config=True,
                template_folder='app/templates',
                static_folder='app/static')
    
    # 設定 Flask 配置
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(app.instance_path, 'library.db')}"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化資料庫
    init_db(app)

    # 註冊路由
    register_blueprints(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
