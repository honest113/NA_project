from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from na_service import app, db, posts, logger, logger_post
from na_service.models import Post
from na_service.posts.forms import PostForm

posts = Blueprint("posts", __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        logger_post.info(f"A post has been created by {current_user.username}, post_id = {post.id}")
        flash("Your post has been created!", "success")
        return redirect(url_for('main.home'))
    return render_template("create_post.html", title="New Post", form=form, legend="Create Post")

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/update/<int:post_id>", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        logger_post.info(f"The post: {post.id} has been updated by {current_user.username}")
        flash("Your post has been updated!", "success")
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update Post", form=form, legend="Update Post")

@posts.route("/post/delete/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    logger_post.warning(f"The post: title - {post.title} has been deleted by {current_user.username}")
    flash("Your post has been deleted!", "success")
    return redirect(url_for("main.home"))