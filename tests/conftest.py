import pytest
import os
import shutil
from main import app as flask_app, db, User, Cafe
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='session', autouse=True)
def backup_production_db():
    """
    BEZPIECZEŃSTWO: Tworzy kopię zapasową produkcyjnej bazy przed testami.
    Jeśli coś pójdzie źle, możesz przywrócić bazę z pliku .backup
    """
    prod_db = os.path.join(os.path.dirname(__file__), '..', 'instance', 'cafes.db')
    backup_db = os.path.join(os.path.dirname(__file__), '..', 'instance', 'cafes.db.backup')
    
    if os.path.exists(prod_db):
        shutil.copy2(prod_db, backup_db)
        print(f"\n🛡️  Kopia zapasowa produkcyjnej bazy: {backup_db}")
    
    yield


@pytest.fixture
def app():
    """
    Fixture aplikacji - używa TYLKO testowej bazy danych.
    
    ROZWIĄZANIE: Modyfikacja wewnętrznego słownika db.engines.
    Flask-SQLAlchemy 3.x ma db.engine jako read-only property, ale db.engines jest dict.
    """
    # Ścieżka do testowej bazy
    test_db_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'instance', 'test_cafes.db'
    ))

    original_uri = flask_app.config.get('SQLALCHEMY_DATABASE_URI')
    
    # Ustaw konfigurację testową
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{test_db_path}"
    flask_app.config['WTF_CSRF_ENABLED'] = False
    
    with flask_app.app_context():
        original_engine = db.engine

        db.session.remove()

        from sqlalchemy import create_engine
        new_engine = create_engine(f"sqlite:///{test_db_path}")

        db.engines[None] = new_engine

        db.metadata.bind = new_engine

        db.create_all()

        actual_db = db.engine.url.database
        print(f"\n✅ Używana baza: {actual_db}")

        assert 'test_cafes.db' in str(actual_db), f"BŁĄD! Używana baza: {actual_db}"
        
        yield flask_app

        db.session.remove()
        db.drop_all()

        new_engine.dispose()

        db.engines[None] = original_engine
        db.metadata.bind = original_engine

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = original_uri
    flask_app.config['TESTING'] = False

    if os.path.exists(test_db_path):
        try:
            os.remove(test_db_path)
        except:
            pass

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_user(app):
    with app.app_context():
        hashed_pw = generate_password_hash("password123", method='pbkdf2:sha256', salt_length=8)
        user = User(email="test@example.com", password=hashed_pw, name="Tester")
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user

@pytest.fixture
def sample_cafe(app, auth_user):
    """Tworzy testową kawiarnię w bazie danych."""
    cafe = Cafe(
        name="Testowa Kawiarnia",
        map_url="https://google.com/maps",
        img_url="https://images.com/cafe.jpg",
        location="Kraków",
        has_sockets=True,
        has_toilet=True,
        has_wifi=True,
        can_take_calls=True,
        seats="20-30",
        coffee_price="12 PLN",
        user_id=auth_user.id
    )
    db.session.add(cafe)
    db.session.commit()

    return cafe

@pytest.fixture
def login_user(client, email, password):
    """Helper: Loguje użytkownika."""
    return client.post('/login', data={
        'email': email,
        'password': password
    }, follow_redirects=True)

@pytest.fixture
def logout_user(client):
    """Helper: Wylogowuje użytkownika."""
    return client.get('/logout', follow_redirects=True)

@pytest.fixture
def register_user(client, name, email, password):
    """Helper: Rejestruje nowego użytkownika."""
    return client.post('/register', data={
        'name': name,
        'email': email,
        'password': password,
        'confirm_password': password
    }, follow_redirects=True)

@pytest.fixture
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

@pytest.fixture
def update_cafe(client, cafe_id, cafe_data):
    """Helper: Aktualizuje kawiarnię."""
    return client.post(f'/update/cafe/{cafe_id}', data=cafe_data, follow_redirects=True)

@pytest.fixture
def delete_cafe(client, cafe_id):
    """Helper: Usuwa kawiarnię."""
    return client.get(f'/delete/{cafe_id}', follow_redirects=True)

@pytest.fixture
def set_language(client, lang_code):
    """Helper: Ustawia język aplikacji."""
    return client.get(f'/set-language/{lang_code}', follow_redirects=True)