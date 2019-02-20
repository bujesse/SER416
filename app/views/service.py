from flask import (
    render_template,
    Blueprint,
    flash,
    redirect,
    url_for,
)
from flask_login import login_required
import arrow

from app.main import db
from app.models.bcs import Service
from app.forms.service import ServiceForm

blueprint = Blueprint('service', __name__)


@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    service_form = ServiceForm()
    if service_form.validate_on_submit():
        new_service = Service()
        service_form.populate_obj(new_service)
        new_service.start_date = parse_time(new_service.start_date)
        new_service.end_date = parse_time(new_service.end_date)

        db.session.add(new_service)
        db.session.commit()

        flash('Save Successful', 'info')
        return redirect(url_for('index.index'))

    return render_template("service/editor.jinja.html",
                           form=service_form)


@blueprint.route('/edit/<service_id>', methods=['GET', 'POST'])
@login_required
def edit(service_id):
    service_obj = Service.query.get(service_id)
    service_obj.start_date = service_obj.start_date.format('MM/DD/YYYY HH:mm A')
    service_obj.end_date = service_obj.end_date.format('MM/DD/YYYY HH:mm A')
    service_form = ServiceForm(obj=service_obj)

    if service_form.validate_on_submit():
        service_form.populate_obj(service_obj)
        service_obj.start_date = parse_time(service_obj.start_date)
        service_obj.end_date = parse_time(service_obj.end_date)
        db.session.add(service_obj)
        db.session.commit()

        flash('Save Successful', 'info')
        return redirect(url_for('index.index'))

    return render_template("service/editor.jinja.html",
                           form=service_form)


@blueprint.route('/delete/<service_id>', methods=['GET'])
def delete(service_id):
    db.session.delete(Service.query.get(service_id))
    db.session.commit()
    flash('Deletion Successful', 'info')
    return redirect(url_for('index.index'))


def parse_time(time):
    try:
        return arrow.get(time, 'MM/DD/YYYY H:mm A')
    except Exception:
        return arrow.get(time, 'MM/DD/YYYY HH:mm A')
