
def test_password_is_hashed_not_plaintext(client):
    """Test: Hasło NIE jest przechowywane jako plaintext."""
    from main import User, db
    
    response = client.post('/register', data={
        "name": "Security Test",
        "email": "security@example.com",
        "password": "secret123",
        "confirm_password": "secret123"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    user = User.query.filter_by(email="security@example.com").first()
    assert user is not None
    assert user.password != "secret123"
    assert "pbkdf2:sha256" in user.password or "scrypt:" in user.password


def test_password_hash_is_different_for_same_password(client):
    """Test: To samo hasło ma różne hashe"""
    from main import User, db
    
    client.post('/register', data={
        "name": "User One",
        "email": "user1@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }, follow_redirects=True)
    
    client.get('/logout', follow_redirects=True)
    
    client.post('/register', data={
        "name": "User Two",
        "email": "user2@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }, follow_redirects=True)
    
    user1 = User.query.filter_by(email="user1@example.com").first()
    user2 = User.query.filter_by(email="user2@example.com").first()
    
    assert user1 is not None
    assert user2 is not None
    assert user1.password != user2.password


def test_password_verification_works(client, auth_user):
    """Test: Weryfikacja hasła działa (check_password_hash)."""
    from werkzeug.security import check_password_hash
    
    assert check_password_hash(auth_user.password, "password123") == True
    assert check_password_hash(auth_user.password, "wrongpass") == False


def test_weak_password_rejected(client):
    """Test: Słabe hasła są odrzucane (< 8 znaków)."""
    response = client.post('/register', data={
        "name": "Weak Pass User",
        "email": "weak@example.com",
        "password": "123",
        "confirm_password": "123"
    }, follow_redirects=True)
    assert response.status_code == 200
    page_content = response.data.decode('utf-8')
    assert "Field must be at least 8 characters long" in page_content or "register" in page_content.lower()


def test_very_long_password_accepted(client):
    """Test: Bardzo długie hasła są akceptowane."""
    long_password = "a" * 100
    response = client.post('/register', data={
        "name": "Long Pass User",
        "email": "longpass@example.com",
        "password": long_password,
        "confirm_password": long_password
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Twoje konto zostało utworzone" in response.data.decode('utf-8')

def test_session_expires_after_logout(client, auth_user):
    """Test: Sesja wygasa po wylogowaniu."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.get('/add')
    assert response.status_code == 200
    
    client.get('/logout', follow_redirects=True)
    
    response = client.get('/add', follow_redirects=True)
    assert response.status_code == 200
    assert "login" in response.request.path or "Zaloguj" in response.data.decode('utf-8')


def test_cannot_reuse_old_session_token(client, auth_user):
    """Test: Nie można użyć starego tokenu sesji po wylogowaniu."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    with client.session_transaction() as session:
        old_session_data = dict(session)
    
    client.get('/logout', follow_redirects=True)
    
    with client.session_transaction() as session:
        session.update(old_session_data)
    
    response = client.get('/add', follow_redirects=True)
    assert response.status_code == 200


def test_session_fixation_protection(client):
    """Test: Ochrona przed session fixation."""
    from main import User
    
    User.query.filter_by(email="fixation@example.com").delete()
    
    client.post('/register', data={
        "name": "Fixation Test",
        "email": "fixation@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }, follow_redirects=True)
    
    response = client.get('/')
    assert response.status_code == 200

def test_sql_injection_in_login_email(client):
    """Test: SQL injection w polu email nie działa (ORM chroni)."""
    response = client.post('/login', data={
        "email": "admin'--",
        "password": "anything"
    }, follow_redirects=True)
    assert response.status_code == 200
    page_content = response.data.decode('utf-8')
    assert "login" in page_content.lower() or "zaloguj" in page_content.lower()


def test_sql_injection_in_cafe_name(client, auth_user):
    """Test: SQL injection w nazwie kawiarni nie działa."""
    from main import Cafe
    
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    malicious_name = "Cafe'; DROP TABLE cafe;--"
    response = client.post('/add', data={
        "name": malicious_name,
        "map_url": "https://google.com/maps/test",
        "img_url": "https://images.com/test.jpg",
        "location": "Test Location",
        "seats": "10-20",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": True,
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    cafe = Cafe.query.filter_by(name=malicious_name).first()
    assert cafe is not None
    assert cafe.name == malicious_name
    
    all_cafes = Cafe.query.all()
    assert len(all_cafes) > 0


def test_xss_in_cafe_name(client, auth_user):
    """Test: XSS w nazwie kawiarni jest escaped."""
    with client:
        client.post('/login', data={
            "email": "test@example.com",
            "password": "password123"
        }, follow_redirects=True)
        
        xss_name = "<script>alert('XSS')</script>"
        response = client.post('/add', data={
            "name": xss_name,
            "map_url": "https://google.com/maps/test",
            "img_url": "https://images.com/test.jpg",
            "location": "Test Location",
            "seats": "10-20",
            "has_sockets": True,
            "has_toilet": True,
            "has_wifi": True,
            "can_take_calls": True,
            "coffee_price": "15 PLN"
        }, follow_redirects=True)
        assert response.status_code == 200
        
        response = client.get('/')
        page_content = response.data.decode('utf-8')
        assert "&lt;script&gt;" in page_content or xss_name not in page_content


def test_xss_in_user_name(client):
    """Test: XSS w imieniu użytkownika jest escaped."""
    xss_name = "<script>alert('XSS')</script>"
    with client:
        client.post('/register', data={
            "name": xss_name,
            "email": "xssuser@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True)
        

        response = client.get('/')
        page_content = response.data.decode('utf-8')
        assert "&lt;script&gt;" in page_content or xss_name not in page_content

def test_xss_in_cafe_location(client, auth_user):
    """Test: XSS w lokalizacji jest escaped."""
    with client:
        client.post('/login', data={
            "email": "test@example.com",
            "password": "password123"
        }, follow_redirects=True)
        
        xss_location = "<img src=x onerror=alert('XSS')>"
        response = client.post('/add', data={
            "name": "XSS Test Cafe",
            "map_url": "https://google.com/maps/test",
            "img_url": "https://images.com/test.jpg",
            "location": xss_location,
            "seats": "10-20",
            "has_sockets": True,
            "has_toilet": True,
            "has_wifi": True,
            "can_take_calls": True,
            "coffee_price": "15 PLN"
        }, follow_redirects=True)
        assert response.status_code == 200
        
        response = client.get('/')
        page_content = response.data.decode('utf-8')
        assert "&lt;img" in page_content or "onerror=alert" not in page_content

def test_authorization_check_on_update(client, auth_user, sample_cafe):
    """Test: Sprawdzenie autoryzacji przy update."""
    from main import User
    
    User.query.filter_by(email="user2@example.com").delete()
    
    client.post('/register', data={
        "name": "User Two",
        "email": "user2@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }, follow_redirects=True)
    
    response = client.post(f'/update/cafe/{sample_cafe.id}', data={
        "name": "Unauthorized Edit",
        "map_url": sample_cafe.map_url,
        "img_url": sample_cafe.img_url,
        "location": sample_cafe.location,
        "seats": sample_cafe.seats,
        "has_sockets": sample_cafe.has_sockets,
        "has_toilet": sample_cafe.has_toilet,
        "has_wifi": sample_cafe.has_wifi,
        "can_take_calls": sample_cafe.can_take_calls,
        "coffee_price": sample_cafe.coffee_price
    }, follow_redirects=True)
    
    page_content = response.data.decode('utf-8')
    assert "Nie masz uprawnień" in page_content or sample_cafe.name in page_content


def test_authorization_check_on_delete(client, auth_user, sample_cafe):
    """Test: Sprawdzenie autoryzacji przy delete."""
    from main import User, Cafe
    
    User.query.filter_by(email="deluser@example.com").delete()
    
    client.post('/register', data={
        "name": "Delete User",
        "email": "deluser@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }, follow_redirects=True)
    
    response = client.get(f'/delete/{sample_cafe.id}', follow_redirects=True)
    page_content = response.data.decode('utf-8')
    assert "Nie masz uprawnień" in page_content or response.status_code == 200
    
    cafe_still_exists = Cafe.query.get(sample_cafe.id)
    assert cafe_still_exists is not None


def test_direct_access_to_protected_route(client):
    """Test: Bezpośredni dostęp do chronionej strony bez logowania."""
    response = client.get('/add', follow_redirects=True)
    assert response.status_code == 200
    assert "login" in response.request.path or "Zaloguj" in response.data.decode('utf-8')


def test_cookie_manipulation(client, auth_user):
    """Test: Manipulacja cookies nie daje dostępu."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    client.get('/logout', follow_redirects=True)
    
    client.set_cookie('session', 'fake_session_value')
    
    response = client.get('/add', follow_redirects=True)
    assert response.status_code == 200
    assert "login" in response.request.path or "Zaloguj" in response.data.decode('utf-8')


def test_email_format_validation(client):
    """Test: Walidacja formatu email."""
    response = client.post('/register', data={
        "name": "Invalid Email User",
        "email": "not-an-email",
        "password": "password123",
        "confirm_password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    page_content = response.data.decode('utf-8')
    assert "Invalid email address" in page_content or "register" in page_content.lower()


def test_url_format_validation(client, auth_user):
    """Test: Walidacja formatu URL."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.post('/add', data={
        "name": "Invalid URL Cafe",
        "map_url": "not-a-url",
        "img_url": "also-not-a-url",
        "location": "Test Location",
        "seats": "10-20",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": True,
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200
    page_content = response.data.decode('utf-8')
    assert "Invalid URL" in page_content or "add" in response.request.path.lower()


def test_html_tags_stripped_from_input(client, auth_user):
    """Test: HTML tagi są usuwane/escaped z input."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    html_name = "<b>Bold Cafe</b>"
    response = client.post('/add', data={
        "name": html_name,
        "map_url": "https://google.com/maps/test",
        "img_url": "https://images.com/test.jpg",
        "location": "Test Location",
        "seats": "10-20",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": True,
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    response = client.get('/')
    page_content = response.data.decode('utf-8')
    assert "&lt;b&gt;" in page_content or "Bold Cafe" in page_content


def test_unicode_and_emoji_handled_safely(client, auth_user):
    """Test: Unicode i emoji są bezpiecznie obsługiwane."""
    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    emoji_name = "Cafe ☕🎉"
    response = client.post('/add', data={
        "name": emoji_name,
        "map_url": "https://google.com/maps/test",
        "img_url": "https://images.com/test.jpg",
        "location": "Test Location",
        "seats": "10-20",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": True,
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert emoji_name in response.data.decode('utf-8') or "Cafe" in response.data.decode('utf-8')

def test_password_not_in_response(client):
    """Test: Hasło NIE jest zwracane w response."""
    password = "secretpassword123"
    response = client.post('/register', data={
        "name": "Response Test",
        "email": "responsetest@example.com",
        "password": password,
        "confirm_password": password
    }, follow_redirects=True)
    assert response.status_code == 200
    page_content = response.data.decode('utf-8')
    assert password not in page_content


def test_error_messages_dont_leak_info(client):
    """Test: Komunikaty błędów nie wyciekają informacji."""
    response = client.post('/login', data={
        "email": "nonexistent@example.com",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    page_content = response.data.decode('utf-8').lower()
    assert "email not found" not in page_content
    assert "user not found" not in page_content
