from flask import (
    render_template,
    Blueprint,
)
from flask_login import login_required, current_user

from app.models.bcs import Service, WorkerService, ClientService

blueprint = Blueprint('index', __name__)


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if current_user.is_admin:
        services = Service.query.all()
        assigned_to_self = [ws.service_id for ws in WorkerService.query.filter_by(user_id=current_user.id).all()]
    else:
        services = [service for service in Service.query.all() if service.is_available]
        assigned_to_self = [cs.service_id for cs in ClientService.query.filter_by(user_id=current_user.id).all()]

    return render_template("index.jinja.html",
                           services=services,
                           assigned_to_self=assigned_to_self,
                           is_admin=current_user.is_admin)
