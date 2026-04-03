from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Listing

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    total_listings = Listing.query.count()

    user_listings = 0
    if current_user.is_authenticated:
        user_listings = Listing.query.filter_by(landlord_id=current_user.id).count()

    recent_listings = Listing.query.order_by(Listing.id.desc()).limit(3).all()

    return render_template(
        'index.html',
        total_listings=total_listings,
        user_listings=user_listings,
        recent_listings=recent_listings
)


@app.route("/")
def index():
    return render_template("index.html")

from flask import request, redirect, url_for

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)

        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=hashed_password,
            role="tenant"
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('register.html')

from flask_login import login_user
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))

        else:
            return "Invalid email or password"

    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/listings')
def listings():
    query = Listing.query

    # Get search inputs
    location = request.args.get('location')
    max_price = request.args.get('max_price')
    room_type = request.args.get('room_type')

    # Apply filters
    if location:
        query = query.filter(Listing.location.ilike(f"%{location}%"))

    if max_price:
        query = query.filter(Listing.price <= float(max_price))

    if room_type:
        query = query.filter(Listing.room_type == room_type)

    listings = query.all()

    return render_template('listings.html', listings=listings)

@app.route('/add_listing', methods=['GET', 'POST'])
def add_listing():
    if request.method == 'POST':
        title = request.form.get('title')
        location = request.form.get('location')
        price = request.form.get('price')
        room_type = request.form.get('room_type')
        description = request.form.get('description')

        new_listing = Listing(
            title=title,
            location=location,
            price=float(price),
            room_type=room_type,
            description=description,
            landlord_id=current_user.id
        )

        db.session.add(new_listing)
        db.session.commit()

        return redirect(url_for('listings'))

    return render_template('add_listing.html')

@app.route('/delete_listing/<int:listing_id>')
@login_required
def delete_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)

    if listing.landlord_id != current_user.id:
        return "Access denied", 403

    db.session.delete(listing)
    db.session.commit()

    return redirect(url_for('listings'))

@app.route('/edit_listing/<int:listing_id>', methods=['GET', 'POST'])
@login_required
def edit_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)

    if listing.landlord_id != current_user.id:
        return "Access denied", 403

    if request.method == 'POST':
        listing.title = request.form['title']
        listing.location = request.form['location']
        listing.price = request.form['price']
        listing.room_type = request.form['room_type']
        listing.description = request.form['description']

        db.session.commit()

        return redirect(url_for('listings'))

    return render_template('edit_listing.html', listing=listing)


if __name__ == "__main__":
   with app.app_context():
       db.create_all()
   app.run(debug=True)
