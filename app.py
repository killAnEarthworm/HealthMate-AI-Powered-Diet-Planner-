from flask import Flask
from flask_mail import Mail
from blueprints.data_board_personal_center import data_board_personal_center_bp
from blueprints.nutrition_storage_login import nutrition_storage_login_bp
from blueprints.health_report_weight_prediction import health_report_weight_prediction_bp
from blueprints.generate_plan import generate_plan_bp
from database import db  # 导入db对象

mail2 = Mail()


def create_app():
    app = Flask(__name__)
    app.secret_key = '12345678'  # 替换为你的随机字符串
    # 数据库配置 mysql+pymysql://(用户名):(密码)@localhost/healthoney
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/healthoney'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 添加fastgpt的API配置
    app.config['FASTGPT_API_URL'] = "http://localhost:3000/api/v1/chat/completions"
    app.config['FASTGPT_API_KEY'] = 'fastgpt-tAN5X7i0KxjTGGkWFsWiNHMXYfu6ZA3O5vYWZUbXF1mvkaR3ZxcMdDUAVjyQT5h' # 替换为你的api密钥

    # 初始化数据库
    db.init_app(app)

    # 配置邮件服务器
    app.config['MAIL_SERVER'] = 'smtp.qq.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'xxx@qq.com'  # 替换为你的邮箱
    app.config['MAIL_PASSWORD'] = 'xxx'  # 替换为你的授权码
    app.config['MAIL_DEFAULT_SENDER'] = 'xxx@qq.com'  # 默认发件人

    # # 初始化 Flask-Mail
    mail2.init_app(app)

    # 注册蓝图
    app.register_blueprint(data_board_personal_center_bp)
    app.register_blueprint(nutrition_storage_login_bp)
    app.register_blueprint(health_report_weight_prediction_bp)
    app.register_blueprint(generate_plan_bp)

    return app


# 启动应用
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
