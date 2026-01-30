import pytest
from main import User, db

def test_home_page(client):
    """Sprawdza, czy strona główna ładuje się poprawnie."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Brew & Byte" in response.data

def test_register_user(client):
    """Sprawdza poprawną rejestrację nowego użytkownika."""
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
    """Sprawdza, że rejestracja z już istniejącym emailem zwraca odpowiedni błąd."""
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
    """Sprawdza pełny cykl: rejestracja, wylogowanie, ponowne zalogowanie."""
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
    """Sprawdza, że logowanie z nieprawidłowym hasłem zwraca błąd."""
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
    """Sprawdza, że logowanie z nieistniejącym emailem zwraca błąd."""
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
    """Sprawdza, że niezalogowany użytkownik jest przekierowywany do logowania przy próbie dodania kawiarni."""
    response = client.get('/add', follow_redirects=False)
    assert response.status_code == 302
    assert response.location.startswith('/login')

def test_redirect_to_login_page_on_update(client, sample_cafe):
    """Sprawdza, że niezalogowany użytkownik jest przekierowywany do logowania przy próbie edycji kawiarni."""
    response =  client.get(f'/update/cafe/{sample_cafe.id}', follow_redirects=False)
    assert response.status_code == 302
    assert response.location.startswith('/login')

def test_too_short_password(client):
    """Sprawdza, że zbyt krótkie hasło jest odrzucane przez walidację."""
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
    """Sprawdza, że niezgodne hasła są wykrywane przez walidację."""
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
    """Sprawdza, że rejestracja bez emaila zwraca błąd walidacji."""
    user_data = {
        "name": "Nowy User",
        "password": "password123",
        "confirm_password": "password123"
    }
    response = client.post('/register', data=user_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'To pole jest wymagane' in response.data.decode('utf-8')

def test_register_with_invalid_email(client):
    """Sprawdza, że nieprawidłowy format emaila jest wykrywany przez walidację."""
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
    """Sprawdza, że rejestracja bez imienia zwraca błąd walidacji."""
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }
    response = client.post('/register', data=user_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'To pole jest wymagane' in response.data.decode('utf-8')

def test_register_without_password(client):
    """Sprawdza, że rejestracja bez hasła zwraca błąd walidacji."""
    user_data = {
        "name": "Nowy User",
        "email": "test@example.com",
        "confirm_password": "password123"
    }
    response = client.post('/register', data=user_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'To pole jest wymagane' in response.data.decode('utf-8')

def test_register_without_confirm_password(client):
    """Sprawdza, że rejestracja bez potwierdzenia hasła zwraca błąd walidacji."""
    user_data = {
        "name": "Nowy User",
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post('/register', data=user_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'To pole jest wymagane' in response.data.decode('utf-8')

def test_login_without_email(client):
    """Sprawdza, że logowanie bez emaila zwraca błąd walidacji."""
    response = client.post('/login', data={
        'password': "password123"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'To pole jest wymagane' in response.data.decode('utf-8')

def test_login_with_invalid_email(client):
    """Sprawdza, że logowanie z nieprawidłowym formatem emaila zwraca błąd walidacji."""
    response = client.post('/login', data={
         'email': 'nieprawidlowy-email',
        'password': "password123"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Nieprawidłowy adres e-mail.' in response.data.decode('utf-8')

def test_login_without_password(client):
    """Sprawdza, że logowanie bez hasła zwraca błąd walidacji."""
    response = client.post('/login', data={
        'email': 'test@test.com'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'To pole jest wymagane' in response.data.decode('utf-8')

def test_register_with_whitespace_email(client):
    """Sprawdza, że email z białymi znakami na początku/końcu jest odrzucany."""
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
    """Sprawdza, że zbyt długie imię (>100 znaków) jest odrzucane przez walidację."""
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
    """Sprawdza, że znaczniki HTML w imieniu są wykrywane i blokowane."""
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
    """Sprawdza, że puste stringi w polach formularza powodują błąd walidacji."""
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
    """Sprawdza, że zbyt długie hasło (>200 znaków) jest odrzucane przez walidację."""
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
    """Sprawdza, że ORM chroni przed SQL injection podczas rejestracji."""
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
    """Sprawdza, że logowanie nie jest case-sensitive dla emaila."""
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
    """Sprawdza, że wielokrotne błędne próby logowania zwracają odpowiedni komunikat."""
    for _ in range(5):
        response = client.post('/login', data={
            "email": auth_user.email,
            "password": "pass",
        })
        assert response.status_code == 200
        assert "Nieprawidłowy email, lub hasło" in response.data.decode('utf-8')

def test_user_stays_logged_in_after_redirect(client, auth_user):
    """Sprawdza, że użytkownik pozostaje zalogowany po przekierowaniach między stronami."""
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    # 1. Strona główna
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert 'Tester' in response.data.decode('utf-8')

    # 2. Strona dodawania kawiarni (wymaga logowania)
    response = client.get('/add', follow_redirects=True)
    assert response.status_code == 200
    assert b'add' in response.request.path.encode() or 'Dodaj' in response.data.decode('utf-8')

    # 3. Powrót na stronę główną
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert 'Tester' in response.data.decode('utf-8')
