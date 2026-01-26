from flask import Flask, render_template, request, jsonify, url_for, redirect, flash, session
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, PasswordField, Form
from wtforms.validators import DataRequired, URL, Email, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_babel import Babel, gettext, lazy_gettext as _l

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

# Babel configuration
app.config['BABEL_DEFAULT_LOCALE'] = 'pl'
app.config['BABEL_SUPPORTED_LOCALES'] = ['pl', 'en']
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

babel = Babel(app)

def get_locale():
    """Determine the best language to use for the request."""
    # Try to get language from session
    if 'language' in session:
        return session['language']
    # Otherwise try to guess from browser Accept-Language header
    return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES']) or app.config['BABEL_DEFAULT_LOCALE']

babel.init_app(app, locale_selector=get_locale)

@app.context_processor
def inject_gettext():
    """Udostępnia funkcję tłumaczenia gettext w szablonach Jinja2."""
    return dict(_=gettext)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Musisz być zalogowany, aby uzyskać dostęp do tej strony."
login_manager.login_message_category = 'info'

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(UserMixin, db.Model):
    """Model użytkownika z możliwością dodawania kawiarni.
    
    Attributes:
        id: Unikalny identyfikator użytkownika
        email: Adres email (unikalny)
        password: Zahashowane hasło
        name: Imię i nazwisko użytkownika
        cafes: Relacja do dodanych kawiarni
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    cafes = relationship('Cafe', backref='owner', lazy=True)

class Cafe(db.Model):
    """Model kawiarni z informacjami o udogodnieniach dla pracy zdalnej.
    
    Attributes:
        id: Unikalny identyfikator kawiarni
        name: Nazwa kawiarni
        map_url: Link do lokalizacji na mapie
        img_url: URL zdjęcia kawiarni
        location: Adres/lokalizacja
        seats: Liczba miejsc siedzących
        has_toilet: Czy ma toaletę
        has_wifi: Czy ma WiFi
        has_sockets: Czy ma gniazdka elektryczne
        can_take_calls: Czy można odbierać rozmowy telefoniczne
        coffee_price: Cena kawy
        user_id: ID użytkownika który dodał kawiarnię
    """
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
    """Funkcja callback do ładowania użytkownika z sesji dla Flask-Login.
    
    Args:
        user_id: ID użytkownika do załadowania
        
    Returns:
        User: Obiekt użytkownika lub None
    """
    return db.session.get(User, int(user_id))

class CafeForm(FlaskForm):
    """Formularz do dodawania i edycji kawiarni."""
    name = StringField(_l('Cafe Name'), validators=[DataRequired()])
    location = StringField(_l('Location'), validators=[DataRequired()])
    map_url = StringField(_l('Map URL'), validators=[DataRequired(), URL()])
    img_url = StringField(_l('Image URL'), validators=[DataRequired(), URL()])
    seats = SelectField(_l('Number of Seats'),
                        choices=[('0-10', '0-10'), ('10-20', '10-20'), ('20-30', '20-30'),
                                 ('30-40', '30-40'), ('40-50', '40-50'), ('50+', '50+')],
                        validators=[DataRequired()])
    coffee_price = StringField(_l('Coffee Price'), validators=[DataRequired()])
    has_wifi = BooleanField(_l('Has WiFi'), default=True)
    has_sockets = BooleanField(_l('Has Power Sockets'), default=True)
    has_toilet = BooleanField(_l('Has Toilet'), default=True)
    can_take_calls = BooleanField(_l('Can Take Calls'), default=False)
    submit = SubmitField(_l('Save'))

class LoginForm(FlaskForm):
    """Formularz logowania użytkownika."""
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Login'))

class RegisterForm(FlaskForm):
    """Formularz rejestracji nowego użytkownika."""
    name = StringField(_l('Name'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[
        DataRequired(),
        Length(min=8, message=_l('Password must be at least 8 characters'))
    ])
    confirm_password = PasswordField(_l('Confirm Password'), validators=[
        DataRequired(),
        EqualTo('password', message=_l('Passwords must match'))
    ])
    submit = SubmitField(_l('Register'))

with app.app_context():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Rejestracja nowego użytkownika z walidacją i hashowaniem hasła.
    
    Returns:
        Przekierowanie do strony głównej po udanej rejestracji
        lub renderowanie formularza rejestracji
    """
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
    """Strona główna wyświetlająca wszystkie kawiarnie.
    
    Returns:
        Renderowana strona z listą kawiarni
    """
    all_cafes = db.session.query(Cafe).all()
    return render_template("index.html", cafes=all_cafes)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_cafe():
    """Dodawanie nowej kawiarni do bazy danych (wymaga logowania).
    
    Returns:
        Przekierowanie do strony głównej po dodaniu kawiarni
        lub renderowanie formularza dodawania
    """
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
    """Usuwanie kawiarni z bazy danych (wymaga logowania).
    
    Args:
        cafe_id: ID kawiarni do usunięcia
        
    Returns:
        Przekierowanie do strony głównej
    """
    cafe_to_delete = db.session.get(Cafe, cafe_id)
    if cafe_to_delete.user_id != current_user.id:
        flash('Nie masz uprawnień!', 'danger')
        return redirect(url_for('home'))
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
    """Edycja istniejącej kawiarni (wymaga logowania).
    
    Args:
        cafe_id: ID kawiarni do edycji
        
    Returns:
        Przekierowanie do strony głównej po aktualizacji
        lub renderowanie formularza edycji
    """
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
    """Logowanie użytkownika z weryfikacją hasła.
    
    Returns:
        Przekierowanie do strony głównej po udanym logowaniu
        lub renderowanie formularza logowania
    """
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
    """Wylogowanie zalogowanego użytkownika.
    
    Returns:
        Przekierowanie do strony głównej
    """
    logout_user()
    flash('Zostałeś wylogowany', 'info')
    return redirect(url_for('home'))

@app.route('/set-language/<language>')
def set_language(language):
    """Zmiana języka aplikacji (PL/EN).
    
    Args:
        language: Kod języka ('pl' lub 'en')
        
    Returns:
        Przekierowanie do poprzedniej strony lub strony głównej
    """
    if language in app.config['BABEL_SUPPORTED_LOCALES']:
        session['language'] = language
        flash(gettext('Language changed successfully!'), 'success')
    return redirect(request.referrer or url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

