from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SECRET_KEY"] = "abc"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def loader_user(user_id):
    return createAccount.query.get(user_id)

class createAccount(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(200), nullable=False)
    lastName = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return'<Task %r>' % self.id
@app.route('/')
@app.route('/create', methods=['POST', 'GET'])
def create():
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


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            logemail = request.form['email-text']
            logpassw = request.form['pass-text']

            combo = db.session.query(createAccount).filter_by(email=logemail, password=logpassw).first()

            if combo:
                return 'You are logged in!'
            else:
                return 'Wrong username and password combination. Please try again'
        except:
            return 'Something went wrong on the server. Please try again'

    else:
        return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
