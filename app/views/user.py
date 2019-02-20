from flask import (
    render_template,
    Blueprint,
    request,
    flash,
    redirect,
    url_for,
    )
from flask_login import login_user, logout_user, current_user
from app.main import db
from app.models.user import User
from app.forms.user import UserForm

from app.services.auth import (
    AuthenticationError,
    InvalidCredentialsError,
    AccountError,
    authenticate_user,
    )

blueprint = Blueprint('user', __name__)


@blueprint.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('index.index'))

    return render_template(
        'user/login.jinja.html'
    )


@blueprint.route('/login', methods=['POST'])
def do_login():
    try:
        user = authenticate_user(request.form.get('username'), request.form.get('password'))
        login_user(user, remember=True)
        flash('Welcome back, %s' % (user.first_name,), 'info')
        return redirect(url_for('index.index'))
    except InvalidCredentialsError:
        flash('Invalid username or password', 'error')
    except AccountError as e:
        flash(str(e), 'error')
    except AuthenticationError:
        flash('Unexpected authentication failure', 'error')

    return redirect(url_for('user.login'))


@blueprint.route('/list', methods=['GET'])
def user_list():
    users = User.query.all()
    return render_template('user/list.jinja.html',
                           users=users)


@blueprint.route('/create', methods=['GET', 'POST'])
def create():
    form = UserForm()
    if form.validate_on_submit():
        new_user = User()
        form.populate_obj(new_user)
        if not form.data['username']:
            new_user.username = '.'.join([form.data['first_name'].lower(), form.data['last_name'].lower()])

        db.session.add(new_user)
        db.session.commit()

        flash('Save Successful', 'success')
        return redirect(url_for('user.user_list'))
    return render_template('common/editor.jinja.html',
                           title='User',
                           form=form)


@blueprint.route('/edit/<user_id>', methods=['GET', 'POST'])
def edit(user_id):
    user_obj = User.query.get(user_id)
    user_form = UserForm(obj=user_obj)

    if user_form.validate_on_submit():
        if not user_form.data['password']:
            password = user_obj.password
            user_form.populate_obj(user_obj)
            user_obj.password = password
        else:
            user_form.populate_obj(user_obj)
        db.session.add(user_obj)
        db.session.commit()

        flash('Save Successful', 'success')
        return redirect(url_for('user.user_list'))

    return render_template('common/editor.jinja.html',
                           title='User',
                           form=user_form)


@blueprint.route('/delete/<user_id>', methods=['GET'])
def delete(user_id):
    db.session.delete(User.query.get(user_id))
    db.session.commit()
    flash('Deletion Successful', 'success')
    return redirect(url_for('user.user_list'))


@blueprint.route('/profile/<user_id>', methods=['POST'])
def profile(user_id):
    return render_template('user/profile.jinja.html')


@blueprint.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('user.login'))
