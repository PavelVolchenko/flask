from flask import Flask
from flask import render_template, make_response
from flask import request
from flask import redirect, url_for, flash, session
import db
import logging

app = Flask(__name__)
app.config.update(TEMPLATES_AUTO_RELOAD=True)
app.secret_key = '4514b0a7a24c391b62a3876a5a2055cb831a3f853598bbf6274d2d4f3b986e51'
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    if 'username' in session:
        context = {
            'title': "ArtCentre Главная",
            'user': session.get('username'),
            'cards': db.cards(),
        }
        response = make_response(render_template('index.html', **context))
        print(session)
        return response
    else:
        return redirect(url_for('sign_in'))

@app.route('/sign-in/', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        if not request.form.get('username') or not request.form.get('email'):
            flash('Все поля должны быть заполнены!', 'danger')
            return redirect(url_for('sign_in'))
        else:
            session.update(username=request.form.get('username'))
            session.update(email=request.form.get('email'))
            print(session.get('username'))
            print(session.get('email'))
            return redirect(url_for('index'))
    return render_template('sign-in.html')

@app.route('/logout/')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    print(session.get('username'))
    print(session.get('email'))
    return redirect(url_for('index'))

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
        'user': session.get('username'),
    }
    return render_template('about.html', **context)


@app.route('/contact/')
def contact():
    context = {
        'title': "Контакты",
        'user': session.get('username'),
    }
    return render_template('contact.html', **context)


@app.route('/item-card/')
def item_card():
    context = {
        'title': "Страница товара",
        'user': session.get('username'),
        'plate': db.text_plate(),
    }
    return render_template('item-card.html', **context)


@app.route('/auction/')
def auction():
    context = {
        'title': "Аукцион",
        'user': session.get('username'),
        'auction': db.auction(),
    }
    return render_template('auction.html', **context)


if __name__ == '__main__':
    app.run()
