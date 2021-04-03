from na_service import app, logger
from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user
from na_service.models import Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    if current_user.is_authenticated:
        app.logger.info(f"A request to homepage - user: {current_user.username}")
    else:
        app.logger.info("A request to homepage")
    return render_template("home.html", posts=posts, title="Home")

@main.route('/about')
def about():
    return render_template("about.html", title="About")
