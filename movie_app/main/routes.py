from flask import render_template, request, Blueprint
from movie_app.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('home.html', posts=posts)
    #return "Hello World!"


@main.route("/about")
def about():
    return render_template('about.html')


@main.route("/layout")
def layout():
    return render_template('layout.html')


@main.route("/parts")
def products():
    return render_template('products.html')


@main.route("/cart")
def cart():
    return render_template('cart.html')


@main.route("/cart")
def index():
    return render_template('index.html')
