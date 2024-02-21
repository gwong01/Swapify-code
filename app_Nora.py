from flask import Flask, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

#
@app.route('/sonny-items')
def sonny_items():
    items = Sonny.query.all()  # Fetch all items from the sonny table
    return render_template('sonny_items.html', items=items)

# Inventory
@app.route('/add_inventory', methods=['POST'])
def add_inventory():
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    name = request.form['name']
    series = request.form.get('series', '')
    category = request.form.get('category', '')
    mrk_value = request.form.get('mrk_value', 0.0)
    images = request.form.get('images', '')
    favorite = 'favorite' in request.form

    cursor.execute('''
          INSERT INTO inventory (name, series, category, mrk_value, images, Favorite)
          VALUES (?, ?, ?, ?, ?, ?)
      ''', (name, series, category, mrk_value, images, favorite))

    conn.commit()
    conn.close()

    # get the page for the sonny
    return redirect(url_for('profile'))

# Profile
@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        # If not logged in, redirect to the login page
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    if user:
        # Assuming you have models for inventory and favorites, fetch them here
        # For example: user_inventory = Inventory.query.filter_by(user_id=user_id).all()
        return render_template('profile.html', user=user)
    else:
        # Handle case where user is not found, e.g., session corruption
        return redirect(url_for('login'))

# logging in
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id  # Log in the user by storing their user ID in the session
            return redirect(url_for('profile'))
        else:
            # Handle login failure
            pass
    # Render the login template if GET request or login failed
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove the user ID from the session to log out the user
    return redirect(url_for('index'))

# Home
@app.route('/')
def index():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)