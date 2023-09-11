from flask import Flask, render_template, make_response, request, redirect, url_for, flash, session
from flask_wtf import CSRFProtect
import items
import logging
from config import Config
from models import db, add_user, User
from form import RegistrationForm, LoginForm
from models import verify_password

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
csrf = CSRFProtect(app)
logger = logging.getLogger(__name__)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('OK')


@app.context_processor
def inject_user():
    return dict(user=request.cookies.get('first_name'))


@app.route('/')
def index():
    context = {
        'title': "Главная страница",
        'cards': items.cards(),
    }
    return render_template('index.html', **context)


@app.route('/sign-in/', methods=['GET', 'POST'])
@csrf.exempt
def sign_in():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        user_dict = dict()
        user_dict.update(
            {
                'first_name': form.first_name.data,
                'last_name': form.last_name.data,
                'email': form.email.data,
                'password': form.password.data,
            }
        )
        response = make_response(redirect(url_for('index')))
        response.set_cookie('first_name', user_dict.get('first_name'))
        print(add_user(user_dict))
        return response
    return render_template('sign-in.html', form=form)


@app.route('/sign-up/', methods=['GET', 'POST'])
@csrf.exempt
def sign_up():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user_dict = dict()
        user_dict.update(
            {
                'email': form.email.data,
                'password': form.password.data,
            }
        )
        user = User.query.filter_by(email=user_dict.get('email')).first()
        print(user.password)
        if verify_password(user_dict.get('password'), user.password):
            print('OK!')
            response = make_response(redirect(url_for('index')))
            response.set_cookie('first_name', user.first_name)
        return response
    return render_template('sign-up.html', form=form)


@app.route('/logout/')
def logout():
    response = make_response(redirect(url_for('sign_in')))
    response.delete_cookie('first_name')
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
