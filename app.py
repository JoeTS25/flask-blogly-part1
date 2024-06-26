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
##############################################################

# User routes

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
###################################################################

# Post Routes

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post(user_id):
    """Submit new user post form"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'], content=request.form['content'],
                    user=user)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    """Shows specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Edit Specific Post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Deletes Specific Post"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

#####################################################################

# Tag Routes

@app.route('/tags')
def tags_list():
    """Lists all tags with links to individual tags"""

    tags = Tag.query.all()
    return render_template('tags/tag_list.html', tags=tags)

@app.route('/tags/new')
def add_tag():
    """Form to enter new tag"""

    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)

@app.route('/tags/new', methods=["POST"])
def make_tag():
    """Creates new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id')
def show_tags(tag_id):
    """Show page with tag info"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """Gets form to edit tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def make_tag_edit(tag_id):
    """Submits tag editing form"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Deletes tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')

