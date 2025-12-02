from flask import Flask
import psycopg2
from flask_mail import Mail

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'kevin'

    # 🧩 PostgreSQL database connection settings
    app.config['DB_HOST'] = 'localhost'
    app.config['DB_NAME'] = 'lms_system'
    app.config['DB_USER'] = 'postgres'
    app.config['DB_PASSWORD'] = 'password01'  # change if needed

    # 🧠 SMTP / Email configuration (Gmail example)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'kevlat09@gmail.com'     # <-- change this
    app.config['MAIL_PASSWORD'] = 'lmhh vsqe zouh iwgh'  # <-- Gmail App Password
    app.config['MAIL_DEFAULT_SENDER'] = ('LMS System', 'yourgmail@gmail.com')

    # Initialize Flask-Mail
    mail.init_app(app)

    # 🧠 Helper: create connection function
    def get_db_connection():
        conn = psycopg2.connect(
            host=app.config['DB_HOST'],
            database=app.config['DB_NAME'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD']
        )
        return conn

    app.get_db_connection = get_db_connection

    # 🔗 Blueprints
    from .auth import auth
    from .views import views

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    return app
