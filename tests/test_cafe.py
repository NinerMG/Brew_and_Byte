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


# Błędne URL-e: Sprawdź, czy formularz CafeForm
# odrzuci map_url, który nie zaczyna się od http lub https.

# Edycja kawiarni (update_cafe): Sprawdź, czy po zmianie
# nazwy kawiarni w formularzu i wysłaniu POST, nazwa w bazie danych faktycznie się zmieniła.

# Brak kawiarni: Co się stanie, gdy użytkownik spróbuje wejść na /update/cafe/9999?
# Powinieneś otrzymać błąd 404.

#Zmiana języka: Przetestuj endpoint /set-language/en. Sprawdź, czy po zmianie
# w sesji znajduje się 'language': 'en' i czy napisy na stronie (np. w formularzu)
# faktycznie się zmieniają.

#Test unikalności nazwy: W modelu Cafe masz unique=True.
# Co się stanie, gdy spróbujesz dodać kawiarnię o nazwie, która już istnieje?
# Powinieneś sprawdzić, czy aplikacja obsłuży IntegrityError lub czy walidator WTForms to wyłapie.

# Test pustych pól: Spróbuj wysłać formularz dodawania z samymi spacjami lub pustymi polami,
# które są oznaczone jako DataRequired().

# Test formatu obrazka/URL: Co jeśli użytkownik poda w img_url ciąg znaków, który nie jest linkiem?
# Twoje testy powinny potwierdzić, że walidator URL() działa.

# Test wygaśnięcia sesji: Sprawdź, czy po wejściu na /logout,
# próba wejścia na /add kończy się przekierowaniem do logowania.

# Test transakcyjności: Sprawdź, czy jeśli podczas dodawania kawiarni wystąpi błąd bazy danych
# (np. symulowany db.session.rollback()), kawiarnia na pewno nie zostanie zapisana.

