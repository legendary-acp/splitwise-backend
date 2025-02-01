# routes/balances.py
from flask import Blueprint, jsonify
from models import Group, Expense
from collections import defaultdict

balances_bp = Blueprint('balances', __name__)

@balances_bp.route('/<int:group_id>/balances', methods=['GET'])
def get_balances(group_id):
    group = Group.query.get(group_id)
    if not group:
        return jsonify({"error": "Group not found"}), 404

    # Compute net balances: for each expense, users (other than the payer) owe their share.
    balances = defaultdict(float)
    expenses = Expense.query.filter_by(group_id=group_id).all()

    for expense in expenses:
        for split in expense.splits:
            if split.user_id == expense.paid_by:
                continue
            balances[expense.paid_by] += split.amount
            balances[split.user_id] -= split.amount

    # Format the response including each member's balance.
    result = []
    for member in group.members:
        result.append({
            "user_id": member.user_id,
            "balance": balances[member.user_id]
        })
    return jsonify(result), 200
