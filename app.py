import os
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from models import db, bcrypt, User, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key-change-in-production'

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# --- HOME / WELCOME ROUTE ---
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Full Auth Productivity Backend API!"}), 200


# --- AUTHENTICATION ENDPOINTS ---

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=str(new_user.id))
    return jsonify({"user": new_user.to_dict(), "access_token": access_token}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"user": user.to_dict(), "access_token": access_token}), 200


@app.route('/me', methods=['GET'])
@jwt_required()
def check_session():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200


# --- PROTECTED RESOURCE CRUD ENDPOINTS ---

@app.route('/resources', methods=['GET'])
@jwt_required()
def get_resources():
    current_user_id = int(get_jwt_identity())
    
    # Query parameters for pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    pagination = Task.query.filter_by(user_id=current_user_id).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        "tasks": [task.to_dict() for task in pagination.items],
        "total": pagination.total,
        "page": page,
        "per_page": per_page,
        "pages": pagination.pages
    }), 200


@app.route('/resources/<int:id>', methods=['GET'])
@jwt_required()
def get_resource(id):
    current_user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=id, user_id=current_user_id).first()

    if not task:
        return jsonify({"error": "Resource not found or unauthorized"}), 404

    return jsonify(task.to_dict()), 200


@app.route('/resources', methods=['POST'])
@jwt_required()
def create_resource():
    current_user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    title = data.get('title')
    if not title:
        return jsonify({"error": "Title is required"}), 400

    new_task = Task(
        title=title,
        description=data.get('description', ''),
        user_id=current_user_id
    )

    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201


@app.route('/resources/<int:id>', methods=['PATCH', 'PUT'])
@jwt_required()
def update_resource(id):
    current_user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=id, user_id=current_user_id).first()

    if not task:
        return jsonify({"error": "Resource not found or unauthorized"}), 404

    data = request.get_json() or {}
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']

    db.session.commit()
    return jsonify(task.to_dict()), 200


@app.route('/resources/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_resource(id):
    current_user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=id, user_id=current_user_id).first()

    if not task:
        return jsonify({"error": "Resource not found or unauthorized"}), 404

    db.session.delete(task)
    db.session.commit()
    return make_response('', 204)


if __name__ == '__main__':
    app.run(port=5555, debug=True)