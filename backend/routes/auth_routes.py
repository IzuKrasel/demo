# backend/routes/auth_routes.py
from flask import Blueprint, request, session, jsonify
from backend.models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.authenticate(
        data.get('login', ''),
        data.get('password', '')
    )
    if not user:
        return jsonify({
            'success': False,
            'message': 'Неверный логин или пароль'
        }), 401

    # Очистка старой сессии (защита от fixation)
    session.clear()

    session['user_id'] = user['id']
    session['role'] = user['role']
    session['login'] = user['login']
    session.permanent = True

    return jsonify({
        'success': True,
        'role': user['role'],
        'redirect': '/admin' if user['role'] == 'admin' else '/dashboard'
    }), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    user = User(
        login=data.get('login', '').strip(),
        password=data.get('password', ''),
        email=data.get('email', '').strip(),
        phone=data.get('phone', '').strip(),
        role='user'
    )
    ok, result = user.save()
    if not ok:
        return jsonify({'success': False, 'message': result}), 400
    return jsonify({'success': True, 'user_id': result}), 201