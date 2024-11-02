from flask import Blueprint, render_template, flash, redirect, url_for
from accounts.forms import RegistrationForm, LoginForm
from config import User, db
from flask import session


accounts_bp = Blueprint('accounts', __name__, template_folder='templates')

@accounts_bp.route('/registration', methods=['GET','POST'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        #if not form.recaptcha.validate_on_submit():
            #flash('Please complete the reCAPTCHA.', category='danger')
            #return render_template('accounts/login.html', form=form)

        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists', category="danger")
            return render_template('accounts/registration.html', form=form)

        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        phone=form.phone.data,
                        password=form.password.data,
                        )

        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash('Account Created', category='success')
        return redirect(url_for('accounts.login'))

    return render_template('accounts/registration.html', form=form)


@accounts_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # Initialize login attempts in the session if it's not already set
    if 'login_attempts' not in session:
        session['login_attempts'] = 0

    if form.validate_on_submit():
        # Retrieve user by email
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            # Check if the account is locked due to too many failed login attempts
            if session['login_attempts'] >= 3:
                flash("Your account is locked due to too many failed login attempts. Please unlock to try again.",
                      category='danger')
                return render_template('accounts/login.html', form=None, email=user.email)

            # Check if the password matches
            if user.check_password(form.password.data):
                session['login_attempts'] = 0  # Reset login attempts on successful login
                flash('Login successful', category='success')
                return redirect(url_for('posts.posts'))
            else:
                # Increment the login attempts if the password is incorrect
                session['login_attempts'] += 1
                if session['login_attempts'] >= 3:
                    flash('Your account is locked due to too many failed login attempts.', category='danger')
                    return render_template('accounts/login.html', form=None, email=user.email)
                else:
                    attempts_left = 3 - session['login_attempts']
                    flash(f'Login failed. {attempts_left} attempts remaining.', category='danger')
        else:
            flash('Login failed. Check your email and password.', category='danger')

    return render_template('accounts/login.html', form=form)


@accounts_bp.route('/unlock', methods=['GET'])
def unlock_account():
    # Unlock account by resetting session-based login attempts
    session['login_attempts'] = 0
    flash("Your account has been unlocked. You can try logging in again.", category='success')

    return redirect(url_for('accounts.login'))

@accounts_bp.route('/account')
def account():
    return render_template('accounts/account.html')