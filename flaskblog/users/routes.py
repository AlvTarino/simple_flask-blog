from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flaskblog import db, bcrypt
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestPasswordReset, ResetPasswordForm)
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.utils import save_picture, send_reset_email

# instance of the blueprint, with 'users' as name of the blueprint
users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    # to check if data submitted is valid
    if form.validate_on_submit():
        # we hash whatever password the user enters and we pass it to the hashed_password variable
        # we add decode utf-8 to change the hashed password from byte data to a string
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # creating a new user account
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # add created user to the database
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created. You can now log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        # db query to check if user email exists / registered
        user = User.query.filter_by(email=form.email.data).first()
        # condition to simultaneously check if user and matching hashed password are correct
        # user.password --> registered password in the db
        # form.password.data --> password entered by the user in the login form
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # to get redirected to a required page instead of going to home page first
            next_page = request.args.get('next')
            # ternary conditional
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# to log out the user
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# to display account details of a user after logging in
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # instance of the UpdateAccountForm
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account information has been updated', 'success')
        # MUST be a redirect to avoid data being submitted twice
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        # to populate the form with current user information
        form.username.data = current_user.username
        form.email.data = current_user.email
    # path to user profile picture
    profile_pic = url_for('static', filename='profiles/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=profile_pic, form=form)


# Route to show user specific posts
@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('single_user_posts.html', sample=posts, user=user)


# route to request for a password reset
@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    # if user is already logged in, redirect to the home page
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    # if the user is not logged in, they can access the password request form
    form = RequestPasswordReset()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password easily', 'info')
        return redirect(url_for('users.login'))
    return render_template('request_password_reset.html', title='Reset Password', form=form, legend='Reset Password')


# route to reset their password after validation
@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def password_token(token):
    # to check if user is logged in. if true, redirected to the home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or Expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been changed. You can now log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form, legend='Password Reset')
