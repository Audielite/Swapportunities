
from flask import render_template, url_for, flash, redirect, request, Blueprint
from movie_app import db, bcrypt
from movie_app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, PassowrdReset, ResetForm
from movie_app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from movie_app.users.utils import save_pic, send_email

users = Blueprint('users', __name__)
#registration page
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user. is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

#Login page
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user. is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.layout'))
        else:
            flash('Login failed', 'danger')
    return render_template('login.html', title='Login', form=form)

#user logout function
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.layout'))

#account page
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_pic(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('acc.html', title='Account', image_file=image_file, form=form)

#user's personal posts
@users.route("/user/<string:username>")
def users_stuff(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('user_stuff.html', posts=posts, user=user)

#password request page
@users.route("/password_reset", methods=['GET', 'POST'])
def request_reset():
    if current_user. is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash('Reset email has been sent', 'info')
        return redirect(url_for('users.login'))
    return render_template('request_reset.html', title='Password Reset', form=form)

#password reset page
@users.route("/password_reset/<token>", methods=['GET', 'POST'])
def token_request(token):
    if current_user. is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_token(token)
    if user is None:
        flash('Token has expired', 'warning')
        return redirect(url_for('main.equest_reset'))
    form = PassowrdReset()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password was reset successfully', 'success')
        return redirect(url_for('users.login'))
    return render_template('token_request.html', title='Password Reset', form=form )
