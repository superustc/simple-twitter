from flask import render_template, url_for, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, jsonify

from simple_twitter import app, db, login_manager
from simple_twitter.models import User, Chat, followers

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    followed_chats_query = Chat.query.join(
        followers, (followers.c.followed_id == Chat.user_id)
    ).filter(
        followers.c.follower_id == current_user.id
    ).join(User, User.id == Chat.user_id).add_columns(
        User.username, Chat.content, Chat.timestamp
    ).order_by(
        Chat.timestamp.desc()
    ).all()

    followed_chats = [
        {'username': chat.username, 'content': chat.content, 'timestamp': chat.timestamp}
        for chat in followed_chats_query
    ]

    all_users = User.query.all()
    return render_template('index.html', chats=followed_chats, all_users=all_users)

@app.route('/get_chats')
@login_required
def get_chats():
    followed_chats_query = Chat.query.join(
        followers, (followers.c.followed_id == Chat.user_id)
    ).filter(
        followers.c.follower_id == current_user.id
    ).join(User, User.id == Chat.user_id).add_columns(
        User.username, Chat.content, Chat.timestamp
    ).order_by(
        Chat.timestamp.desc()
    ).all()

    chats = [
        {'username': chat.username, 'content': chat.content, 'timestamp': chat.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
        for chat in followed_chats_query
    ]
    return jsonify(chats)

# Add routes for register, login, logout, and post chat here
# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Post chat route
@app.route('/post_chat', methods=['POST'])
@login_required
def post_chat():
    content = request.form.get('content')
    new_chat = Chat(content=content, user_id=current_user.id)
    db.session.add(new_chat)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    # if user == current_user:
    #     flash('You cannot follow yourself!')
    #     return redirect(url_for('index'))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following {}!'.format(username))
    return redirect(url_for('index'))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    # if user == current_user:
    #     flash('You cannot unfollow yourself!')
    #     return redirect(url_for('index'))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are no longer following {}.'.format(username))
    return redirect(url_for('index'))