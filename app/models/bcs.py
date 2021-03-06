from app.main import db
from sqlalchemy.sql import func
from sqlalchemy_utils import ArrowType


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    description = db.Column(db.String(255), unique=False, nullable=False)
    location = db.Column(db.String(255), unique=False, nullable=False)
    start_date = db.Column(ArrowType, server_default=func.now(), index=True)
    end_date = db.Column(ArrowType, server_default=func.now(), index=True)
    type = db.Column(db.String(255), unique=False, nullable=True)
    workers_needed = db.Column(db.Integer, nullable=False)

    @property
    def workers_assigned(self):
        return len(WorkerService.query.filter_by(service_id=self.id).all())

    @property
    def is_available(self):
        return self.workers_assigned == self.workers_needed

    @property
    def users_signed_up(self):
        return len(ClientService.query.filter_by(service_id=self.id).all())


class WorkerService(db.Model):
    __tablename__ = 'worker_services'
    """Association object model to handle the relationship between worker users and services"""
    service_id = db.Column(db.BigInteger, db.ForeignKey('services.id', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True)
    service = db.relationship('Service', lazy='joined')


class ClientService(db.Model):
    __tablename__ = 'client_services'
    """Association object model to handle the relationship between client users and services"""
    service_id = db.Column(db.BigInteger, db.ForeignKey('services.id', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True)
    service = db.relationship('Service', lazy='joined')
