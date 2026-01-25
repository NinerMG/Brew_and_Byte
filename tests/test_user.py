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