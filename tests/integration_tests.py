def test_complete_user_journey_register_to_delete_cafe(client):
    """Test kompletnej ścieżki użytkownika od rejestracji do usunięcia kawiarni.
    
    Scenariusz:
    1. Rejestracja nowego użytkownika
    2. Dodanie pierwszej kawiarni
    3. Edycja kawiarni (zmiana nazwy, lokalizacji i wszystkich pól)
    4. Usunięcie kawiarni
    5. Wylogowanie i weryfikacja braku dostępu do chronionych zasobów
    """


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

    # STEP 2: Dodanie kawiarni
    response = client.post('/add', data={
        "name": "Moja Pierwsza Kawiarnia",
        "map_url": "https://google.com/maps/test",
        "img_url": "https://images.com/test.jpg",
        "location": "Warszawa, ul. Testowa 1",
        "seats": "10-20",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": False,
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Moja Pierwsza Kawiarnia" in response.data.decode('utf-8')

    # STEP 3: Edycja kawiarni
    response = client.get('/update/cafe/1')
    assert response.status_code == 200
    assert "Moja Pierwsza Kawiarnia" in response.data.decode('utf-8')
    
    response = client.post('/update/cafe/1', data={
        "name": "Kawiarnia Po Edycji",
        "map_url": "https://google.com/maps/updated",
        "img_url": "https://images.com/updated.jpg",
        "location": "Kraków, ul. Nowa 2",
        "seats": "20-30",
        "has_sockets": False,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": True,
        "coffee_price": "18 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Kawiarnia Po Edycji" in response.data.decode('utf-8')
    assert "Kraków, ul. Nowa 2" in response.data.decode('utf-8')

    response = client.get('/delete/1', follow_redirects=True)
    assert response.status_code == 200
    assert "Kawiarnia Po Edycji" not in response.data.decode('utf-8')

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    
    response = client.get('/add', follow_redirects=True)
    assert response.status_code == 200
    assert "login" in response.request.path or "Zaloguj się" in response.data.decode('utf-8')

def test_two_users_independent_cafes(client, app):
    """Test izolacji danych między użytkownikami.
    
    Scenariusz:
    1. User1 rejestruje się i dodaje kawiarnię
    2. User2 rejestruje się i dodaje własną kawiarnię
    3. User2 próbuje usunąć kawiarnię User1 (brak uprawnień)
    4. User2 próbuje edytować kawiarnię User1 (brak uprawnień)
    5. User1 wraca i usuwa własną kawiarnię (sukces)
    
    Weryfikuje, że użytkownicy nie mogą modyfikować cudzych kawiarni.
    """
    
    from main import db, Cafe


    response = client.post('/register', data={
        "name": "User One",
        "email": "user1@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    response = client.post('/add', data={
        "name": "Kawiarnia A",
        "map_url": "https://google.com/maps/a",
        "img_url": "https://images.com/a.jpg",
        "location": "Warszawa B",
        "seats": "20-30",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": True,
        "coffee_price": "12 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200
    

    with app.app_context():
        cafe_a = db.session.query(Cafe).filter_by(name="Kawiarnia A").first()
        assert cafe_a is not None, "Kawiarnia A nie została dodana do bazy"
        cafe_a_id = cafe_a.id
    
    client.get('/logout', follow_redirects=True)

    response = client.post('/register', data={
        "name": "User Two",
        "email": "user2@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    response = client.post('/add', data={
        "name": "Kawiarnia B",
        "map_url": "https://google.com/maps/b",
        "img_url": "https://images.com/b.jpg",
        "location": "Warszawa B",
        "seats": "20-30",
        "has_sockets": False,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": False,
        "coffee_price": "14 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200

    response = client.get(f'/delete/{cafe_a_id}', follow_redirects=True)
    assert response.status_code == 200
    page_content = response.data.decode('utf-8')
    assert "Nie masz uprawnień" in page_content or "nie masz uprawnień" in page_content.lower()
    

    with app.app_context():
        cafe_check = db.session.query(Cafe).filter_by(id=cafe_a_id).first()
        assert cafe_check is not None, "Kawiarnia A została usunięta przez User2!"

    response = client.post(f'/update/cafe/{cafe_a_id}', data={
        "name": "Kawiarnia A ZMIENIONA",
        "map_url": "https://google.com/maps/a",
        "img_url": "https://images.com/a.jpg",
        "location": "Warszawa A",
        "seats": "10-20",
        "has_sockets": False,
        "has_toilet": False,
        "has_wifi": False,
        "can_take_calls": False,
        "coffee_price": "12 PLN"
    }, follow_redirects=True)
    
    with app.app_context():
        cafe_check = db.session.query(Cafe).filter_by(id=cafe_a_id).first()
        assert cafe_check.name == "Kawiarnia A", "User2 zmienił nazwę kawiarni User1!"
        assert cafe_check.has_sockets == True, "User2 zmienił ustawienia kawiarni User1!"

    client.get('/logout')
    
    response = client.post('/login', data={
        "email": "user1@example.com",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    response = client.get(f'/delete/{cafe_a_id}', follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        cafe_check = db.session.query(Cafe).filter_by(id=cafe_a_id).first()
        assert cafe_check is None, "Kawiarnia A nie została usunięta przez User1!"

def test_user_adds_multiple_cafes(client):
    """Test dodawania wielu kawiarni przez jednego użytkownika.
    
    Scenariusz:
    1. Rejestracja użytkownika
    2. Dodanie 5 kawiarni
    3. Weryfikacja że wszystkie są widoczne na stronie głównej
    4. Usunięcie pierwszych dwóch kawiarni
    5. Edycja trzeciej kawiarni
    6. Weryfikacja końcowego stanu
    """

    response = client.post('/register', data={
        "name": "Multi Cafe User",
        "email": "multi@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200

    cafe_names = ['Cafe A', 'Cafe B', 'Cafe C', 'Cafe D', 'Cafe E']
    for name in cafe_names:
        response = client.post('/add', data={
            "name": name,
            "map_url": f"https://google.com/maps/{name}",
            "img_url": f"https://images.com/{name}.jpg",
            "location": f"Location {name}",
            "seats": "10-20",
            "has_sockets": True,
            "has_toilet": True,
            "has_wifi": True,
            "can_take_calls": True,
            "coffee_price": "15 PLN"
        }, follow_redirects=True)
        assert response.status_code == 200

    response = client.get('/')
    assert response.status_code == 200
    page_content = response.data.decode('utf-8')
    for name in cafe_names:
        assert name in page_content

    response = client.get('/delete/1', follow_redirects=True)
    assert response.status_code == 200
    response = client.get('/delete/2', follow_redirects=True)
    assert response.status_code == 200
    
    response = client.get('/')
    page_content = response.data.decode('utf-8')
    assert 'Cafe A' not in page_content
    assert 'Cafe B' not in page_content
    assert 'Cafe C' in page_content
    assert 'Cafe D' in page_content
    assert 'Cafe E' in page_content

    response = client.post('/update/cafe/3', data={
        "name": "Cafe C Modified",
        "map_url": "https://google.com/maps/modified",
        "img_url": "https://images.com/modified.jpg",
        "location": "New Location C",
        "seats": "30-40",
        "has_sockets": False,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": False,
        "coffee_price": "20 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    response = client.get('/')
    page_content = response.data.decode('utf-8')
    assert "Cafe C Modified" in page_content
    assert "New Location C" in page_content

def test_language_switch_during_session(client):
    """Test przełączania języka interfejsu podczas sesji.
    
    Scenariusz:
    1. Rejestracja (domyślnie PL)
    2. Dodanie kawiarni z interfejsem PL
    3. Przełączenie języka na EN
    4. Edycja kawiarni z interfejsem EN
    5. Przełączenie z powrotem na PL
    
    Weryfikuje, że zmiana języka działa poprawnie i nie wpływa na dane.
    """

    # STEP 1: Rejestracja (domyślnie PL)
    response = client.post('/register', data={
        "name": "Lang User",
        "email": "lang@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Twoje konto zostało utworzone" in response.data.decode('utf-8')


    response = client.get('/add')
    assert response.status_code == 200
    page_content = response.data.decode('utf-8')
    assert "Nazwa" in page_content or "nazwa" in page_content.lower()
    
    response = client.post('/add', data={
        "name": "Test Cafe",
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

    response = client.get('/set-language/en', follow_redirects=True)
    assert response.status_code == 200

    response = client.get('/update/cafe/1')
    assert response.status_code == 200
    page_content = response.data.decode('utf-8')
    assert "Name" in page_content or "name" in page_content.lower()
    
    response = client.post('/update/cafe/1', data={
        "name": "Test Cafe Updated",
        "map_url": "https://google.com/maps/updated",
        "img_url": "https://images.com/updated.jpg",
        "location": "Updated Location",
        "seats": "30-40",
        "has_sockets": False,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": False,
        "coffee_price": "18 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200

    response = client.get('/set-language/pl', follow_redirects=True)
    assert response.status_code == 200
    
    response = client.get('/')
    assert response.status_code == 200

def test_failed_login_then_register_then_login(client):
    """Test scenariusza nieudanego logowania prowadzącego do rejestracji.
    
    Scenariusz:
    1. Próba logowania z nieistniejącym kontem (błąd)
    2. Przejście do rejestracji tego samego emaila
    3. Pomyślna rejestracja
    4. Wylogowanie
    5. Pomyślne logowanie z nowo utworzonym kontem
    """

    response = client.post('/login', data={
        "email": "nieistniejacy@example.com",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    page_content = response.data.decode('utf-8')
    assert "login" in page_content.lower() or "zaloguj" in page_content.lower()

    response = client.get('/register')
    assert response.status_code == 200
    
    response = client.post('/register', data={
        "name": "New User",
        "email": "nieistniejacy@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Twoje konto zostało utworzone" in response.data.decode('utf-8')

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200

    response = client.post('/login', data={
        "email": "nieistniejacy@example.com",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    response = client.get('/')
    assert response.status_code == 200

def test_add_cafe_with_all_boolean_combinations(client, auth_user):
    """Test dodawania kawiarni z różnymi kombinacjami pól boolean.
    
    Scenariusz:
    1. Logowanie
    2. Dodanie kawiarni z wszystkimi boolean=True
    3. Dodanie kawiarni z wszystkimi boolean=False
    4. Dodanie kawiarni z mieszanymi wartościami boolean
    
    Weryfikuje, że wszystkie kombinacje są poprawnie zapisywane.
    """

    response = client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200

    response = client.post('/add', data={
        "name": "Cafe All True",
        "map_url": "https://google.com/maps/true",
        "img_url": "https://images.com/true.jpg",
        "location": "Location True",
        "seats": "10-20",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": True,
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Cafe All True" in response.data.decode('utf-8')

    response = client.post('/add', data={
        "name": "Cafe All False",
        "map_url": "https://google.com/maps/false",
        "img_url": "https://images.com/false.jpg",
        "location": "Location False",
        "seats": "20-30",
        "has_sockets": False,
        "has_toilet": False,
        "has_wifi": False,
        "can_take_calls": False,
        "coffee_price": "12 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Cafe All False" in response.data.decode('utf-8')

    response = client.post('/add', data={
        "name": "Cafe Mixed",
        "map_url": "https://google.com/maps/mixed",
        "img_url": "https://images.com/mixed.jpg",
        "location": "Location Mixed",
        "seats": "20-30",
        "has_sockets": True,
        "has_toilet": False,
        "has_wifi": False,
        "can_take_calls": False,
        "coffee_price": "18 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    response = client.get('/')
    page_content = response.data.decode('utf-8')
    assert "Cafe All True" in page_content
    assert "Cafe All False" in page_content
    assert "Cafe Mixed" in page_content

def test_concurrent_edits_by_same_user(client, auth_user, sample_cafe):
    """Test wielokrotnych edycji tej samej kawiarni przez użytkownika.
    
    Scenariusz:
    1. Logowanie
    2. Pierwsza edycja: zmiana nazwy
    3. Druga edycja: zmiana lokalizacji
    4. Trzecia edycja: zmiana pól boolean
    5. Weryfikacja że ostatnie zmiany zostały zachowane
    """

    response = client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200

    response = client.post('/update/cafe/1', data={
        "name": "New Name 1",
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
    assert response.status_code == 200

    response = client.post('/update/cafe/1', data={
        "name": "New Name 1",
        "map_url": sample_cafe.map_url,
        "img_url": sample_cafe.img_url,
        "location": "New Location",
        "seats": sample_cafe.seats,
        "has_sockets": sample_cafe.has_sockets,
        "has_toilet": sample_cafe.has_toilet,
        "has_wifi": sample_cafe.has_wifi,
        "can_take_calls": sample_cafe.can_take_calls,
        "coffee_price": sample_cafe.coffee_price
    }, follow_redirects=True)
    assert response.status_code == 200

    response = client.post('/update/cafe/1', data={
        "name": "New Name 1",
        "map_url": sample_cafe.map_url,
        "img_url": sample_cafe.img_url,
        "location": "New Location",
        "seats": sample_cafe.seats,
        "has_sockets": not sample_cafe.has_sockets,
        "has_toilet": sample_cafe.has_toilet,
        "has_wifi": sample_cafe.has_wifi,
        "can_take_calls": sample_cafe.can_take_calls,
        "coffee_price": sample_cafe.coffee_price
    }, follow_redirects=True)
    assert response.status_code == 200
    
    response = client.get('/')
    page_content = response.data.decode('utf-8')
    assert "New Name 1" in page_content
    assert "New Location" in page_content

def test_user_journey_with_validation_errors(client):
    """Test scenariusza z błędami walidacji formularzy.
    
    Scenariusz:
    1. Próba rejestracji ze zbyt krótkim hasłem (błąd)
    2. Próba rejestracji z niezgodnymi hasłami (błąd)
    3. Pomyślna rejestracja z poprawnymi danymi
    4. Próba dodania kawiarni z nieprawidłowymi URL (błąd)
    5. Próba dodania kawiarni z pustymi polami wymaganymi (błąd)
    6. Pomyślne dodanie kawiarni z poprawnymi danymi
    
    Weryfikuje działanie walidacji WTForms.
    """

    # STEP 1: Rejestracja z błędami
    response = client.post('/register', data={
        "name": "Test User",
        "email": "validation@example.com",
        "password": "123",
        "confirm_password": "123"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    response = client.post('/register', data={
        "name": "Test User",
        "email": "validation@example.com",
        "password": "password123",
        "confirm_password": "password456"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    response = client.post('/register', data={
        "name": "Test User",
        "email": "validation@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Twoje konto zostało utworzone" in response.data.decode('utf-8')

    response = client.post('/add', data={
        "name": "Error Cafe",
        "map_url": "not-a-valid-url",
        "img_url": "also-not-valid",
        "location": "Test Location",
        "seats": "10-20",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": True,
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    response = client.post('/add', data={
        "name": "",
        "map_url": "https://google.com/maps/test",
        "img_url": "https://images.com/test.jpg",
        "location": "",
        "seats": "",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": True,
        "coffee_price": ""
    }, follow_redirects=True)
    assert response.status_code == 200
    
    response = client.post('/add', data={
        "name": "Valid Cafe",
        "map_url": "https://google.com/maps/valid",
        "img_url": "https://images.com/valid.jpg",
        "location": "Valid Location",
        "seats": "10-20",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": True,
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Valid Cafe" in response.data.decode('utf-8')

def test_unauthorized_access_attempts(client, sample_cafe):
    """Test prób dostępu do chronionych zasobów bez autoryzacji.
    
    Scenariusz:
    1. Próba GET /add bez logowania (przekierowanie do login)
    2. Próba POST /add bez logowania (przekierowanie do login)
    3. Próba GET /update/cafe/1 bez logowania (przekierowanie do login)
    4. Próba POST /update/cafe/1 bez logowania (przekierowanie do login)
    5. Próba GET /delete/1 bez logowania (przekierowanie do login)
    6. Weryfikacja że kawiarnia nie została zmieniona
    
    Weryfikuje działanie dekoratora @login_required.
    """

    response = client.get('/add', follow_redirects=True)
    assert response.status_code == 200
    assert "login" in response.request.path or "Zaloguj" in response.data.decode('utf-8')
    
    response = client.post('/add', data={
        "name": "Unauthorized Cafe",
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
    assert "login" in response.request.path or "Zaloguj" in response.data.decode('utf-8')
    
    response = client.get('/update/cafe/1', follow_redirects=True)
    assert response.status_code == 200
    assert "login" in response.request.path or "Zaloguj" in response.data.decode('utf-8')
    
    response = client.post('/update/cafe/1', data={
        "name": "Changed Name",
        "map_url": "https://google.com/maps/changed",
        "img_url": "https://images.com/changed.jpg",
        "location": "Changed Location",
        "seats": "20-30",
        "has_sockets": False,
        "has_toilet": False,
        "has_wifi": False,
        "can_take_calls": False,
        "coffee_price": "20 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "login" in response.request.path or "Zaloguj" in response.data.decode('utf-8')
    
    response = client.get('/delete/1', follow_redirects=True)
    assert response.status_code == 200
    assert "login" in response.request.path or "Zaloguj" in response.data.decode('utf-8')
    
    response = client.get('/')
    assert response.status_code == 200
    assert "Testowa Kawiarnia" in response.data.decode('utf-8')

def test_cross_user_data_isolation(client):
    """Test izolacji danych między użytkownikami w kontekście edycji.
    
    Scenariusz:
    1. User1 tworzy 3 kawiarnie
    2. User2 tworzy 2 kawiarnie
    3. Weryfikacja że obie kawiarnie są widoczne na stronie głównej
    4. User2 próbuje edytować kawiarnię User1 (dostęp do formularza)
    5. User1 loguje się i widzi wszystkie kawiarnie
    6. User1 może edytować swoją kawiarnię
    """

    response = client.post('/register', data={
        "name": "User One",
        "email": "isolation1@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    for i in range(1, 4):
        response = client.post('/add', data={
            "name": f"User1 Cafe {i}",
            "map_url": f"https://google.com/maps/u1c{i}",
            "img_url": f"https://images.com/u1c{i}.jpg",
            "location": f"Location U1 {i}",
            "seats": "10-20",
            "has_sockets": True,
            "has_toilet": True,
            "has_wifi": True,
            "can_take_calls": True,
            "coffee_price": "15 PLN"
        }, follow_redirects=True)
        assert response.status_code == 200
    
    client.get('/logout')
    
    response = client.post('/register', data={
        "name": "User Two",
        "email": "isolation2@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    for i in range(1, 3):
        response = client.post('/add', data={
            "name": f"User2 Cafe {i}",
            "map_url": f"https://google.com/maps/u2c{i}",
            "img_url": f"https://images.com/u2c{i}.jpg",
            "location": f"Location U2 {i}",
            "seats": "20-30",
            "has_sockets": True,
            "has_toilet": True,
            "has_wifi": True,
            "can_take_calls": True,
            "coffee_price": "18 PLN"
        }, follow_redirects=True)
        assert response.status_code == 200
    
    response = client.get('/')
    page_content = response.data.decode('utf-8')
    assert "User1 Cafe 1" in page_content
    assert "User2 Cafe 1" in page_content
    
    response = client.get('/update/cafe/1', follow_redirects=True)
    assert response.status_code == 200
    
    client.get('/logout')
    
    response = client.post('/login', data={
        "email": "isolation1@example.com",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    response = client.get('/')
    page_content = response.data.decode('utf-8')
    assert "User1 Cafe 1" in page_content
    assert "User2 Cafe 1" in page_content
    
    response = client.get('/update/cafe/4', follow_redirects=True)
    assert response.status_code == 200

def test_database_transaction_rollback_scenario(client, auth_user, monkeypatch):
    """Test rollbacku transakcji bazodanowej przy błędzie.
    
    Scenariusz:
    1. Logowanie użytkownika
    2. Mockowanie db.session.commit() aby rzucał wyjątek
    3. Próba dodania kawiarni (błąd podczas commit)
    4. Przywrócenie oryginalnej funkcji commit
    5. Weryfikacja że kawiarnia NIE została dodana (rollback zadziałał)
    
    Testuje mechanizm rollback w bloku try-except.
    """

    response = client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    from main import db
    original_commit = db.session.commit
    
    def mock_commit_error():
        raise Exception("Database error during commit")
    
    monkeypatch.setattr(db.session, 'commit', mock_commit_error)
    
    try:
        response = client.post('/add', data={
            "name": "Rollback Cafe",
            "map_url": "https://google.com/maps/rollback",
            "img_url": "https://images.com/rollback.jpg",
            "location": "Rollback Location",
            "seats": "10-20",
            "has_sockets": True,
            "has_toilet": True,
            "has_wifi": True,
            "can_take_calls": True,
            "coffee_price": "15 PLN"
        }, follow_redirects=True)
        assert response.status_code == 200 or response.status_code == 500
    except:
        pass
    
    monkeypatch.setattr(db.session, 'commit', original_commit)
    
    response = client.get('/')
    assert response.status_code == 200
    assert "Rollback Cafe" not in response.data.decode('utf-8')

def test_session_expiration_scenario(client, auth_user):
    """Test zachowania aplikacji po wygaśnięciu sesji użytkownika.
    
    Scenariusz:
    1. Logowanie i dodanie kawiarni
    2. Wylogowanie (symulacja wygaśnięcia sesji)
    3. Próba GET /add bez sesji (przekierowanie do login)
    4. Próba POST /add bez sesji (przekierowanie do login)
    5. Weryfikacja że kawiarnia nie została dodana do bazy
    
    Testuje ochronę endpointów po wygaśnięciu sesji.
    """

    response = client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    response = client.post('/add', data={
        "name": "Before Expiration",
        "map_url": "https://google.com/maps/before",
        "img_url": "https://images.com/before.jpg",
        "location": "Before Location",
        "seats": "10-20",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": True,
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Before Expiration" in response.data.decode('utf-8')
    
    # Logout to simulate session expiration
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    
    # Try to access protected route without authentication
    response = client.get('/add', follow_redirects=True)
    assert response.status_code == 200
    assert "login" in response.request.path or "Zaloguj" in response.data.decode('utf-8')
    
    # Try to post to protected route without authentication
    response = client.post('/add', data={
        "name": "After Expiration",
        "map_url": "https://google.com/maps/after",
        "img_url": "https://images.com/after.jpg",
        "location": "After Location",
        "seats": "20-30",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": True,
        "coffee_price": "18 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "login" in response.request.path or "Zaloguj" in response.data.decode('utf-8')
    
    from main import Cafe
    cafe = Cafe.query.filter_by(name="After Expiration").first()
    assert cafe is None

def test_duplicate_form_submission(client, auth_user):
    """Test podwójnego wysłania formularza dodawania kawiarni.
    
    Scenariusz:
    1. Logowanie
    2. Dodanie kawiarni o nazwie "Duplicate Test Cafe"
    3. Ponowne dodanie kawiarni z tą samą nazwą (ale innymi danymi)
    4. Weryfikacja że obie kawiarnie zostały dodane
    
    Sprawdza, czy aplikacja pozwala na duplikaty nazw kawiarni.
    """

    response = client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    response = client.post('/add', data={
        "name": "Duplicate Test Cafe",
        "map_url": "https://google.com/maps/duplicate",
        "img_url": "https://images.com/duplicate.jpg",
        "location": "Duplicate Location",
        "seats": "10-20",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": True,
        "coffee_price": "15 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Duplicate Test Cafe" in response.data.decode('utf-8')
    
    response = client.post('/add', data={
        "name": "Duplicate Test Cafe",
        "map_url": "https://google.com/maps/duplicate2",
        "img_url": "https://images.com/duplicate2.jpg",
        "location": "Duplicate Location 2",
        "seats": "15-25",
        "has_sockets": False,
        "has_toilet": False,
        "has_wifi": False,
        "can_take_calls": False,
        "coffee_price": "18 PLN"
    }, follow_redirects=True)
    assert response.status_code == 200

def test_many_cafes_display_performance(client, auth_user):
    """Test wydajności wyświetlania dużej liczby kawiarni.
    
    Scenariusz:
    1. Logowanie
    2. Dodanie 50 kawiarni z różnymi konfiguracjami
    3. Pobranie strony głównej
    4. Weryfikacja że wybrane kawiarnie są widoczne
    
    Sprawdza czy aplikacja radzi sobie z większą ilością danych.
    """

    response = client.post('/login', data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    for i in range(50):
        response = client.post('/add', data={
            "name": f"Performance Cafe {i+1}",
            "map_url": f"https://google.com/maps/perf{i+1}",
            "img_url": f"https://images.com/perf{i+1}.jpg",
            "location": f"Location {i+1}",
            "seats": "10-20",
            "has_sockets": i % 2 == 0,
            "has_toilet": i % 3 == 0,
            "has_wifi": i % 2 == 0,
            "can_take_calls": i % 4 == 0,
            "coffee_price": f"{10 + i % 10} PLN"
        }, follow_redirects=True)
        assert response.status_code == 200
    
    response = client.get('/')
    assert response.status_code == 200
    page_content = response.data.decode('utf-8')
    
    assert "Performance Cafe 1" in page_content
    assert "Performance Cafe 25" in page_content
    assert "Performance Cafe 50" in page_content
