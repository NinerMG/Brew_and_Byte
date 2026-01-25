import pytest
from main import app as flask_app, db, User, Cafe
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
    })

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

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
