from app import app, db, lm
from flask import render_template, redirect, url_for, g, flash
from .forms import ExpenseForm
from .oauth import OAuthSignIn
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from .models import User, Tag, Expense
import datetime

lm.login_view = 'login'

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('user', nickname=g.user.nickname))
    return render_template('login.html')

@app.route('/expense', methods=['GET', 'POST'])
@login_required
def add_update_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        print("Form is valid")
        if form.timestamp.data == None:
            ts = datetime.datetime.now()
            print("Date time was not specified")
        else:
            ts = datetime.datetime(form.timestamp.data)
        expense = Expense(spender=g.user, description=form.description.data, amount=form.amount.data, timestamp=ts)
        if form.expense_tags.data != None:
            tags_arr = form.expense_tags.data.rsplit()
            for a_tag in tags_arr:
                t = Tag.query.filter_by(body=a_tag).first()
                if t == None:
                    t = Tag(body=a_tag)
                print("Tag: {0}".format(t.body))
                expense.tags.append(t)
                db.session.add(t)
        db.session.add(expense)
        db.session.commit()
        flash('Your expense has been saved.')
        return redirect(url_for('user', nickname=g.user.nickname))
    print("form was invalid")
    for err in form.errors:
        print(err)
    return render_template('expense.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('login'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user_nick = User.query.filter_by(nickname=username).first()
        if user_nick != None:
            flash('user with same nickname already exists, try a different provider')
            return redirect(url_for('login'))
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('login'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash("User {1} not found.".format(nickname))
        return redirect(url_for('login'))
    return render_template('user.html', user=user, expenses=user.expenses.all())
