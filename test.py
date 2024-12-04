from flask import Flask, jsonify, make_response, Response, request
import sqlite3
from db import db
import os

if not os.path.exists('db'):
    os.makedirs('db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'  # Table name in the database

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

with app.app_context():
    try:
        db.create_all()
        print(f"Columns in the '{User.__tablename__}' table:")
        for column in User.__table__.columns:
            print(f"- {column.name} ({column.type})")
    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    app.run(debug=True)