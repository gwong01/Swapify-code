from flask import Flask, render_template, request, flash, redirect, url_for
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

class SonnyItems(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    series = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=False)
    mrk_value = db.Column(db.Float, nullable=False)
    images = db.Column(db.String(200, nullable=False))
    favorite = db.Column(db.Boolean, default=0)

    def __repr__(self):
        return'<Task %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/common')
def common():
    return render_template('common.html')


@app.route('/limited')
def limited():
    return render_template('limited.html')


@app.route('/discontinued')
def discontinued():
    return render_template('discontinued.html')


@app.route('/secrets')
def secrets():
    return render_template('secrets.html')


@app.route('/robbie')
def robbie():
    return render_template('robbie.html')


@app.route('/favorites')
def favorites():
    return render_template('favorites.html')


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
            flash("Username already exists.", 'error')
            return redirect(url_for('create'))
        elif emailExists:
            flash("Email already exists.", 'error')
            return redirect(url_for('create'))
        else:
            try:
                db.session.add(createAccount(firstName=first, lastName=last, username=user, email=em, password=passw))
                db.session.commit()
                flash('You signed up!', 'info')
                return redirect(url_for('index'))
            except:
                flash('There was an issue adding one of your inputs.', 'error')
                return redirect(url_for('create'))

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
                flash('You are logged in!', 'info')
                return redirect(url_for('index'))
            else:
                flash('Wrong username and password combination. Please try again', 'error')
                return redirect(url_for('login'))
        except:
            flash('Something went wrong on the server. Please try again', 'error')
            return redirect(url_for('login'))

    else:
        return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)