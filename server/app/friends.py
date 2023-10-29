from flask import (
    Blueprint, jsonify, request
)

from .models import User, FriendRequest

# define blueprint
bp = Blueprint("friends", __name__, url_prefix="/friends")

from app import db

# Retrieving friend requests
@bp.route('/request/<int:user_id>', methods=['GET'])
def get_friend_requests(user_id):
    # Check if user with matching id exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            'status': 'error',
            'msg': 'User not found'
        }), 404
    
    # If no friend requests for user
    friend_requests = FriendRequest.query.filter_by(to_user_id=user_id).all()
    print(friend_requests)
    if not friend_requests:
        return jsonify({
            'status': 'success',
            'data': []
        }), 200
    
    # Extract useful information from each request and database
    friend_requests_list = []
    for request in friend_requests:

        information = {
            'from_username': User.query.get(request.from_user_id).username,
            'from_user_id': request.from_user_id,
        }
        friend_requests_list.append(information)

    return jsonify({
        'status': 'success',
        'data': friend_requests_list
    }), 200

@bp.route('/add', methods=['POST'])
def add_friend():
    data: dict = request.get_json()
    friend_id = data.get('friend_id')
    user_id = data.get('user_id')
    print(friend_id, user_id)

    # Get friend request from database and remove it
    request_to_remove = FriendRequest.query.filter_by(from_user_id=friend_id, to_user_id=user_id).first()
    print(request_to_remove.from_user_id)
    db.session.delete(request_to_remove)
    
    # Add friends. Because of sqlalchemy relationships this should add to both friends lists
    user = User.query.get(user_id)
    friend = User.query.get(friend_id)
    user.friends.append(friend)
    friend.friends.append(user)

    db.session.commit()

    return jsonify({
        'status': 'success',
        'msg': 'Friend added to list'
    }), 201

# No error handling, assumes users exist
@bp.route('/decline', methods=['POST'])
def decline_friend():
    data = request.get_json()
    friend_id = data.get('friend_id')
    user_id = data.get('user_id')

    # Get friend request from database and remove it
    request_to_remove = FriendRequest.query.filter_by(from_user_id=friend_id, to_user_id=user_id).first()
    db.session.delete(request_to_remove)

    db.session.commit()

    return jsonify({
        'status': 'success',
        'msg': 'Friend request declined'
    }), 201
