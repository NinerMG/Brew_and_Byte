# ========================================
# DODATKOWE FIXTURES - Dodaj do conftest.py
# ========================================
# Te fixtures będą potrzebne do niektórych testów

"""
Dodaj te fixtures do swojego conftest.py
"""

import pytest
from main import User, Cafe, db
from werkzeug.security import generate_password_hash


@pytest.fixture
def second_user(app):
    """Fixture: Drugi użytkownik testowy."""
    with app.app_context():
        hashed_pw = generate_password_hash("password456", method='pbkdf2:sha256', salt_length=8)
        user = User(email="user2@example.com", password=hashed_pw, name="Second User")
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user


@pytest.fixture
def third_user(app):
    """Fixture: Trzeci użytkownik testowy."""
    with app.app_context():
        hashed_pw = generate_password_hash("password789", method='pbkdf2:sha256', salt_length=8)
        user = User(email="user3@example.com", password=hashed_pw, name="Third User")
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user


@pytest.fixture
def multiple_cafes(app, auth_user):
    """Fixture: Kilka kawiarni dla testów."""
    cafes = []
    cafe_data = [
        {"name": "Cafe Alpha", "location": "Warsaw"},
        {"name": "Cafe Beta", "location": "Krakow"},
        {"name": "Cafe Gamma", "location": "Gdansk"},
    ]
    
    with app.app_context():
        for data in cafe_data:
            cafe = Cafe(
                name=data["name"],
                map_url="https://maps.google.com/test",
                img_url="https://images.com/test.jpg",
                location=data["location"],
                has_sockets=True,
                has_toilet=True,
                has_wifi=True,
                can_take_calls=False,
                seats="20-30",
                coffee_price="15 PLN",
                user_id=auth_user.id
            )
            db.session.add(cafe)
            cafes.append(cafe)
        
        db.session.commit()
        for cafe in cafes:
            db.session.refresh(cafe)
    
    return cafes


@pytest.fixture
def cafe_by_second_user(app, second_user):
    """Fixture: Kawiarnia należąca do drugiego użytkownika."""
    with app.app_context():
        cafe = Cafe(
            name="Second User's Cafe",
            map_url="https://maps.google.com/test2",
            img_url="https://images.com/test2.jpg",
            location="Wroclaw",
            has_sockets=True,
            has_toilet=True,
            has_wifi=True,
            can_take_calls=True,
            seats="10-20",
            coffee_price="18 PLN",
            user_id=second_user.id
        )
        db.session.add(cafe)
        db.session.commit()
        db.session.refresh(cafe)
        return cafe


# ========================================
# HELPER FUNCTIONS
# ========================================
# Dodaj te funkcje pomocnicze do conftest.py lub osobnego pliku helpers.py

def login_user(client, email, password):
    """Helper: Loguje użytkownika."""
    return client.post('/login', data={
        'email': email,
        'password': password
    }, follow_redirects=True)


def logout_user(client):
    """Helper: Wylogowuje użytkownika."""
    return client.get('/logout', follow_redirects=True)


def register_user(client, name, email, password):
    """Helper: Rejestruje nowego użytkownika."""
    return client.post('/register', data={
        'name': name,
        'email': email,
        'password': password,
        'confirm_password': password
    }, follow_redirects=True)


def add_cafe(client, cafe_data):
    """Helper: Dodaje kawiarnię."""
    default_data = {
        "name": "Test Cafe",
        "location": "Test City",
        "map_url": "https://maps.google.com/test",
        "img_url": "https://images.com/test.jpg",
        "seats": "10-20",
        "coffee_price": "15 PLN",
        "has_wifi": True,
        "has_sockets": True,
        "has_toilet": True,
        "can_take_calls": False
    }
    default_data.update(cafe_data)
    return client.post('/add', data=default_data, follow_redirects=True)


def update_cafe(client, cafe_id, cafe_data):
    """Helper: Aktualizuje kawiarnię."""
    return client.post(f'/update/cafe/{cafe_id}', data=cafe_data, follow_redirects=True)


def delete_cafe(client, cafe_id):
    """Helper: Usuwa kawiarnię."""
    return client.get(f'/delete/{cafe_id}', follow_redirects=True)


def set_language(client, lang_code):
    """Helper: Ustawia język aplikacji."""
    return client.get(f'/set-language/{lang_code}', follow_redirects=True)


# ========================================
# PRZYKŁADY UŻYCIA HELPERS
# ========================================

"""
def test_example_using_helpers(client, auth_user):
    # Zaloguj użytkownika
    login_user(client, "test@example.com", "password123")
    
    # Dodaj kawiarnię
    response = add_cafe(client, {
        "name": "My Cafe",
        "location": "Warsaw"
    })
    assert "Kawiarnia dodana pomyślnie" in response.data.decode()
    
    # Zmień język
    set_language(client, 'en')
    
    # Wyloguj
    logout_user(client)
"""
