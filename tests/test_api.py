def test_invalid_date_input(client):
    response = client.post("/api/weather/", json={"city": "New York", "date": "pleb"})
    assert response.status_code == 422
    assert "Input should be a valid date or datetime" in response.text

def test_valid_date_input(client, use_stub_data):
    response = client.post("/api/weather/", json={"city": "New York", "date": "2023-02-25"})
    assert response.status_code == 200
    assert "Weather data stored successfully" in response.text

def test_post_weather(client, use_stub_data):
    response = client.post("/api/weather/", json={"city": "New York", "date": "2023-08-15"})
    
    assert response.status_code == 200
    assert response.json() == {
        'city': 'New York',
        'date': '2023-08-15',
        'message': 'Weather data stored successfully',
        'status': 'success'
    }

    response = client.get("/api/weather/?city=New York&date=2023-08-15")
    assert response.json() == {
        "city": "New York",
        "date": "2023-08-15",
        "min_temp": 20.05,
        "max_temp": 51.93,
        "average_temp": 35.99,
        "humidity": 76.38
    }

def test_already_requested_weather(client, use_stub_data):
    response = client.post("/api/weather/", json={"city": "New York", "date": "2023-08-15"})
    
    assert response.status_code == 200
    assert response.json() == {
        'city': 'New York',
        'date': '2023-08-15',
        'message': 'Weather data stored successfully',
        'status': 'success'
    }

    response = client.post("/api/weather/", json={"city": "New York", "date": "2023-08-15"})
    
    assert response.status_code == 200
    assert response.json() == {
        'city': 'New York',
        'date': '2023-08-15',
        'message': 'Weather data already exists.',
        'status': 'already_exists'
    }


def test_get_weather(client):
    response = client.get("/api/weather/?city=New York&date=1990-08-10")
    assert response.status_code == 404
    assert "Weather data not found for New York on 1990-08-10" in response.text
