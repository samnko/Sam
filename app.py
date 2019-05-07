from flask import session, render_template, request, redirect, url_for,flash
from models import app, db, User, Discussion, Message
from sqlalchemy import desc
from datetime import datetime
from utils import validate_password

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' 

@app.route('/')
def index():
    discussions = Discussion.query.all()
    messages = Message.query.all() 
    user = User.query.all()
    messages_number = len(messages)
    dernier_message = messages[-1]
    return render_template('index.html', discussions=discussions,messages=messages,user=user,messages_number=messages_number,dernier_message=dernier_message)

@app.route('/liste_messages/<int:discussion_id>/',methods=['GET', 'POST'])
def liste_messages(discussion_id):
    if request.method == 'POST':
        text = request.form['text']
        discussion_id = discussion_id
        user = User.query.filter_by(username=session['username']).first()
        new_message = Message(
                    text = text,
                    discussion_id = discussion_id,
                    user_id = user.id)
        db.session.add(new_message)
        db.session.commit()

    discussion = Discussion.query.filter_by(id=discussion_id).first()
    messages = Message.query.filter_by(discussion_id=discussion_id).order_by(Message.date.desc()).all()

    for message in messages:
        message.user = User.query.filter_by(id=message.user_id).first()

    return render_template('liste_message.html',messages=messages,discussion=discussion)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first() == None:
            if validate_password(password):
                user = User(username=username,password=password)
                db.session.add(user)
                db.session.commit()
                session['username'] = username # pour qu'il se connect directe
                return redirect(url_for('index'))
            else:
                flash('Password is too weak!!')
        else:
            flash('Username is already taken')
    return render_template('signup.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if 'chances' not in session:
        session['chances'] = 3 
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        if session['chances'] <= 1:
            flash('Too many login attempts')
        else:
            user = User.query.filter_by(
                username=request.form['username'],
                password=request.form['password']
            ).first()
            if user:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            else:
                session['chances'] -= 1 
                flash('Invalid credentials you have {} chances remaining'.format(session['chances']))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/profile/<int:user_id>/')
def profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    messages = Message.query.filter_by(user_id=user_id).all()
    
    return render_template('profile.html',user=user,messages=messages)


@app.route('/profile/<int:user_id>/new_password',methods=['POST'])
def new_password(user_id):
    
    if 'old_password' in request.form: # verifier si ya la clef old password
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            user = User.query.filter_by(username=session['username'],password=old_password).first()

            if user != None:
                if validate_password(new_password) and new_password != old_password:
                    user.password = new_password
                    flash('You change your password with sucess')
                    db.session.commit()
                else:
                    flash('New password is too weak')
            else:
                user = User.query.filter_by(id=user_id).first()
                flash('Invalid password')

    return redirect(url_for('profile' ,user_id=user.id))
    


@app.route('/profile/<int:user_id>/new_username',methods=['POST'])
def new_username(user_id):

    user = User.query.filter_by(id=user_id).first()
    if 'new_username' in request.form:
        new_username = request.form['new_username']
        search_user = User.query.filter_by(username=new_username).first()
        if search_user == None:
            user.username = new_username
            flash('You change your username with sucess')
            db.session.commit()
            session['username'] = new_username

        else:
            flash('Username already taken')
    
    return redirect(url_for('profile',user_id=user.id))




















