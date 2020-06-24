import os
from flask import render_template, request,redirect,url_for,abort, flash
from . import main
from ..models import User, PhotoProfile
from .forms import UpdateProfile
from ..import db, photos
from flask_login import login_required, current_user
from ..requests import get_quote


#Views

# home page
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    quote = get_quote()
    
    title = 'Pomodoro Today'
    return render_template('index.html', title=title, quote= quote)

# user profile page
@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)


    title = 'Pomodoro Today: myProfile'
    return render_template("profile/profile.html", user=user, title=title)

# update profile page - update user bio
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))
    
    title = 'Pomodoro Today'
    return render_template('profile/update.html', form=form, user = user, title =title)

# update profile pic
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user_photo = PhotoProfile(pic_path = path,user = user)
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
