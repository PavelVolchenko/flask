from flask import Flask, render_template, make_response, request, redirect, url_for, flash, session
import items
import logging
from config import Config
from models import db, User, Post

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
logger = logging.getLogger(__name__)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('OK')


@app.context_processor
def inject_user():
    return dict(user=request.cookies.get('user'))


@app.route('/')
def index():
    context = {
        'title': "Главная страница",
        'cards': items.cards(),
    }
    return render_template('index.html', **context)


@app.route('/sign-in/', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        user = request.form.get('username')
        email = request.form.get('email')
        if not request.form.get('username') or not request.form.get('email'):
            flash("Все поля должны быть заполнены!", 'danger')
            return redirect(url_for('sign_in'))
        else:
            response = make_response(redirect(url_for('index')))
            response.set_cookie('user', user)
            response.set_cookie('email', email)
            return response
    return render_template('sign-in.html')


@app.route('/logout/')
def logout():
    response = make_response(redirect(url_for('sign_in')))
    response.delete_cookie('user')
    response.delete_cookie('email')
    return response


@app.route('/redirect/')
def redirect_to_index():
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    logger.warning(e)
    context = {
        'title': "Страница не найдена!",
        'url': request.base_url,
    }
    return render_template('404.html', **context), 404


@app.route('/about/')
def about():
    context = {
        'title': "О нас",
    }
    return render_template('about.html', **context)


@app.route('/contact/')
def contact():
    context = {
        'title': "Контакты",
    }
    return render_template('contact.html', **context)


@app.route('/item-card/')
def item_card():
    context = {
        'title': "Страница товара",
        'plate': items.text_plate(),
    }
    return render_template('item-card.html', **context)


@app.route('/auction/')
def auction():
    context = {
        'title': "Аукцион",
        'auction': items.auction(),
    }
    return render_template('auction.html', **context)
