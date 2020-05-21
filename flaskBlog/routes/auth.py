import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from functools import wraps
from werkzeug.utils import secure_filename
from flaskBlog.forms import RegisterForm, LoginForm, UpdateForm
from flaskBlog import app, bcrypt, db
from flaskBlog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


def redirect_user_authenticated(views):
    @wraps(views)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        else:
            return views(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['POST', 'GET'])
@redirect_user_authenticated
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            flash(f'Welcome {user.username}', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Failed, Please check username and password', 'danger')
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['POST','GET'])
@redirect_user_authenticated
def register():
    form = RegisterForm()
    if form.validate_on_submit(): #Si les donnees sont valides...
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=password)
        #On ajoute l'utilisateur
        db.session.add(user)
        db.session.commit() #save the user
        flash(f'Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_image):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_image.filename)
    random_fn = random_hex + f_ext
    path = os.path.join(app.root_path, 'static/img', random_fn)
    output_size = (300,300)
    #resize image
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(path)

    return random_fn

@app.route('/<username>', methods=['POST','GET'])
@login_required
def account(username):
    form = UpdateForm()
    if form.validate_on_submit():
        if form.image.data:
            image_file = save_picture(form.image.data)
            current_user.image_file = image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    posts = Post.query.filter_by(author=current_user)
    image_file = url_for('static', filename=f'img/{current_user.image_file}') 
    return render_template('auth/account.html', image_file=image_file, form=form, posts=posts)