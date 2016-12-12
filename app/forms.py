from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField
from wtforms.validators import DataRequired


class ExpenseForm(FlaskForm):
    description = StringField('desciption', validators=[DataRequired()])
    amount = FloatField('amount', validators=[DataRequired()])
    date_of_purchase = DateField('date_of_purchase', validators=[DataRequired()])
    expense_tags = StringField('expense_tags')
