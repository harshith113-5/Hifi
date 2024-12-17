from flask import Flask,redirect,url_for,render_template,request

app = Flask(__name__)

@app.route('/') 
def start():
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/verify_data', methods=['GET', 'POST'])
def verify_data():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        email = request.form['email']
        location = request.form['location']
        contact = request.form['contact']
        if password == confirm_password:
            return redirect(url_for('login'))
    
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)