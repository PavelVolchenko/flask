from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
import db
import logging

app = Flask(__name__)
app.config.update(TEMPLATES_AUTO_RELOAD=True)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    context = {
        'title': "ArtCentre Главная",
        'cards': db.cards(),
    }
    return render_template('index.html', **context)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        user = request.form.get('name')
        email = request.form.get('email')
        return f'Hello {user}! Email: {email}'
    return render_template('sign-in.html')


@app.route('/sign-in/')
def sign_in():
    context = {
        'title': "Авторизация",
    }
    return render_template('sign-in.html', **context)


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
        'plate': db.text_plate(),
    }
    return render_template('item-card.html', **context)


@app.route('/auction/')
def auction():
    context = {
        'title': "Аукцион",
        'auction': db.auction(),
    }
    return render_template('auction.html', **context)


if __name__ == '__main__':
    app.run()
