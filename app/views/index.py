from flask import (
    render_template,
    Blueprint,
)
from flask_login import login_required

from app.models.bcs import Service

blueprint = Blueprint('index', __name__)


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    services = Service.query.all()
    return render_template("index.jinja.html",
                           services=services)
