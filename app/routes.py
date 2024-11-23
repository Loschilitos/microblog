# app/routes.py
#from werkzeug.urls import url_parse
from urllib.parse import urlparse  # Use urlparse from the standard library instead
from flask import send_from_directory
from PIL import Image
from flask_login import current_user
from werkzeug.utils import secure_filename
from flask import send_file, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app import app, db  # Import the app instance
from app.forms import LoginForm
from app.models import User
from flask_login import login_user, logout_user
from app.forms import RegistrationForm, EditProfileForm
from app.forms import ChurchSignupForm
from app.models import Church
import io
import os


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    churches = Church.query.order_by(Church.arrival_date.asc()).all()
    return render_template('dashboard.html', churches=churches)

# Function to check allowed extensions
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
    	if 'file' not in request.files:
        	return render_template('upload.html', error='No file part')  # Render the form with error message

    	file = request.files['file']

    	if file.filename == '':
        	return render_template('upload.html', error='No selected file')  # Return form with error message

    	if file and allowed_file(file.filename):
        	filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        	file.save(filename)
        	return render_template('upload.html', success='File successfully uploaded')  # Render the form with success message
    	else:
        	return render_template('upload.html', error='Invalid file type')  # Return form with error message

	# If GET request, just render the upload form
    return render_template('upload.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '' or next_page == url_for('login'):
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author':user, 'body': 'Test post #1'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template('register.html', title='Register', form=form)
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you created an account!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/trip', methods=['GET', 'POST'])
def trip():
    form = ChurchSignupForm()
    if form.validate_on_submit():
        # Create a new Church instance using form data
        new_church = Church(
            church_name=form.church_name.data,
            contact_person=form.contact_person.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            num_participants=form.num_participants.data,
            arrival_date=form.arrival_date.data,
            departure_date=form.departure_date.data
        )
        # Add to the database
        db.session.add(new_church)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('thank_you'))
    return render_template('trip.html', form=form)


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html', title='Thank you')


@app.route('/flash')
#cant name function flash, it overrides built-in flash function
def flash_message():
    # Flash a simple message
    flash("This is a flash message!")  # You can change "success" to "info", "warning", "error" for different categories
    return redirect(url_for('index'))



@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile', title='Edit Profile',
                           form=form)
