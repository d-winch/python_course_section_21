from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from send_email import send_email

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:__REDACTED__@localhost/python_web_app_s21'
app.config['SQLALCHEMY_DATABASE_URI']='__REDACTED__?sslmode=require'
db = SQLAlchemy(app)

class Data(db.Model):

    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(120), unique=True)
    height_ = db.Column(db.Float)

    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form["form_email"]
        height = request.form["form_height"]
        if db.session.query(Data).filter(Data.email_ == email).count() == 0:
            data = Data(email, height)
            db.session.add(data)
            db.session.commit()
            average_height = db.session.query(func.avg(Data.height_)).scalar()
            print(average_height)
            average_height = round(average_height, 2)
            count = db.session.query(Data.height_).count()
            send_email(email, height, average_height, count)
            return render_template("success.html")
        return render_template("index.html",
        text="That email address has already been used. Please enter a new one.")

if __name__ == '__main__':
    app.debug = True
    app.run()
