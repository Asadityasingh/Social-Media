from flask import Flask, request,redirect,Response
from flask import render_template,url_for,flash,request, redirect
from flask import current_app as app

from werkzeug.utils import secure_filename
from flask import send_from_directory

from sqlalchemy import select,create_engine
from auth.form import RegisterForm,LoginForm,Resetpass,Edit_Profile,Search

from flask_login import login_user,LoginManager,login_required,logout_user,current_user
from flask_bcrypt import Bcrypt

from application import config
from application.config import LocalDevelopmentConfig

import os

from application.models import *

import datetime;


bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=["GET", "POST"])
def index():
    # users=User.query.filter_by(id=2)
    user_=User.query.all()
    #print(user_)
    return render_template('index.html',users=user_)

# logedinuser='none'
@app.route('/login', methods=["GET", "POST"])
def login():
    # invalid = 'None'
    
    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(user_name=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user)
                # logedinuser=user.user_name

                return redirect(url_for('dashboard',uname=user.user_name ,dp=user.dp))
            else:
                return render_template('login.html',invalid="icorrect password or username",form=form)
        else:
                return render_template('login.html',invalid="icorrect password or username",form=form)
    return render_template('login.html',form=form)

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user
    return redirect(url_for('index'))




@app.route('/passreset',methods=["GET", "POST"])
def passreset():
    form = Resetpass()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.username.data).first()
        if user:
            
            hashed_password=bcrypt.generate_password_hash(form.newpassword.data)
            user.user_name=form.username.data
            user.keys=form.keys.data
            user.password=hashed_password
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('passrest.html',form=form)

@app.route('/edit_profile/<uname>',methods=["GET", "POST"])
@login_required
def edit_profile(uname):
    form = Edit_Profile()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=uname).first()
        if user:
            if int(form.age.data)<18:
                return render_template('edit_profile.html',invalid="Your are not elegible to create account",form=form)
            else:
                user.keys=form.keys.data
                user.name=form.name.data
                user.age=form.age.data
                user.address=form.address.data
                user.about=form.about.data
                user.email=form.email.data
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('dashboard',uname=uname))
    return render_template('edit_profile.html',form=form)


@app.route('/ep/<uname>/<id>',methods=["GET", "POST"])
@login_required
def ep(uname,id):
    print('from ep : ----------------------------')
    return render_template('edit_post.html',uname=uname,id=id)



@app.route('/edit_/<uname>/<id>',methods=["GET", "POST"])
@login_required
def edit_(uname,id):
    
    ct = datetime.datetime.now() #get current time
    pic=request.files['file1']
    cap=request.form['txt1']
    tit=request.form['txt2']
    filename = secure_filename(pic.filename)
    al=f'/home/aditya/Documents/programming/APPdev/social_media/static/'+filename
    pic.save(al)
    post_ = Img.query.filter_by(img_Id=int(id)).first()
    old_img_name=post_.img_name
    
    if post_:
        mimetype = pic.mimetype
        post_.user_name=uname
        post_.mimetype=mimetype
        post_.title=tit
        post_.caption=cap
        post_.img_name=filename
        post_.ct=ct
        db.session.add(post_)
        db.session.commit()
        name=uname

        os.remove(os.path.join('static',old_img_name)) #removing image from static folder

        return redirect(url_for('dashboard',uname=name))
    return redirect(url_for('edit_post'))
        


@app.route('/dashboard/<uname>', methods=["GET", "POST"])
@login_required #if user is not logeg in dont go to dashboard
def dashboard(uname):
    post =Img.query.filter_by(user_name=uname).all()
    user_=User.query.all()
    f=Follower.query.filter_by(user_name=uname).all()
    f1=Following.query.filter_by(user_name=uname).all()
    user_detail=User.query.filter_by(user_name=uname).all()

    return render_template('dashboard.html',uname=uname,i_img=post,uzer=user_,no_follower=len(f),no_following=len(f1),f1=f1,f=f,user_detail=user_detail)





@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

   
    if form.validate_on_submit():#chacking if this user name is avl
        user = User.query.filter_by(user_name=form.username.data).first()
        if user:
            return render_template('register.html',invalid="please select another username",form=form)

        elif int(form.age.data)<18:
            return render_template('register.html',invalid="Your are not elegible to create account",form=form)
        else:
            hashed_password=bcrypt.generate_password_hash(form.password.data)
            new_user = User(user_name=form.username.data,password=hashed_password,keys=form.keys.data,name=form.name.data,age=form.age.data,address=form.address.data,about=form.about.data, email=form.email.data)
            db.session.add(new_user)
            db.session.commit()

            

        return redirect(url_for('login'))
    return render_template('register.html',form=form)



@app.route("/upload/<uname>" , methods=['POST'])
@login_required
def upload(uname):
    ct = datetime.datetime.now() #get current time
    pic=request.files['file1']
    cap=request.form['txt1']
    tit=request.form['txt2']
    
    if not pic:
        return 'No pic uploaded',400
    
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype


    al=f'/home/aditya/Documents/programming/APPdev/social_media/static/'+filename
    
    pic.save(al)
    img=Img(mimetype=mimetype,img_name=filename,user_name=uname,caption=cap,ct=ct,title=tit)
    db.session.add(img)
    db.session.commit()
    name=uname
    return redirect(url_for('dashboard',uname=name))

@app.route('/del_user/<uname>', methods=["GET", "POST"])
@login_required #if user is not logeg in dont go to dashboard
def del_user(uname):
    print(uname)

    f=Follower.query.filter(Follower.followers==uname).first()
    if f:
        db.session.delete(f)
    f_=Follower.query.filter(Follower.user_name==uname).first()
    if f_:
        db.session.delete(f_)
    f1_=Following.query.filter(Following.following==uname).first()
    if f1_:
        db.session.delete(f1_)
    f1=Following.query.filter(Following.user_name==uname).first()
    if f1:
        db.session.delete(f1)
    i=Img.query.filter(Img.user_name==uname).first()
    if i:
        db.session.delete(i)
    z=User.query.filter(User.user_name==uname).first()

    db.session.delete(z)
    
    
    db.session.commit()
    return redirect(url_for('logout'))

@app.route('/del_post/<id>/<uname>', methods=["GET", "POST"])
@login_required #if user is not logeg in dont go to dashboard
def del_post(id,uname):
   
    z=Img.query.filter(Img.img_Id==id).first()
    img_name=z.img_name
    os.remove(os.path.join('static',img_name)) #removing image from static folder
    db.session.delete(z)    #removing image from DB
    db.session.commit()
    name=uname
    return redirect(url_for('dashboard',uname=name))


# follow
@app.route('/follow/<uname>/<funame>', methods=["GET", "POST"])
@login_required #if user is not logeg in dont go to dashboard
def follow(uname,funame):

    already =Following.query.filter_by(user_name=uname,following=funame).all()
    if already:
        return redirect(url_for('dashboard',uname=uname))
    else:
        a=Following(user_name=uname,following=funame)
        b=Follower(user_name=funame,followers=uname)
        db.session.add(a)
        db.session.add(b)
        db.session.commit()
    
    
    return redirect(url_for('dashboard',uname=uname))

# unfollow
@app.route('/unfollow/<uname>/<funame>', methods=["GET", "POST"])
@login_required #if user is not logeg in dont go to dashboard
def unfollow(uname,funame):
    try:
        a=Following.query.filter_by(user_name=uname,following=funame).first()
        b=Follower.query.filter_by(user_name=funame,followers=uname).first()
        db.session.delete(a)
        db.session.delete(b)
        db.session.commit()
        return redirect(url_for('dashboard',uname=uname))
    except:
        return 'Your are not following him'
    


@app.route('/su/<uname>',methods=["GET", "POST"])
@login_required
def su(uname):
    print('from su : ----------------------------')

    return render_template('search.html',uname=uname)



@app.route('/search/<uname>', methods=["GET", "POST"])
@login_required #if user is not logeg in dont go to dashboard
def search(uname):
    # form = Search()
    # tit=request.form['txt2']
    # s =User.query.filter_by(user_name=tit).first()
    # print(s.user_name)

    # q= request.args.get('q')
    user_=User.query.first()
    q= request.form['txt2']
    query = "%"+q+"%"
    result =User.query.filter(User.user_name.like(query)).all()
    return render_template('search.html',sw=result,q=q,uname=uname,user=user_)


@app.route('/profile/<uname>', methods=["GET", "POST"])
@login_required #if user is not logeg in dont go to dashboard
def profile(uname):    

    post =Img.query.filter_by(user_name=uname).all()
   
    f=Follower.query.filter_by(user_name=uname).all()
    f1=Following.query.filter_by(user_name=uname).all()


    return render_template('profile.html',uname=uname,i_img=post,no_follower=len(f),no_following=len(f1))

@app.route('/feed/<uname>', methods=["GET", "POST"])
@login_required #if user is not logeg in dont go to dashboard
def feed(uname):  
    
    f1=Following.query.filter_by(user_name=uname).all()
    post =Img.query.all()
    l=[]
    
    for i in f1:
        for j in post:
            if  j.user_name in i.following :
                # post =Img.query.filter_by(user_name=j.user_name).all()
                l.append(j)
                
    print(l)
    return render_template('feed.html',f1=f1,list_=l,uname=uname)