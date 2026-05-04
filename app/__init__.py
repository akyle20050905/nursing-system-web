from flask import Flask, redirect, url_for
from app.extensions import db, swagger
import os

def create_app():
    app = Flask(__name__)
    
    # 配置 (建議未來改用環境變數)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:kyle0905@127.0.0.1:3306/nursing_shift"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "super_secret_key_for_demo_purposes"

    # 初始化擴充套件
    db.init_app(app)
    swagger.init_app(app)

    # 延遲導入以避免循環引用
    from app.routes.nurse_routes import nurse_bp
    from app.routes.task_routes import task_bp
    from app.routes.patient_routes import patient_bp

    # 註冊 Blueprints
    app.register_blueprint(nurse_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(patient_bp)

    with app.app_context():
        # 工程師修正：除非顯式要求，否則不應每次啟動都 drop_all
        # 如果是初期開發需要頻繁更動 Schema，建議使用 Flask-Migrate
        db.create_all()
        
        # 執行初始測試資料植入
        from app.controllers.nurse_controller import seed_hospital_data
        seed_hospital_data()

    @app.route("/")
    def index():
        return redirect(url_for('nurse_bp.login_ui'))

    return app