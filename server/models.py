from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    # Add relationship
    signup = db.relationship("Signup", back_populates = "activity", cascade = 'all, delete-orphan')

    # Add serialization rules
    serialize_rules = ('-signup.activity', )
    
    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    # Add relationship
    signup = db.relationship("Signup", back_populates = "camper", cascade = 'all, delete-orphan')

    # Add serialization rules
    serialize_rules = ('-signup.camper', )

    # Add validation
    @validates('name')
    def validates_name(self, key, name):
        if type(name) == str:
            return name
        else:
            raise ValueError("Name must be a string!")
    
    @validates('age')
    def validates_age(self, key, age):
        if type(age) == int and 8 <= age <= 18:
            return age
        else:
            raise ValueError("Age must be an integer with a value between 8 and 18, inclusive!")

    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

    # Add relationships
    activity = db.relationship("Activity", back_populates = ('signup'))
    camper = db.relationship("Camper", back_populates = ('signup'))

    # Add serialization rules
    serialize_rules = ('-camper.signup', '-activity.signup')
    
    # Add validation
    @validates('time')
    def validates_time(self, key, time):
        if type(time) == int and 0 <= time <= 23:
            return time
        else:
            raise ValueError("Time must be an integer with a value between 0 and 23, inclusive!")
    
    def __repr__(self):
        return f'<Signup {self.id}>'


