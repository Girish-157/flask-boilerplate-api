from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from project.models import db, User

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db:5432/mydatabase'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!

    db.init_app(app)
    jwt = JWTManager(app)

    @app.route('/api/authenticate', methods=['POST'])
    def authenticate():
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return jsonify({"msg": "Invalid username or password"}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)

    @app.route('/api/me', methods=['GET'])
    @jwt_required()
    def me():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return jsonify(id=user.id, username=user.username)

    return app

