# from flask import Flask,redirect,url_for,render_template, request, flash 
import re
import random
import time
from flask import Flask, request, jsonify, render_template, session, flash, redirect, url_for
from flask_mail import Mail, Message
# from flask_sqlalchemy import SQLAlchemy
# import pymysql
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecrethifi'  # Used for session security
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hello_world67@localhost/hifidb'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize the database
# db = SQLAlchemy(app)


# # Define the User model(defined user table with columns)
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), nullable=False, unique=True)
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     location = db.Column(db.String(100), nullable=False)
#     contact = db.Column(db.String(15), nullable=False)
#     password = db.Column(db.String(200), nullable=False)
    
#     def __repr__(self):
#         return f"User('{self.username}','{self.email}')"

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'hifidelivery213@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'oiya zlhv irvc yowz'  # Replace with your app-specific password

mail = Mail(app)
# Store OTPs in memory (can be changed to a database in production)
otp_store = {}

# Send OTP to the email
def send_otp(email, otp):
    try:
        msg = Message('Your OTP Code', sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = f"Your OTP code is {otp}. It will expire in 10 minutes."
        mail.send(msg)
        print(f"OTP sent to {email}")
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return False
    return True

@app.route('/') 
def start():
    return render_template('homepage.html')

@app.route('/send_otp', methods=['POST'])
def send_otp_route():
    data = request.get_json()
    email = data.get('email')

    if not email or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return jsonify({'success': False, 'message': 'Invalid email format.'})

    otp = str(random.randint(100000, 999999))
    otp_store[email] = {'otp': otp, 'timestamp': time.time()}  # Store OTP with timestamp

    if send_otp(email, otp):
        return jsonify({'success': True, 'message': 'OTP sent to email.'})
    else:
        return jsonify({'success': False, 'message': 'Error sending OTP.'})


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        otp_input = request.form['otp']

        # Verify OTP
        stored_otp = otp_store.get(email, {}).get('otp')
        timestamp = otp_store.get(email, {}).get('timestamp', 0)

        if not stored_otp:
            flash('OTP not generated or expired. Please request a new OTP.', 'danger')
            return redirect(url_for('register'))

        # Check if OTP is valid and not expired (expires after 10 minutes)
        if otp_input == stored_otp:
            elapsed_time = time.time() - timestamp
            if elapsed_time > 600:
                flash('OTP has expired. Please request a new one.', 'danger')
                del otp_store[email]
                return redirect(url_for('register'))
            
            flash('OTP verified successfully! You are now registered.', 'success')
            del otp_store[email]  # Clear OTP after successful registration
            return redirect(url_for('index'))  # Redirect to the home page after successful registration
        else:
            flash('Invalid OTP. Please try again.', 'danger')
            return redirect(url_for('register'))  # Redirect back to registration page if OTP is incorrect

    return render_template('register.html')  # Ensure register.html is your registration page

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/recovery')
def recovery():
    return render_template('recovery.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/verify_data', methods=['GET', 'POST'])
def verify_data():
    print("Verify data function triggered.")  # Debugging line
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        email = request.form['email']
        location = request.form['location']
        contact = request.form['contact']
        # print(f"Username: {username}, Email: {email}")  # Check if values are correct
        
        # # Check if user already exists
        # existing_user = User.query.filter_by(email=email).first()
        # if existing_user:
        #     flash('Email already registered. Please use a different one.', 'warning')
        #     return redirect(url_for('register'))
        
        # # Check if password and confirm password match
        # if password != confirm_password:
        #     flash('Passwords do not match. Please try again.', 'danger')
        #     return redirect(url_for('register'))
        
        # # Debugging before attempting to add the user
        # print("Attempting to add new user to the database.")

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return redirect(url_for('register'))
        
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            flash("Invalid email format.", "error")
            return redirect(url_for('register'))
        
        if not re.match(r'^\d{10}$', contact):
            flash("Contact number must be a valid 10-digit number.", "error")
            return redirect(url_for('register'))

    
        # # Save new user to the database
        # new_user = User(username=username, email=email, location=location, contact=contact, password=password)
        # try:
        #     db.session.add(new_user)
        #     db.session.commit()
        #     flash('Registration successful! Please log in.', 'success')
        #     return redirect(url_for('login'))
        # except Exception as e:
        #     db.session.rollback()
        #     flash(f'Error: {e}', 'danger')
        #     return redirect(url_for('register'))
         
    return redirect(url_for('start'))

@app.route('/submit_contact',methods=['GET','POST'])
def submit_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            flash("Invalid email format.", "error")
            return redirect(url_for('register'))
        print(name,email,message,sep='\n')
    return redirect(url_for('start'))
    

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        new_password = request.form.get('new_password')
        re_new_password = request.form.get('re_new_password')


        if new_password != re_new_password:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('forgot_password'))


        flash('Password reset successful. Please log in with your new password.', 'success')
        return redirect(url_for('start'))

    return render_template(url_for('forgot'))



if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()  #create tables if they don't exists
    app.run(debug=True)



