from flask import render_template
from flask_login import login_required, current_user
from app.forms import UpdateProfileForm
from app import db
from app.utils import save_picture
from flask import render_template, redirect, url_for, flash, request
from app import db, bcrypt
from app.forms import RegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from app.forms import UpdateProfileForm
from app.utils import save_picture
from app.models import User
from app.main import bp

@bp.route("/")
@bp.route("/home")
def home():
    return render_template('home.html')

@bp.route("/dashboard")
@login_required
def dashboard():
    user_stats = {
        'total_games': current_user.total_games or 0,
        'wins': current_user.number_of_wins or 0,
        'losses': current_user.number_of_losses or 0,
        'draws': current_user.number_of_draws or 0,
        'games_against_ai': current_user.games_against_ai or 0,
        'games_against_real_players': current_user.games_against_real_players or 0
    }
    
    # Calculate win percentage
    win_percentage = 0
    if user_stats['total_games'] > 0:
        win_percentage = round((user_stats['wins'] / user_stats['total_games']) * 100, 1)
    
    return render_template('dashboard.html', 
                           title='Dashboard',
                           user_stats=user_stats,
                           win_percentage=win_percentage)

@bp.route("/rules")
def rules():
    return render_template('rules.html')

@bp.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('profile.html', title='Profile', image_file=image_file, form=form)