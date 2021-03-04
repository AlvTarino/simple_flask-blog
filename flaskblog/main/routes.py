from flask import Blueprint
from flask import render_template, request
from flaskblog.models import Post


# instance of the blueprint, with 'main' as name of the blueprint
main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    # query parameter to grab the exact page we want, with the default set to 1 and type int
    page = request.args.get('page', 1, type=int)
    # order_by method to arrange the posts in descending order....most current first
    # adding pagination to only accept 5 posts per page
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', sample=posts)


@main.route('/about')
def about():
    return render_template('about.html', title='About')
