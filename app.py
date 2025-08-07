from flask import Flask, session
from config import SECRET_KEY, DEBUG_MODE, HOST, PORT
from routes.main import main_bp
from routes.auth import auth_bp
from routes.pay import pay_bp
from routes.review import review_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Регистрация маршрутов
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(pay_bp)
app.register_blueprint(review_bp)

if __name__ == "__main__":
    app.run(debug=DEBUG_MODE, host=HOST, port=PORT)
