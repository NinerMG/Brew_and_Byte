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
    assert 'Hasło musi mieć minimum 8 znaków' in response.data.decode('utf-8')

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