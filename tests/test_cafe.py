def test_login_add_cafe(client, auth_user):
    client.post('/login',data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)

    response = client.post('/add', data={
        "name": "Testowa Kawiarnia",
        "location": "Warszawa",
        "map_url": "https://maps.google.com/test",
        "img_url": "https://images.com/test.jpg",
        "seats": "10-20",
        "coffee_price": "15 PLN",
        "has_wifi": True,
        "has_sockets": True,
        "has_toilet": True,
        "can_take_calls": False
    }, follow_redirects=True)

    assert "Kawiarnia dodana pomyślnie" in response.data.decode('utf-8')
    assert b"Testowa Kawiarnia" in response.data

def test_delete_cafe_requires_login(client):
    response = client.get('/delete/1')
    assert response.status_code == 302
    assert '/login' in response.location

def test_delete_cafe(client, auth_user, sample_cafe):
    client.get(f'/delete/{sample_cafe.id}', follow_redirects=True)

    client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)

    response = client.get(f'/delete/{sample_cafe.id}', follow_redirects=True)

    assert response.status_code == 200
    assert "Kawiarnia usunięta!" in response.get_data(as_text=True)