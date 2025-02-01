# routes/groups.py
from flask import Blueprint, request, jsonify
from database import db
from models import Group, GroupMember, User

groups_bp = Blueprint('groups', __name__)

# Create a new group
@groups_bp.route('/', methods=['POST'])
def create_group():
    data = request.get_json()
    name = data.get('name')
    members = data.get('members')  # Expected as a list of user IDs
    if not name or not members:
        return jsonify({"error": "Missing group name or members"}), 400

    group = Group(name=name)
    db.session.add(group)
    db.session.commit()

    # Add each user to the group
    for user_id in members:
        gm = GroupMember(group_id=group.id, user_id=user_id)
        db.session.add(gm)
    db.session.commit()

    return jsonify({"id": group.id, "name": group.name}), 201

# Optional: Create a user for testing
@groups_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"error": "Missing user name"}), 400

    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "name": user.name}), 201
