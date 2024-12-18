from flask import Flask,redirect,url_for,render_template, request, flash 
# from flask_sqlalchemy import SQLAlchemy
# import pymysql

# # Initialize Flask app, SQLAlchemy
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'mysecrethifi'  # Used for session security
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

@app.route('/') 
def start():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

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
        if password == confirm_password:
            return redirect(url_for('register'))
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
        print(name,email,message,sep='\n')
    return redirect(url_for('start'))
    
    


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()  #create tables if they don't exists
    app.run(debug=True)