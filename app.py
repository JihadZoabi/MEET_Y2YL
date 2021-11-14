from flask import Flask, flash, render_template, request, redirect, Response, url_for, abort
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import base64
from info import get_info
from colorfinder import color_pic
import cv2 as cv
import numpy as np
from functions import readb64, allowed_info, allowed_question, correct_info
from database import add_user, query_all, User, session, add_question, delete_question, get_question, \
    get_user_by_id, get_user_by_name, add_answer
from models import Question

login_manager = LoginManager()

UPLOAD_FOLDER = 'user/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '362eb9306eba402f9b67fee2c616cc9b'



def page_not_found(e):
    return render_template('404.html'), 404


app.register_error_handler(404, page_not_found)


db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).filter_by(user_id=user_id).first()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Global Variables in Jinja2
@app.context_processor
def inject_stage_and_region():
    return dict(current_user=current_user)


@app.route('/colors', methods=['GET', 'POST'])
def colors():
    if request.method == 'GET':
        return render_template('colors.html')
    link = request.form['imgLink']
    processed_img = readb64(link)
    color, hx = color_pic(processed_img)
    img_url = "https://www.colorhexa.com/" + hx + ".png"
    c_info = get_info(hx)
    return render_template("results.html", color=color, c_info=c_info, img_url=img_url)


@app.route("/")
def index():
    return render_template("main.html")


@app.route("/forum")
@login_required
def forum():
    return render_template("forum.html", questions=query_all(Question))


@app.route("/submit", methods=["GET", "POST"])
@login_required
def submit():
    if request.method == 'POST':
        title = request.form['title']
        details = request.form['details']
        file = request.files['file']
        message = allowed_question(title, details)
        if message is not True:
            return render_template("submit.html", message=message)
        message = allowed_file(file.filename)
        if message is not True:
            print(message)
            return render_template("submit.html", message="Only image files are allowed")
        img = cv.imdecode(np.fromstring(file.read(), np.uint8), cv.IMREAD_UNCHANGED)
        img64base = base64.b64encode(cv.imencode('.jpg', img)[1]).decode()
        add_question(title, details, current_user, img64base)
        return redirect(url_for('forum'))
    return render_template("submit.html", message=None)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('forum'))

    if request.method == "POST":
        username = request.form['username']
        password = request.form['psw']

        message = correct_info(username, password)
        if message is not True:
            return render_template("login.html", message=message)

        login_user(get_user_by_name(username))
        return redirect(url_for('forum'))
    return render_template("login.html", message=None)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('forum'))
    message = None
    if request.method == "POST":
        username = request.form['username']
        password = request.form['psw']
        repeat = request.form['repeat-psw']
        vol = request.form.getlist('volunteer')
        message = allowed_info(username, password, repeat)
        if message is True:
            if not vol:
                vol = False
            else:
                vol = True
            # vol is either ['on'] or [], not vol checks for empty list
            add_user(username, password, vol)
            return redirect(url_for("login"))
    return render_template("register.html", message=message)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/ask/<question_id>", methods=["POST", "GET"])
@login_required
def ask(question_id):
    question = get_question(question_id)
    if question is None:
        return "<h1>No Question Found</h1>"
    if request.method == "POST":
        answer_text = request.form['answer']
        for ans in question.question_answers:
            if current_user.user_id == ans.answerer_id:
                return "<h1>Already Answered</h1>"
        add_answer(answer_text, current_user, get_question(question_id))
    return render_template("ask.html", question=question,
                           get_user=get_user_by_id,
                           current_user=current_user
                           )


@app.route("/delete/<question_id>")
@login_required
def delete(question_id):
    question = get_question(question_id)
    if question is None:
        return redirect(url_for('forum'))
    if current_user == get_user_by_id(question.asker_id):
        delete_question(question_id)
    return redirect(url_for('forum'))


@app.route('/profile/<name>')
@login_required
def profile(name):
    user = get_user_by_name(name)
    if user is None:
        abort(404)
    return render_template("profile.html", user=user)


@app.route("/follow/<name>")
@login_required
def follow(name):
    user = get_user_by_name(name)
    if user is None or user == current_user:
        return redirect(url_for('index'))
    if user not in current_user.followers:
        current_user.followers.append(user)
    return redirect(url_for('forum'))


if __name__ == '__main__':
    app.run(debug=True)

# azore
