from app.main import db
from app.models.bcs import Service, ClientService, WorkerService


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.UnicodeText, nullable=False)
    first_name = db.Column(db.UnicodeText, nullable=False)
    last_name = db.Column(db.UnicodeText, nullable=False)
    role = db.Column(db.UnicodeText, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    enabled = db.Column(db.Boolean(), nullable=False, default=True, server_default='1')

    client_services = db.relationship('ClientService', cascade='all, delete-orphan', backref='users')
    worker_services = db.relationship('WorkerService', cascade='all, delete-orphan', backref='users')

    @property
    def full_name(self):
        return ' '.join([self.first_name, self.last_name])

    # Required for flask-login
    @property
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
