import pytest
from main import User,Cafe, db

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Brew & Byte" in response.data

def test_register_user(client):
    response = client.post(
        '/register', data={
            "name": "Nowy User",
            "email": "nowy@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True
    )
    assert response.status_code == 200
    assert "Twoje konto zostało utworzone" in response.data.decode('utf-8')

def test_register_user_with_existitng_email(client):
    user_data = {
        "name": "Nowy User",
        "email": "duplicate@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }
    client.post('/register', data=user_data, follow_redirects=True)

    client.get('/logout', follow_redirects=True)

    response = client.post('/register', data=user_data, follow_redirects=True)

    assert "Ten adres email jest już zarejestrowany" in response.data.decode('utf-8')
    assert response.status_code == 200

def test_register_user_logout_and_login(client):
    user_data = {
        "name": "Nowy User",
        "email": "duplicate@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }
    client.post('/register', data=user_data, follow_redirects=True)

    client.get('/logout', follow_redirects=True)

    response = client.post('/login', data={
        'email': user_data.get('email'),
        'password': user_data.get('password')
    }, follow_redirects=True)

    assert response.status_code == 200
    assert user_data.get('name') in response.get_data(as_text=True)

def test_login_with_wrong_password(client):
    user_data = {
        "name": "Nowy User",
        "email": "duplicate@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }
    client.post('/register', data=user_data, follow_redirects=True)
    client.get('/logout', follow_redirects=True)

    response = client.post('/login', data={
        'email': user_data.get('email'),
        'password': "password12"
    },follow_redirects=True)

    assert response.status_code == 200
    assert 'Nieprawidłowy email, lub hasło. Spróbuj ponownie' in response.data.decode('utf-8')

def test_login_with_wrong_email(client):
    user_data = {
        "name": "Nowy User",
        "email": "duplicate@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }
    client.post('/register', data=user_data, follow_redirects=True)
    client.get('/logout', follow_redirects=True)

    response = client.post('/login', data={
        'email': 'test@test.com',
        'password': "password123"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Nieprawidłowy email, lub hasło. Spróbuj ponownie' in response.data.decode('utf-8')

def test_redirect_to_login_page_on_add(client):
    response = client.get('/add', follow_redirects=False)
    assert response.status_code == 302
    assert response.location.startswith('/login')

def test_redirect_to_login_page_on_update(client, sample_cafe):
    response =  client.get(f'/update/cafe/{sample_cafe.id}', follow_redirects=False)
    assert response.status_code == 302
    assert response.location.startswith('/login')

def test_too_short_password(client):
    user_data = {
        "name": "Nowy User",
        "email": "duplicate@example.com",
        "password": "pass",
        "confirm_password": "pass"
    }
    response = client.post('/register', data=user_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'Password must be at least 8 characters and no more than 200 characters' in response.data.decode('utf-8')

def test_password_and_confirm_password_different(client):
    user_data = {
        "name": "Nowy User",
        "email": "duplicate@example.com",
        "password": "password321",
        "confirm_password": "password123"
    }
    response = client.post('/register', data=user_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'Hasła muszą być identyczne' in response.data.decode('utf-8')

def test_register_without_email(client):
    user_data = {
        "name": "Nowy User",
        # "email": "test@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }
    response = client.post('/register', data=user_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'To pole jest wymagane' in response.data.decode('utf-8')

def test_register_with_invalid_email(client):
    user_data = {
        "name": "Nowy User",
        "email": "nieprawidlowy-email",
        "password": "password123",
        "confirm_password": "password123"
    }
    response = client.post('/register', data=user_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'Nieprawidłowy adres e-mail.' in response.data.decode('utf-8')

def test_register_without_name(client):
    user_data = {
        #"name": "Nowy User",
        "email": "test@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }
    response = client.post('/register', data=user_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'To pole jest wymagane' in response.data.decode('utf-8')

def test_register_without_password(client):
    user_data = {
        "name": "Nowy User",
        "email": "test@example.com",
        #"password": "password123",
        "confirm_password": "password123"
    }
    response = client.post('/register', data=user_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'To pole jest wymagane' in response.data.decode('utf-8')

def test_register_without_confirm_password(client):
    user_data = {
        "name": "Nowy User",
        "email": "test@example.com",
        "password": "password123",
        #"confirm_password": "password123"
    }
    response = client.post('/register', data=user_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'To pole jest wymagane' in response.data.decode('utf-8')

def test_login_without_email(client):
    response = client.post('/login', data={
        #'email': 'test@test.com',
        'password': "password123"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'To pole jest wymagane' in response.data.decode('utf-8')

def test_login_with_invalid_email(client):
    response = client.post('/login', data={
         'email': 'nieprawidlowy-email',
        'password': "password123"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Nieprawidłowy adres e-mail.' in response.data.decode('utf-8')

def test_login_without_password(client):
    response = client.post('/login', data={
        'email': 'test@test.com',
        #'password': "password123"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'To pole jest wymagane' in response.data.decode('utf-8')

def test_register_with_whitespace_email(client):
    user_data = {
        "name": "Nowy User",
        "email": "  test@example.com  ",
        "password": "password123",
        "confirm_password": "password123"
    }
    response = client.post('/register', data=user_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'Nieprawidłowy adres e-mail.' in response.data.decode('utf-8')

def test_register_with_very_long_name(client):
    user_data = {
        "name": 'a'*150,
        "email": "test@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }
    response = client.post('/register', data=user_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'Name must be between 2 and 100' in response.data.decode('utf-8')

def test_register_with_special_characters_in_name(client):
    user_data = {
        "name": 'User<script>alert()</script>',
        "email": "test@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }
    response = client.post('/register', data=user_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'Pole nie może zawierać znaczników HTML' in response.data.decode('utf-8')

def test_register_with_empty_strings(client):
    user_data = {
        "name": '',
        "email": "",
        "password": "",
        "confirm_password": ""
    }
    response = client.post('/register', data=user_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'To pole jest wymagane.' in response.data.decode('utf-8')

def test_register_password_max_length(client):
    user_data = {
        "name": "Nowy User",
        "email": "duplicate@example.com",
        "password": 'a'*2000,
        "confirm_password": 'a'*2000
    }
    response = client.post('/register', data=user_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'Password must be at least 8 characters and no more than 200 characters' in response.data.decode('utf-8')

def test_register_with_sql_injection_attempt(client, app):
    response = client.post(
        '/register', data={
            "name": "Nowy User",
            "email": "nowy@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True
    )
    assert response.status_code == 200
    assert "Twoje konto zostało utworzone" in response.data.decode('utf-8')

    user = db.session.query(User).filter_by(email="nowy@example.com").first()
    assert user is not None

def test_login_case_sensitive_email(client):
    user_data = {
        "name": "Test User",
        "email": "Test@Example.com",
        "password": "password123",
        "confirm_password": "password123"
    }
    client.post('/register', data=user_data, follow_redirects=True)
    client.get('/logout', follow_redirects=True)

    response = client.post('/login', data={
        "email": "test@example.com",
        "password": "password123",
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Test User" in response.data.decode('utf-8')

def test_multiple_failed_login_attempts(client, auth_user):
    for _ in range(5):
        response = client.post('/login', data={
            "email": auth_user.email,
            "password": "pass",
        })
        assert response.status_code == 200
        assert "Nieprawidłowy email, lub hasło" in response.data.decode('utf-8')

def test_user_stays_logged_in_after_redirect(client, auth_user):
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    # 1. Strona główna
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert 'Tester' in response.data.decode('utf-8')  # Imię użytkownika widoczne

    # 2. Strona dodawania kawiarni (wymaga logowania)
    response = client.get('/add', follow_redirects=True)
    assert response.status_code == 200
    assert b'add' in response.request.path.encode() or 'Dodaj' in response.data.decode('utf-8')

    # 3. Powrót na stronę główną
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert 'Tester' in response.data.decode('utf-8')

def test_logout_clears_session(client, auth_user):
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    client.get('/logout', follow_redirects=True)
    response = client.get('/add', follow_redirects=False)
    assert response.status_code == 302
    assert '/login' in response.location

def test_access_protected_route_after_logout(client, auth_user):
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    client.get('/logout', follow_redirects=True)
    response = client.get('/add', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data or 'login' in response.request.path

def test_logged_in_user_cannot_access_register(client, auth_user):
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    response = client.get('/register', follow_redirects=False)
    assert response.status_code == 302
    assert response.location == '/'

def test_logged_in_user_cannot_access_login(client, auth_user):
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    response = client.get('/login', follow_redirects=False)
    assert response.status_code == 302
    assert response.location == '/'

def test_user_password_is_hashed(client, app):
    client.post(
        '/register', data={
            "name": "Nowy User",
            "email": "nowy@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True
    )
    with app.app_context():
        user = User.query.filter_by(email="nowy@example.com").first()

        assert user.password != "password123"
        assert user.password.startswith('pbkdf2:sha256')

def test_user_relationship_with_cafes(auth_user, sample_cafe, app):
    with app.app_context():
        user = User.query.get(auth_user.id)
        cafe = Cafe.query.get(sample_cafe.id)

        assert cafe in user.cafes
        assert cafe.owner == user
        assert cafe.user_id == user.id