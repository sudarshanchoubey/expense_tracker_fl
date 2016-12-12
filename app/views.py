from app import app
from flask import render_template
from .forms import ExpenseForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/expense', methods=['GET', 'POST'])
def add_update_expense():
    form = ExpenseForm()
    return render_template('expense.html', form=form)
