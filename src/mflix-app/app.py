# app.py

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy user data for login
users = {
    'user': 'user',
    'admin': 'admin'
}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            return render_template('home.html')
        else:
            return redirect(url_for('login'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
