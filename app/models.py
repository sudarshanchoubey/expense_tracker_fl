from app import db, lm
from flask_login import LoginManager, UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64))
    expenses = db.relationship('Expense', backref='spender', lazy='dynamic')

    def __repr__(self):
        return "<User {0}>".format(self.nickname)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

tags_table = db.Table('tag_table',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('expense_id', db.Integer, db.ForeignKey('expense.id'))
)


class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(140), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship('Tag', secondary=tags_table, backref=db.backref('for_expenses', lazy='dynamic'))

    def __repr__(self):
        return "<Expense {0}: {1}>".format(self.description, self.amount)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(64), nullable=False)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id'))

