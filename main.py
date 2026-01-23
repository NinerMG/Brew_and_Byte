from flask import Flask, render_template, request,jsonify, url_for, redirect, flash
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, PasswordField, Form
from wtforms.validators import DataRequired, URL, Email, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin

"""
O projekcie:
-----------
Brew & Byte to aplikacja webowa pomagająca znaleźć idealne kawiarnie 
do pracy zdalnej w Twoim mieście. Podobnie jak LaptopFriendly.co, 
nasza platforma prezentuje kawiarnie z WiFi, gniazdkami i dobrą kawą.

Funkcjonalności:
- 📋 Przeglądanie wszystkich kawiarni w bazie danych
- ➕ Dodawanie nowych miejsc przez użytkowników
- 🗑️ Usuwanie kawiarni z listy
- 🔍 Informacje o: WiFi, gniazdkach, toaletach, cenach kawy

Technologie: Flask, SQLAlchemy, Bootstrap 5, WTForms
"""

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-productio'


#Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Musisz być zalogowany, aby uzyskać dostęp do tej strony."
login_manager.login_message_category = 'info'

# create database
class Base(DeclarativeBase):
    pass

# connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    cafes = relationship('Cafe', backref='owner', lazy=True)

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer,db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class CafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    map_url = StringField('Map URL', validators=[DataRequired(), URL()])
    img_url = StringField('Image URL', validators=[DataRequired(), URL()])
    seats = SelectField('Number of Seats',
                        choices=[('0-10', '0-10'), ('10-20', '10-20'), ('20-30', '20-30'),
                                 ('30-40', '30-40'), ('40-50', '40-50'), ('50+', '50+')],
                        validators=[DataRequired()])
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    has_wifi = BooleanField('Has WiFi', default=True)
    has_sockets = BooleanField('Has Power Sockets', default=True)
    has_toilet = BooleanField('Has Toilet', default=True)
    can_take_calls = BooleanField('Can Take Calls', default=False)
    submit = SubmitField('Zapisz')  # Zmień na uniwersalny tekst

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Hasło musi mieć minimum 8 znaków')
    ])
    confirm_password = PasswordField('Potwierdź hasło', validators=[
        DataRequired(),
        EqualTo('password', message='Hasła muszą być identyczne')
    ])
    submit = SubmitField('Zarejestruj się')

with app.app_context():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = db.session.query(User).filter_by(email=form.email.data).first()
        if existing_user:
            flash('Ten adres email jest już zarejestrowany. Użyj innego', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8,
        )
        new_user = User(
            email=form.email.data,
            password=hashed_password,
            name=form.name.data
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash(f"Witaj {new_user.name}! Twoje konto zostało utworzone", 'success')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Błąd podczas rejestracji: {str(e)}', 'danger')
            return redirect(url_for('register'))


    return render_template('register.html', form=form)

@app.route("/")
def home():
    all_cafes = db.session.query(Cafe).all()
    return render_template("index.html", cafes=all_cafes)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
            user_id=current_user.id
        )
        try:
            db.session.add(new_cafe)
            db.session.commit()
            flash('Kawiarnia dodana pomyślnie', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Błąd podczas dodawania kawiarni: {str(e)}', 'danger')

    return render_template("add_cafe.html", form=form)

@app.route("/delete/<int:cafe_id>")
@login_required
def delete_cafe(cafe_id):
    cafe_to_delete = db.session.get(Cafe, cafe_id)
    if cafe_to_delete:
        try:
            db.session.delete(cafe_to_delete)
            db.session.commit()
            flash('Kawiarnia usunięta!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Błąd podczas usuwania: {str(e)}', 'danger')
    else:
        flash('Nie znaleziono kawiarni!', 'danger')

    return redirect(url_for('home'))


@app.route('/update/cafe/<int:cafe_id>', methods=['GET', 'POST'])
@login_required
def update_cafe(cafe_id):
    cafe_to_update = Cafe.query.get_or_404(cafe_id)
    form = CafeForm(obj=cafe_to_update)

    if form.validate_on_submit():
        cafe_to_update.name = form.name.data
        cafe_to_update.map_url = form.map_url.data
        cafe_to_update.img_url = form.img_url.data
        cafe_to_update.location = form.location.data
        cafe_to_update.has_sockets = form.has_sockets.data
        cafe_to_update.has_toilet = form.has_toilet.data
        cafe_to_update.has_wifi = form.has_wifi.data
        cafe_to_update.can_take_calls = form.can_take_calls.data
        cafe_to_update.seats = form.seats.data
        cafe_to_update.coffee_price = form.coffee_price.data
        cafe_to_update.user_id = current_user.id

        try:
            db.session.commit()
            flash('Kawiarnia zaktualizowana!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Błąd podczas aktualizowania: {str(e)}', 'danger')
    return render_template("update_cafe.html", form=form, cafe=cafe_to_update)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Witaj ponownie, {user.name}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Nieprawidłowy email, lub hasło. Spróbuj ponownie', 'danger')


    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Zostałeś wylogowany', 'info')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

# TODO
# update cafe