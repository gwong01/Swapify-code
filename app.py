from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class createAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(200), nullable=False)
    lastName = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return'<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return 'HELLO'
    else:
        return render_template('create-account.html')

if __name__ == "__main__":
    app.run(debug=True)