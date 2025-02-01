# models.py
from datetime import datetime
from database import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    members = db.relationship('GroupMember', backref='group', lazy=True)

class GroupMember(db.Model):
    __tablename__ = 'group_members'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='group_members')

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    paid_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=True)
    split_type = db.Column(db.String, nullable=False)  # Expected values: "equal" or "percentage"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    splits = db.relationship('ExpenseSplit', backref='expense', lazy=True)

class ExpenseSplit(db.Model):
    __tablename__ = 'expense_splits'
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    percentage = db.Column(db.Float, nullable=True)
