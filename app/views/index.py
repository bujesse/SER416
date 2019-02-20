from flask import (
    render_template,
    Blueprint,
)
from flask_login import login_required, current_user

from app.models.bcs import Service, WorkerService

blueprint = Blueprint('index', __name__)


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    services = Service.query.all()
    assigned_to_self = [ws.service_id for ws in WorkerService.query.filter_by(user_id=current_user.id).all()]
    return render_template("index.jinja.html",
                           services=services,
                           assigned_to_self=assigned_to_self)
