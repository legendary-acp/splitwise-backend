# routes/expenses.py
from flask import Blueprint, request, jsonify
from database import db
from models import Group, Expense, ExpenseSplit

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/<int:group_id>/expenses', methods=['POST'])
def add_expense(group_id):
    data = request.get_json()
    paid_by = data.get('paid_by')
    total_amount = data.get('total_amount')
    description = data.get('description', '')
    split_type = data.get('split_type')  # "equal" or "percentage"
    splits_data = data.get('splits')  # For percentage split: {user_id: percentage}

    # Validate group existence
    group = Group.query.get(group_id)
    if not group:
        return jsonify({"error": "Group not found"}), 404

    expense = Expense(group_id=group_id, paid_by=paid_by,
                      total_amount=total_amount, description=description,
                      split_type=split_type)
    db.session.add(expense)
    db.session.commit()

    # Retrieve all group members
    group_members = [member.user_id for member in group.members]

    expense_splits = []
    if split_type == 'equal':
        split_amount = total_amount / len(group_members)
        for user_id in group_members:
            expense_splits.append(
                ExpenseSplit(expense_id=expense.id, user_id=user_id, amount=split_amount)
            )
    elif split_type == 'percentage':
        if not splits_data:
            return jsonify({"error": "Percentage splits not provided"}), 400
        total_percentage = sum(splits_data.values())
        if total_percentage != 100:
            return jsonify({"error": "Total percentage must sum to 100"}), 400
        for user_id, perc in splits_data.items():
            amount = total_amount * (perc / 100)
            expense_splits.append(
                ExpenseSplit(expense_id=expense.id, user_id=user_id, amount=amount, percentage=perc)
            )
    else:
        return jsonify({"error": "Invalid split type"}), 400

    for split in expense_splits:
        db.session.add(split)
    db.session.commit()

    return jsonify({
        "id": expense.id,
        "group_id": expense.group_id,
        "paid_by": expense.paid_by,
        "total_amount": expense.total_amount,
        "description": expense.description,
        "split_type": expense.split_type
    }), 201
