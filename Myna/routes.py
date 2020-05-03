from Myna import Myna
from Myna import db
from flask_login import current_user, login_user,logout_user, login_required
from Myna.models import User
from flask import render_template, redirect, request, flash,url_for
from werkzeug.urls import url_parse
from Myna.forms import LoginToAvatar,CreateAvatar,UpdateAvatar,PostForm
from Myna import photos
from datetime import datetime
from .GreenAnts import forms, models
from forms import PostForm
from models import Ant, Post


@Myna.route('/')
@Myna.route('/Myna/Index')
@login_required
def index():
    return render_template('Myna/MynaIndex.html', title='Myna-Framework for Integrated Water Management',fl_nm="styles/base_style.css")


@Myna.errorhandler(404)
def not_found_error(error):
    return render_template('Myna/Myna500Error.html'), 404

@Myna.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('Myna/Myna500Error.html'), 500

@Myna.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@Myna.route('/Myna/Post', methods=['GET', 'POST'])
@login_required
def Wall():
    form = PostForm()
    posts = []
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user.username)
        post.save()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    return render_template("Myna/MynaPost.html", title='Home Page', form=form,posts=posts)

@Myna.route('/Myna/Login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginToAvatar()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('Myna/MynaLoadSYS.html', title='Myna-Load Avatar',fl_nm="styles/base_style.css",form=form)

@Myna.route('/Myna/Register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = CreateAvatar()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, stakeholder=form.stakeholder.data)
        user.set_password(form.password.data)
        filename = photos.save(form.avatar_img.data)
        file_url = photos.url(filename)
        user.update_avatar_img(file_url)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now have a registered Avatar!')
        return redirect(url_for('login'))
    return render_template('Myna/MynaCreateSYS.html', title='Myna-Create Avatar',fl_nm="styles/base_style.css",form=form)
    

@Myna.route('/Myna/Logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@Myna.route('/User/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    user.avatar_img=user.avatarIMG(150)
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('Myna/MynaStakeholder.html', user=user, posts=posts)

@Myna.route('/ProfileUpdate/<username>', methods=['GET', 'POST'])
@login_required
def ProfileUpdate(username):
    form=UpdateAvatar(current_user.email)
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first_or_404()
        user.email=form.email.data
        user.stakeholder=form.stakeholder.data
        user.set_password(form.password.data)
        filename = photos.save(form.avatar_img.data)
        file_url = photos.url(filename)
        user.update_avatar_img(file_url)        
        db.session.commit()
        flash('Congratulations, your Avatar is Updated!')
        return redirect(url_for('index'))
    return render_template('Myna/MynaUpdateProfile.html', user=current_user,form=form)

@Myna.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@Myna.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))
