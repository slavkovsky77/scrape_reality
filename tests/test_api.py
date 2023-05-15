import pytest
from datetime import datetime
from app import create_app
from scrapper.db import Database, ScrappedFlat, FlatHistory


@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


@pytest.fixture(scope='module')
def init_database():
    db = Database()
    db.create()
    flat = ScrappedFlat(
        apartment_number='101A',
        title='Cozy Apartment',
        rooms='1+1',
        size='50m²',
        total_area_size='60m²',
        sales_price='1500000',
        floor_number='3/5',
        project_name='Green Park',
        href='https://example.com/flats/101A',
        img_src='https://example.com/flats/101A/image.jpg',
        status='available'
    )
    db.create_flat(flat)
    yield db


def test_get_flats(test_client, init_database):
    response = test_client.get('/api/flats')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['apartment_number'] == '101A'


def test_get_flat(test_client, init_database):
    response = test_client.get('/api/flats/101A')
    assert response.status_code == 200
    assert response.json['apartment_number'] == '101A'


def mock_create_flat(test_client, apartment_number):
    flat_dict = {
        'apartment_number': apartment_number,
        'title': 'Spacious Apartment',
        'rooms': '2+1',
        'size': '80m²',
        'total_area_size': '90m²',
        'sales_price': '2500000',
        'floor_number': '4/5',
        'project_name': 'Green Park',
        'href': 'https://example.com/flats/102B',
        'img_src': 'https://example.com/flats/102B/image.jpg',
        'status': 'available'
    }
    response = test_client.post('/api/flats/create_flat', json=flat_dict)
    return flat_dict, response


def test_create_flat(test_client, init_database):
    flat_dict, response = mock_create_flat(test_client, '102B')
    assert response.status_code == 201
    assert response.json == flat_dict


def test_update_flat(test_client, init_database):
    flat_dict = {
        'title': 'Updated Apartment',
        'rooms': '3+1',
        'size': '100m²',
        'total_area_size': '110m²',
        'sales_price': '3500000',
        'floor_number': '5/5',
        'project_name': 'Green Park',
        'href': 'https://example.com/flats/101A',
        'img_src': 'https://example.com/flats/101A/image.jpg',
        'status': 'sold'
    }
    response = test_client.put('/api/flats/101A', json=flat_dict)
    assert response.status_code == 200
    assert response.json is not None

    # Check if the flat was updated correctly
    updated_flat = init_database.get_flat('101A')
    assert updated_flat is not None
    assert updated_flat.title == 'Updated Apartment'
    assert updated_flat.rooms == '3+1'
    assert updated_flat.size == '100m²'
    assert updated_flat.total_area_size == '110m²'
    assert updated_flat.sales_price == '3500000'
    assert updated_flat.floor_number == '5/5'
    assert updated_flat.project_name == 'Green Park'
    assert updated_flat.href == 'https://example.com/flats/101A'
    assert updated_flat.img_src == 'https://example.com/flats/101A/image.jpg'
    assert updated_flat.status == 'sold'


def test_get_flat_history(test_client, init_database):
    flat_number = '101AB'
    flat_dict, response = mock_create_flat(test_client, '101AB')

    # Add some history for the flat
    history1 = FlatHistory(apartment_number=flat_number, sales_price='1000', timestamp=datetime.now())
    history2 = FlatHistory(apartment_number=flat_number, sales_price='2000', timestamp=datetime.now())
    init_database.session.add_all([history1, history2])
    init_database.session.commit()

    # Make API request to get the flat's history
    response = test_client.get(f'/api/flats/{flat_number}/history')

    # Check if the response is OK and if the history is correct
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['sales_price'] == '1000'
    assert response.json[1]['sales_price'] == '2000'
