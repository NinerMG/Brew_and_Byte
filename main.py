from flask import Flask, render_template, request,jsonify, url_for, redirect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, URL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


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

# create database
class Base(DeclarativeBase):
    pass

# connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

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

class CafeForm(FlaskForm):
    name = SubmitField('Cafe Name', validators=[DataRequired()])
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
    submit = SubmitField('Add Cafe')

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    all_cafes = db.session.query(Cafe).all()
    return render_template("index.html", cafes=all_cafes)

@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if request.method == "POST":
        new_cafe = Cafe(
            name=request.form.get("name") or request.form.get("cafe_name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("loc"),
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=bool(request.form.get("calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price")
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template("add_cafe.html", form=form)

@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    cafe_to_delete = db.session.get(Cafe, cafe_id)
    if cafe_to_delete:
        db.session.delete(cafe_to_delete)
        db.session.commit()
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)

