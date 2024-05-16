"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretsqlkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def home():
    return redirect("/users")

@app.route("/users")
def list_users():
    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/users/new", methods=["GET"])
def new_user_form():
    return render_template("new_user.html")

@app.route("/users/new", methods=["POST"])
def new_user_info():
    new_user = User(
        first_name=request.form["first_name"],
        last_name=request.form["last_name"],
        image_url=request.form["image_url"] or None)

    db.session.add(new_user) 
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>") 
def user_profile():
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit_page():
    return render_template("edit_user.html")

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_info():
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    

    db.session.add(edit_user)
    db.session.commit()
    
    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])    
def delete_user():
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit

    return redirect("/users")



