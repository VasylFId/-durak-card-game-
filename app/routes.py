from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db, bcrypt
from app.forms import RegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required

bp = Blueprint('main', __name__)

# Home Route
@bp.route("/")
@bp.route("/home")
def home():
    return render_template('home.html')

# Play Route
@bp.route("/play")
@login_required  # Ensure only logged-in users can access the play page
def play():
    return redirect(url_for('main.game'))

# Register Route
@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! Please log in now.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
            print(e)
    return render_template('register.html', title='Register', form=form)

# Login Route
@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.email == form.identifier.data) | (User.username == form.identifier.data)).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page and 'play' in next_page:
                return redirect(url_for('main.dashboard'))
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login unsuccessful. Please check identifier and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# Logout Route
@bp.route("/logout")
@login_required  # Ensure only logged-in users can logout
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@bp.route("/game")
@login_required
def game():
    return render_template('game.html', title='Game')

@bp.route("/play_with_ai")
@login_required
def play_with_ai():
    # Logic to start a game with AI
    return redirect(url_for('main.game'))

@bp.route("/play_with_friend")
@login_required
def play_with_friend():
    # Logic to set up a game with a friend
    return redirect(url_for('main.game'))

@bp.route("/random_match")
@login_required
def random_match():
    # Logic to start a random match with another player
    return redirect(url_for('main.game'))


# Forgot Password Route
@bp.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)  # Make sure this function is implemented and working
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('main.login'))
    return render_template('forgot_password.html', title='Forgot Password', form=form)

# Reset Password Route
@bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    user = User.verify_reset_token(token)  # Ensure this method is implemented in your User model
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('main.forgot_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

# Dashboard Route
@bp.route("/dashboard")
@login_required  # Ensure only logged-in users can access the dashboard
def dashboard():
    return render_template('dashboard.html', title='Dashboard')
