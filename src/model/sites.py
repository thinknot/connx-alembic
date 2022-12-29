from datetime import datetime

from ..flapp.extension import db


class Project(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    description = db.Column(db.String, nullable=True)

    # one-to-many relationship: project owns multiple (1 or more) Sites
    sites = db.relationship(
        # instance of Site will have attribute .project
        "Site",
        backref="project",
    )


class Site(db.Model):
    __tablename__ = "site"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 1-to-many relationship with multiple power monitoring Devices
    devices = db.relationship(
        "Device",
        # instance of Device will have attribute .site
        backref="site",
        cascade="all, delete, delete-orphan",
        single_parent=True,
    )

    # sources = db.relationship(
    #     "Power",
    #     backref="site",
    # )

    # relationship with parent energy Project
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))

    # name = db.Column(db.String, unique=True, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    summary = db.Column(db.String, nullable=False)
    pv_power = db.Column(db.Integer(), default=0)
    timezone = db.Column(db.String(50))
    address1 = db.Column(db.String())
    address2 = db.Column(db.String())

    def __repr__(self):
        return f"<Site {self.name} ({self.id})>"
