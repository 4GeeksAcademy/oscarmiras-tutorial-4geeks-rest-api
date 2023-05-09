from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, default=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    elapsed_time = db.Column(db.Integer, nullable=False)
    attempts = db.Column(db.Integer, nullable=False)
    machine = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Score %r>' % self.machine

    def serialize(self):
        return {
            "machine": self.machine,
            "attemps": self.attempts,
            "elapsed_time": self.elapsed_time,
        }