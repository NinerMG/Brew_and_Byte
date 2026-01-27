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
    """Test: Puste stringi zamiast braku pól."""
    # TODO: POST z name='', email='', password=''
    # TODO: Assert błędy walidacji
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


def test_register_with_sql_injection_attempt(client):
    """Test: Próba SQL injection w email."""
    # TODO: POST z email="admin'--"
    # TODO: Assert że ORM chroni (nie ma błędu SQL)
    pass


# ==========================================
# LOGOWANIE - Dodatkowe testy
# ==========================================

def test_login_without_email(client):
    """Test: Logowanie bez email."""
    # TODO: POST /login z password='...' ale bez email
    # TODO: Assert błąd walidacji
    pass


def test_login_without_password(client, auth_user):
    """Test: Logowanie bez hasła."""
    # TODO: POST z email ale bez password
    # TODO: Assert błąd walidacji
    pass


def test_login_with_invalid_email_format(client):
    """Test: Format email nieprawidłowy przy logowaniu."""
    # TODO: POST z email='not-an-email'
    # TODO: Assert błąd walidacji
    pass


def test_login_case_sensitive_email(client):
    """Test: Czy email jest case-insensitive."""
    # TODO: Zarejestruj 'Test@Example.com'
    # TODO: Spróbuj zalogować z 'test@example.com'
    # TODO: Assert czy działa (zależy od implementacji)
    pass


def test_login_with_remember_me(client, auth_user):
    """Test: Checkbox 'Remember Me' działa."""
    # TODO: POST /login z remember=True
    # TODO: Assert że sesja jest 'permanent' (sprawdź cookie)
    pass


def test_multiple_failed_login_attempts(client, auth_user):
    """Test: Wiele błędnych prób logowania."""
    # TODO: 5x POST z błędnym hasłem
    # TODO: Assert że komunikat błędu jest każdorazowo
    # TODO: (Opcjonalnie: rate limiting test)
    pass


# ==========================================
# SESJA UŻYTKOWNIKA
# ==========================================

def test_user_stays_logged_in_after_redirect(client, auth_user):
    """Test: Użytkownik pozostaje zalogowany po przekierowaniu."""
    # TODO: Zaloguj
    # TODO: GET różne strony (/add, /)
    # TODO: Assert że current_user jest nadal zalogowany
    pass


def test_logout_clears_session(client, auth_user):
    """Test: Wylogowanie czyści sesję."""
    # TODO: Zaloguj
    # TODO: GET /logout
    # TODO: Spróbuj GET /add
    # TODO: Assert przekierowanie do login
    pass


def test_access_protected_route_after_logout(client, auth_user):
    """Test: Brak dostępu do chronionych stron po wylogowaniu."""
    # TODO: Zaloguj, dodaj kawiarnię, wyloguj
    # TODO: Spróbuj GET /add
    # TODO: Assert redirect do /login
    pass


def test_logged_in_user_cannot_access_register(client, auth_user):
    """Test: Zalogowany użytkownik nie może wejść na /register."""
    # TODO: Zaloguj
    # TODO: GET /register
    # TODO: Assert redirect do home
    pass


def test_logged_in_user_cannot_access_login(client, auth_user):
    """Test: Zalogowany użytkownik nie może wejść na /login."""
    # TODO: Zaloguj
    # TODO: GET /login
    # TODO: Assert redirect do home
    pass


# ==========================================
# USER MODEL & DATABASE
# ==========================================

def test_user_password_is_hashed(client):
    """Test: Hasło jest zahashowane w bazie, nie plaintext."""
    # TODO: Zarejestruj użytkownika z password='testpass123'
    # TODO: Pobierz użytkownika z bazy
    # TODO: Assert że user.password != 'testpass123'
    # TODO: Assert że user.password.startswith('pbkdf2:sha256')
    pass


def test_user_model_string_representation(auth_user):
    """Test: __repr__ lub __str__ modelu User."""
    # TODO: user_str = str(auth_user)
    # TODO: Assert że zawiera email lub name
    pass


def test_user_relationship_with_cafes(auth_user, sample_cafe):
    """Test: Relacja User ↔ Cafe działa."""
    # TODO: Assert że auth_user.cafes zawiera sample_cafe
    # TODO: Assert że sample_cafe.owner == auth_user
    pass


def test_duplicate_email_database_constraint():
    """Test: Constraint unique na email działa na poziomie bazy."""
    # TODO: Dodaj 2 userów z tym samym emailem bezpośrednio do bazy
    # TODO: Assert IntegrityError
    pass


# ==========================================
# PRZEKIEROWANIA I FLOW
# ==========================================

def test_redirect_to_login_on_delete(client):
    """Test: /delete wymaga logowania."""
    # TODO: GET /delete/1 bez logowania
    # TODO: Assert redirect do /login
    pass


def test_redirect_after_login_goes_to_home(client, auth_user):
    """Test: Po zalogowaniu przekierowanie do home."""
    # TODO: POST /login
    # TODO: Assert że jesteś na home (/)
    pass


def test_redirect_after_register_goes_to_home(client):
    """Test: Po rejestracji przekierowanie do home."""
    # TODO: POST /register
    # TODO: Assert redirect do home
    pass


def test_next_parameter_after_login(client, auth_user):
    """Test: Parametr ?next=/add przekierowuje po loginie."""
    # TODO: GET /add (niezalogowany) → redirect do /login?next=/add
    # TODO: Zaloguj się
    # TODO: Assert że jesteś na /add
    pass


# ==========================================
# FLASH MESSAGES
# ==========================================

def test_flash_message_on_successful_register(client):
    """Test: Flash message po rejestracji."""
    # TODO: POST /register
    # TODO: Assert 'Twoje konto zostało utworzone' in response
    pass


def test_flash_message_on_successful_login(client, auth_user):
    """Test: Flash message po logowaniu."""
    # TODO: POST /login
    # TODO: Assert 'Witaj ponownie' in response
    pass


def test_flash_message_on_logout(client, auth_user):
    """Test: Flash message po wylogowaniu."""
    # TODO: Zaloguj, wyloguj
    # TODO: Assert 'Zostałeś wylogowany' in response
    pass


def test_flash_message_on_duplicate_email(client):
    """Test: Flash message przy duplikacie email."""
    # TODO: Zarejestruj raz
    # TODO: Spróbuj drugi raz
    # TODO: Assert 'Ten adres email jest już zarejestrowany' in response
    pass


# ==========================================
# SECURITY
# ==========================================

def test_xss_in_user_name(client):
    """Test: XSS protection w imieniu użytkownika."""
    # TODO: Zarejestruj z name='<script>alert("XSS")</script>'
    # TODO: Zaloguj i sprawdź wyświetlanie
    # TODO: Assert że <script> jest escaped (Jinja2 chroni)
    pass


def test_password_hash_different_for_same_password(client):
    """Test: Ten sam password ma różne hashe (salt działa)."""
    # TODO: Zarejestruj user1 z password='test123'
    # TODO: Zarejestruj user2 z password='test123'
    # TODO: Assert że user1.password != user2.password (różne sale)
    pass


# ==========================================
# EDGE CASES
# ==========================================

def test_register_with_unicode_emoji_name(client):
    """Test: Emoji w imieniu użytkownika."""
    # TODO: POST z name='User 😀🎉'
    # TODO: Assert że działa poprawnie
    pass


def test_very_long_email(client):
    """Test: Bardzo długi email."""
    # TODO: POST z email='a'*100 + '@example.com'
    # TODO: Assert błąd walidacji (max 100 znaków)
    pass
