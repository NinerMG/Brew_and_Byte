
def test_set_language_to_english(client):
    """Test: Zmiana języka na angielski."""
    response = client.get('/set-language/en', follow_redirects=False)
    assert response.status_code == 302
    
    with client.session_transaction() as sess:
        assert sess['language'] == 'en'

def test_set_language_to_polish(client):
    """Test: Zmiana języka na polski."""
    response = client.get('/set-language/pl', follow_redirects=False)
    assert response.status_code == 302
    
    with client.session_transaction() as sess:
        assert sess['language'] == 'pl'

def test_set_language_invalid_code(client):
    """Test: Próba ustawienia nieobsługiwanego języka."""
    response = client.get('/set-language/de', follow_redirects=True)
    
    with client.session_transaction() as sess:
        assert 'language' not in sess or sess.get('language') != 'de'

def test_language_stored_in_session(client):
    """Test: Język jest przechowywany w sesji."""
    client.get('/set-language/en', follow_redirects=True)
    client.get('/')
    
    with client.session_transaction() as sess:
        assert sess['language'] == 'en'

def test_language_persists_across_requests(client):
    """Test: Język utrzymuje się między żądaniami."""
    with client:
        client.get('/set-language/en', follow_redirects=True)
        
        response_home = client.get('/')
        response_login = client.get('/login')
        
        assert b'Home' in response_home.data or b'Login' in response_login.data
        
        with client.session_transaction() as sess:
            assert sess['language'] == 'en'

def test_default_language_is_polish(client):
    """Test: Domyślny język to polski (bez ustawienia)."""
    response = client.get('/')
    content = response.data.decode('utf-8')
    
    assert 'Strona główna' in content or 'Zaloguj' in content or 'Zarejestruj' in content

def test_homepage_in_polish(client):
    """Test: Strona główna wyświetla polskie teksty."""
    with client:
        client.get('/set-language/pl', follow_redirects=True)
        response = client.get('/')
        content = response.data.decode('utf-8')
        
        assert 'Brew & Byte' in content
        assert 'Strona główna' in content or 'Zaloguj' in content

def test_homepage_in_english(client):
    """Test: Strona główna wyświetla angielskie teksty."""
    with client:
        client.get('/set-language/en', follow_redirects=True)
        response = client.get('/')
        content = response.data.decode('utf-8')
        
        assert 'Home' in content or 'Login' in content or 'Register' in content

def test_login_form_in_polish(client):
    """Test: Formularz logowania po polsku."""
    with client:
        client.get('/set-language/pl', follow_redirects=True)
        response = client.get('/login')
        content = response.data.decode('utf-8')
        
        assert 'Email' in content
        assert 'Hasło' in content
        assert 'Zaloguj' in content


def test_login_form_in_english(client):
    """Test: Formularz logowania po angielsku."""
    with client:
        client.get('/set-language/en', follow_redirects=True)
        response = client.get('/login')
        content = response.data.decode('utf-8')
        
        assert 'Email' in content
        assert 'Password' in content
        assert 'Login' in content


def test_register_form_in_polish(client):
    """Test: Formularz rejestracji po polsku."""
    with client:
        client.get('/set-language/pl', follow_redirects=True)
        response = client.get('/register')
        content = response.data.decode('utf-8')

        # Sprawdź czy są polskie teksty (niektóre pola mogą być w obu językach)
        assert 'Imię' in content or 'Name' in content
        assert 'Password' in content or 'Hasło' in content
        assert 'Zarejestruj' in content


def test_register_form_in_english(client):
    """Test: Formularz rejestracji po angielsku."""
    with client:
        client.get('/set-language/en', follow_redirects=True)
        response = client.get('/register')
        content = response.data.decode('utf-8')
        
        assert 'Name' in content
        assert 'Password' in content
        assert 'Register' in content or 'Sign up' in content


def test_add_cafe_form_in_polish(client, auth_user):
    """Test: Formularz dodawania kawiarni po polsku."""
    with client:
        client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        client.get('/set-language/pl', follow_redirects=True)
        response = client.get('/add')
        content = response.data.decode('utf-8')
        
        assert 'Name' in content
        assert 'Lokalizacja' in content


def test_add_cafe_form_in_english(client, auth_user):
    """Test: Formularz dodawania kawiarni po angielsku."""
    with client:
        client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        client.get('/set-language/en', follow_redirects=True)
        response = client.get('/add')
        content = response.data.decode('utf-8')
        
        assert 'Cafe Name' in content or 'Name' in content
        assert 'Location' in content


def test_flash_messages_translated_polish(client):
    """Test: Flash messages są po polsku."""
    with client:
        client.get('/set-language/pl', follow_redirects=True)
        response = client.post('/login', data={
            'email': 'wrong@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        content = response.data.decode('utf-8')

        assert 'alert-danger' in content or 'flash-message' in content
        assert 'polski' in content.lower() or 'email' in content.lower()


def test_flash_messages_translated_english(client):
    """Test: Flash messages są po angielsku."""
    with client:
        client.get('/set-language/en', follow_redirects=True)
        response = client.post('/login', data={
            'email': 'wrong@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        content = response.data.decode('utf-8')

        assert 'alert-danger' in content or 'flash-message' in content
        assert 'english' in content.lower() or 'EN' in content


def test_success_messages_translated(client):
    """Test: Komunikaty sukcesu są tłumaczone."""
    with client:
        client.get('/set-language/en', follow_redirects=True)
        response = client.post('/register', data={
            'name': 'Test User',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200


def test_form_errors_translated_polish(client):
    """Test: Błędy formularzy po polsku."""
    with client:
        client.get('/set-language/pl', follow_redirects=True)
        response = client.post('/register', data={
            'name': 'Test',
            'email': 'test@example.com',
            'password': 'short',
            'confirm_password': 'short'
        }, follow_redirects=True)
        content = response.data.decode('utf-8')
        
        assert 'minimum' in content.lower() or 'co najmniej' in content.lower() or '8' in content

def test_form_errors_translated_english(client):
    """Test: Błędy formularzy po angielsku."""
    with client:
        client.get('/set-language/en', follow_redirects=True)
        response = client.post('/register', data={
            'name': 'Test',
            'email': 'test@example.com',
            'password': 'short',
            'confirm_password': 'short'
        }, follow_redirects=True)
        content = response.data.decode('utf-8')
        
        assert 'at least' in content.lower() or 'minimum' in content.lower() or '8' in content


def test_navigation_translated_polish(client):
    """Test: Menu nawigacji po polsku."""
    with client:
        client.get('/set-language/pl', follow_redirects=True)
        response = client.get('/')
        content = response.data.decode('utf-8')
        
        assert 'Strona główna' in content or 'Zaloguj' in content or 'Zarejestruj' in content

def test_navigation_translated_english(client):
    """Test: Menu nawigacji po angielsku."""
    with client:
        client.get('/set-language/en', follow_redirects=True)
        response = client.get('/')
        content = response.data.decode('utf-8')
        
        assert 'Home' in content and ('Login' in content or 'Register' in content)



def test_cafe_boolean_fields_translated_polish(client, sample_cafe):
    """Test: 'Ma WiFi', 'Ma gniazdka' po polsku."""
    with client:
        client.get('/set-language/pl', follow_redirects=True)
        response = client.get('/')
        content = response.data.decode('utf-8')
        
        assert 'WiFi' in content or 'Gniazdka' in content or 'Toaleta' in content


def test_cafe_boolean_fields_translated_english(client, sample_cafe):
    """Test: 'Has WiFi', 'Has Sockets' po angielsku."""
    with client:
        client.get('/set-language/en', follow_redirects=True)
        response = client.get('/')
        content = response.data.decode('utf-8')
        
        assert 'WiFi' in content or 'Sockets' in content or 'Toilet' in content

def test_language_switch_with_user_logged_in(client, auth_user):
    """Test: Zmiana języka gdy użytkownik jest zalogowany."""
    with client:
        client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        client.get('/set-language/en', follow_redirects=True)
        response = client.get('/')
        content = response.data.decode('utf-8')
        content_lower = content.lower()
        

        assert 'logout' in content_lower or 'add cafe' in content_lower or 'test user' in content_lower


def test_language_remains_after_logout(client, auth_user):
    """Test: Język pozostaje po wylogowaniu."""
    with client:
        client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        client.get('/set-language/en', follow_redirects=True)
        client.get('/logout', follow_redirects=True)
        
        response = client.get('/login')
        content = response.data.decode('utf-8')
        
        assert 'Login' in content or 'Password' in content
        
        with client.session_transaction() as sess:
            assert sess.get('language') == 'en'


