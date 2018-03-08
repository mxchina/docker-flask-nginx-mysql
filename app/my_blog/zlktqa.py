#coding=utf-8
from flask import Flask,render_template,request,redirect,url_for,session,g,jsonify
from exts import db
import config,os
from models import User,Question,Answer,Upload_image
from dacorator import login_limit,get_md5
from sqlalchemy import or_
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
@app.route('/<int:page_id>')
def index(page_id = 1):
    questions = g.questions.paginate(page_id,config.QUESTIONS_PER_PAGE,False)
    context = {
        'questions' : questions,
        'pages_number_list' : range(1,(questions.pages+1))
    }
    return render_template('index.html',**context)


@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username_login')
        password = request.form.get('password_login')
        #验证用户名密码是否正确
        user = User.query.filter(User.username == username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            #可以设置3天不用登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u"用户名或者密码错误，请核对后登录"


@app.route('/logout/')
def logout():
    session.pop('user_id')
    return redirect(url_for('index'))

@app.route("/question/",methods=['GET','POST'])
@login_limit
def question():
    if request.method == "GET":
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title = title, content = content)
        question.author_id = g.user.id
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/regist',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        nickname = request.form.get('nickname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #核对手机号码是否已被注册
        user_from_phone = User.query.filter(User.telephone == telephone).first()
        user_from_user = User.query.filter(User.username == username).first()
        if user_from_phone:
            return u"该号码已注册！"
        elif user_from_user:
            return u"该用户名已被注册！"
        elif password1 != password2:
            return u"两次密码不一致，请核对后再注册！"
        else:
            user = User(username = username, telephone = telephone, password = password1, nickname = nickname)
            db.session.add(user)
            db.session.commit()
            #如果注册成功，转到登录页面
            return redirect(url_for('login'))


# @app.route('/detail/<question_id>/')
# def detail(question_id):
#     question_detail = Question.query.filter(Question.id == question_id).first()
#     if request.method == 'GET':
#         return render_template('detail.html',question_detail = question_detail,number = len(question_detail.answer))


@app.route('/detail1/<question_id>/')
@app.route('/detail1/<question_id>/<int:page_id>/')
def detail1(question_id,page_id = 1):
    question_detail = Question.query.filter(Question.id == question_id).first()
    paginations_answer = Answer.query.filter(Answer.question_id ==question_id).order_by('answer_time').paginate(page_id,config.ANSWER_PER_PAGE,False)
    if request.method == 'GET':
        list_a = question_detail.answer
        length_answer = (len(question_detail.answer)+1)
        list_b = range(1,length_answer)
        dict_paginations = dict(zip(list_a,list_b))
        context = {
            'question_detail' : question_detail,
            'pages_number_list' : range(1,(paginations_answer.pages+1)),
            'floor': len(question_detail.answer),
            'paginations_answer' : paginations_answer,
            'dict_paginations' : dict_paginations
        }
        return render_template('detail1.html',**context)


@app.route('/homepage/')
# @app.route('/homepage/<int:page_id>')
@login_limit
def homepage():
    # questions = g.questions.paginate(page_id,config.HOMEPAGE_DETAIL_PER_PAGE,False)
    # questions = g.user.questions.order_by(Question.id.desc())
    questions = Question.query.filter(Question.author_id == session.get('user_id')).order_by(Question.id.desc())

    context = {
        'questions' : questions,
        'user_nikename' : g.user.nickname
        # 'pages_number_list' : range(1,(questions.pages+1))
    }
    return render_template('homepage.html',**context)


@app.route('/delete_question/<question_id>')
@login_limit
def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).first()
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('homepage'))


@app.route('/edit_question/<edit_question_id>/',methods=['GET','POST'])
@login_limit
def edit_question(edit_question_id):
    question = Question.query.filter(Question.id == edit_question_id).first()
    if request.method == "GET":
        return render_template('edit.html',question=question)
    else:
        db.session.delete(question)
        db.session.commit()
        title = request.values.get('title')
        content = request.values.get('content')
        question = Question(id = edit_question_id, title = title, content = content, author_id = g.user.id, create_time = question.create_time)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('homepage'))


@app.route('/search/',methods=['GET'])
def search():
    keyword = request.values.get('q')
    questions = Question.query.filter(or_(Question.title.contains(keyword),Question.content.contains(keyword))).order_by(Question.id.desc())
    if questions.first():
        context = {
        'questions': questions,
        }
        return render_template('index_search.html', **context)
    else:
        return "什么都没找到!"


@app.route('/question/myupload/',methods=['POST'])
@app.route('/edit_question/<edit_question_id>/myupload/',methods=['POST'])
@login_limit
def myupload(edit_question_id=1):
    file = request.files["thumbnail"]
    filename = secure_filename(file.filename)
    base_path = os.path.abspath(os.path.dirname(__file__))
    upload_path = os.path.join(base_path, 'static/uploads/')
    dir_user = str(g.user.id)+'/'
    upload_path = os.path.join(upload_path,dir_user)
    if not os.path.exists(upload_path):
        os.mkdir(upload_path)
    if not g.last_upload_image:
        num = 0
    else:
        num = g.last_upload_image.id+1
    file_name = upload_path +"0"+str(num)+file.filename
    file.save(file_name)

    image_md5 = get_md5(file_name)
    upload_image = Upload_image.query.filter(Upload_image.image_md5 == image_md5).first()
    if upload_image:
        os.remove(file_name)
        return upload_image.addr
    else:
        image_addr = "http://"+config.SERVICE_NAME_+"/static/uploads/"+dir_user+"0"+str(num)+file.filename
        upload_image = Upload_image(addr = image_addr, author_id = g.user.id, image_tag = 'article',image_md5 = image_md5)
        db.session.add(upload_image)
        db.session.commit()

    return image_addr


@app.context_processor
def base_nav():
    session_user_id = session.get('user_id')
    if session_user_id:
        user = User.query.filter(User.id == session_user_id).first()
        if user:
            return {'nav_user':user}
    else:
        return {}

@app.before_request
def my_before_request():
    g.last_upload_image= Upload_image.query.order_by(Upload_image.id.desc()).first()
    g.questions = Question.query.order_by(Question.create_time.desc())
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


@app.route('/answer/',methods=['POST'])
@login_limit
def answer():
    content = request.form.get('detail_answer')
    question_id = request.form.get('question_id')
    answer_model = Answer(content = content, question_id = question_id, author_id = g.user.id)
    db.session.add(answer_model)
    db.session.commit()

    return redirect(url_for('detail1',question_id = question_id))


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)

