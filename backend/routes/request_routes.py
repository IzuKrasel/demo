from flask import Blueprint, request, jsonify, render_template, session
from backend.auth.decorators import (
    login_required, participant_required
)
from backend.models.request import Request
from backend.models.event import Event

request_bp = Blueprint('requests', __name__)


@request_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@request_bp.route('/api/requests', methods=['GET'])
@login_required
def get_my_requests():
    data = Request.get_by_user(session['user_id'])
    return jsonify({'success': True, 'requests': data}), 200


@request_bp.route('/create_request', methods=['GET', 'POST'])
@participant_required
def create_request():
    if request.method == 'GET':
        events = Event.get_all()
        return render_template('create_request.html', events=events)

    data = request.get_json()
    new_request = Request(
        user_id=session['user_id'],
        event_id=int(data.get('event_id')),
        status_id=1
    )
    request_id = new_request.save()
    return jsonify({'success': True, 'request_id': request_id}), 201