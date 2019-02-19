from flask import (
    render_template,
    Blueprint,
    Response,
    flash,
    redirect,
    url_for,
    request,
    current_app
)
from flask_login import login_required
import requests

from app.main import db
from app.models.bcs import Service
from app.forms.service import ServiceForm

blueprint = Blueprint('service', __name__)


@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    service_form = ServiceForm()

    if service_form.validate_on_submit():
        data = service_form.data
        new_service = Service(
            name=data['name'],
            description=data['description'],
            location=data['location'],
            type=data['type'],
            workers_needed=data['workers_needed'],
            start_date=data['start_date'],
            end_date=data['end_date']
        )
        db.session.add(new_service)
        db.session.commit()

        flash('Save Successful', 'info')
        return redirect(url_for('index.index'))

    return render_template("service/editor.jinja.html",
                           form=service_form)
