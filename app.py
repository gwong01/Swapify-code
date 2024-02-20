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
        first = request.form['first-text']
        last = request.form['last']
        user = request.form['user-text']
        em = request.form['email-text']
        passw = request.form['pass-text']

        userExists = db.session.query(createAccount.id).filter_by(username=user).first() is not None
        emailExists = db.session.query(createAccount.id).filter_by(email=em).first() is not None
        if userExists:
            return "Username already exists."
        elif emailExists:
            return "Email already exists."
        else:
            try:
                db.session.add(createAccount(firstName=first, lastName=last, username=user, email=em, password=passw))
                db.session.commit()
                return 'You signed up!'
            except:
                return 'There was an issue adding one of your inputs.'

    else:
        return render_template('create-account.html')

if __name__ == "__main__":
    app.run(debug=True)
