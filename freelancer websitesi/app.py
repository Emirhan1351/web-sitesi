from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        
        new_user = User(username=username, email=email, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error during registration: {e}', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')
# E-ticaret Sayfası
@app.route('/eticaret')
def eticaret():
    return render_template('eticaret.html')

# Yazılım Sayfası
@app.route('/yazilim')
def yazilim():
    return render_template('yazılım.html')

# İlan Verme Sayfası
@app.route('/ilan_verme')
def ilan_verme():
    return render_template('ilan_verme.html')

# Sosyal Medya Sayfası
@app.route('/sosyal_medya')
def sosyal_medya():
    return render_template('sosyal_medya.html')

# Logo Tasarımı Sayfası
@app.route('/logo_tasarimi')
def logo_tasarimi():
    return render_template('logo_tasarımı.html')

# Video Sayfası
@app.route('/video')
def video():
    return render_template('video.html')

# Website Hizmetleri Sayfası
@app.route('/website')
def website():
    return render_template('website.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('users.db'):
            db.create_all()
    app.run(debug=True)
