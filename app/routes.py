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
from datetime import datetime, timedelta
import io
import os
import pandas as pd

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        print("POST requeste received")
        # Extract the church_id from the form submission
        church_id = request.form.get('church_id')
        church = Church.query.get_or_404(church_id)

        # Make sure the current user owns this church (based on email)
        if church.email == current_user.email:
            # Update the church details with the form data
            church.church_name = request.form.get('church_name', church.church_name)
            church.contact_person = request.form.get('contact_person', church.contact_person)
            church.phone = request.form.get('phone', church.phone)
            church.address = request.form.get('address', church.address)
            church.num_participants = request.form.get('num_participants', church.num_participants)
# Handle date fields if they exist in the form
            church.arrival_date = request.form.get('arrival_date', church.arrival_date)
            church.departure_date = request.form.get('departure_date', church.departure_date)

            # Commit the changes to the database
            db.session.commit()

            # Flash a success message
            flash("Church details updated successfully.", "success")

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
        user = User.query.filter_by(email=form.email.data).first()
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
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists. Please choose a different one.', 'error')
            return render_template('register.html', title='Register', form=form)
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you created an account!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/trip', methods=['GET', 'POST'])
def trip():
    form = ChurchSignupForm()
    if current_user.is_authenticated:
        form.email.data = current_user.email
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
@app.route('/<string:church_name>', methods=['GET', 'POST'])
def church_detail(church_name):

    formatted_name = church_name.replace('_', ' ').title()
    # Query the database for the specific church by name
    church = Church.query.filter_by(church_name=formatted_name).first_or_404()
    # Generate a list of dates from arrival to departure
    total_days = (church.departure_date - church.arrival_date).days + 1
    days = [church.arrival_date + timedelta(days=i) for i in range(total_days)]
    if request.method == 'POST':
        # Process submitted form data
        form_data = request.form

        # Meal prices (adjust as needed)
        meal_prices = {
            'breakfast': [4, 7, 0],  # Light, Guatemalan, None
            'lunch': [7, 10, 15, 0],  # Guatemalan, Fast Food, Antigua, None
            'dinner': [7, 10, 0]  # Guatemalan, Fast Food, None
        }

        total_cost = 0
        daily_breakdown = []

        for i in range(total_days):
            day_cost = 0

            # Retrieve meal selections and number of participants
            breakfast_cost = int(form_data.get(f'breakfasts_{i}'))
            breakfast_people = int(form_data.get(f'breakfast_people_{i}'))
            day_cost += meal_prices['breakfast'][breakfast_cost] * breakfast_people

            lunch_cost = int(form_data.get(f'lunches_{i}'))
            lunch_people = int(form_data.get(f'lunch_people_{i}'))
            day_cost += meal_prices['lunch'][lunch_cost] * lunch_people

            dinner_cost = int(form_data.get(f'dinners_{i}'))
            dinner_people = int(form_data.get(f'dinner_people_{i}'))
            day_cost += meal_prices['dinner'][dinner_cost] * dinner_people

            daily_breakdown.append({'day': i + 1, 'cost': day_cost})
            total_cost += day_cost

        # Pass results back to the template
        return render_template('trip_budget.html', church=church, days=days,
                               daily_breakdown=daily_breakdown, total_cost=total_cost)

    return render_template('trip_budget.html', church=church, days=days)



@app.route('/tb')
def tb():
    return render_template('tb.html')


@app.route('/pandas')
def display_csv():
    file_path = '/home/lucas/microblog/app/uploads/donationsNov2024.csv'
    df = pd.read_csv(file_path)
    html_table = df.to_html(classes='table table-striped')
    df['amount'] = df['amount'].str.replace('$', '', regex=False)
    df['amount'] = df['amount'].str.replace(',', '', regex=False)  # Remove ',' if any
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')  # Convert to numeric
    average_donation = df['amount'].mean()
    print(f"Average Donation: ${average_donation:.2f}")
    return render_template('display_csv.html', table=html_table, average=average_donation)


@app.route('/finance')
def finance():
    df = pd.read_csv('/home/lucas/microblog/app/uploads/expenses/chase2024.csv')
    df_expenses = df[df['Amount'] < 0]
    total_spent = df_expenses['Amount'].sum()
    total_spent = round(total_spent, 2)
    highest_negative = df_expenses['Amount'].min()  # min() returns the largest negative number

#    print(f'Total Spent: ${total_spent:.2f}')
    return render_template('finance.html', total_spent=total_spent, highest_negative=highest_negative)


@app.route('/makequote')
def make_quote():
    form = quoteform()
    return render_template('makequote.html')

@app.route('/quote')
def quote():
    pass
    return render_template('quote.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')
