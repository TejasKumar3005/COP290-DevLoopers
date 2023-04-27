# import requests
# from urllib.parse import urlencode
# import json
import pytest
from app import app

# ENDPOINT = "http://127.0.0.1:5000"
# response = requests.get(ENDPOINT)

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_home_page_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    pass

def test_user_register(client):
    
    data = {
        "username" : "ether",
        "firstname" : "Payas",
        "lastname" : "Khurana",
        "age" : "19",
        "height" : "185",
        "weight" : "75",
        "password" : "12345",
        "email" : "payaskhurana@gmail.com",
        "confirmation" : "12345",
    }

    form_data = '&'.join([f'{key}={value}' for key, value in data.items()])

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = client.post("/register", data=form_data, headers=headers,follow_redirects=True)
    
    assert(response.status_code == 200)
    pass

def test_user_login(client):
    data = {
        "username" : "Santhosh",
        "password" : "1234",
    }

    form_data = '&'.join([f'{key}={value}' for key, value in data.items()])

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = client.post("/login", data=form_data, headers=headers,follow_redirects=True)
    
    assert(response.status_code == 200)
    pass

def test_store_page_endpoint(client):
    response = client.get("/store")
    assert response.status_code == 200
    pass

def test_product_page_endpoint(client):
    with client.session_transaction() as session:
        session['user_id'] = 1
    response = client.get("/product/3")
    assert response.status_code == 200
    pass

def test_product_search(client):
    data = {
        "submit" : "search",
        "inputtext" : "all",
    }

    form_data = '&'.join([f'{key}={value}' for key, value in data.items()])

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response =  client.post("/store", data=form_data, headers=headers)
    
    assert(response.status_code == 200)
    pass

def test_product_apply(client):
    data = {
        "submit" : "apply",
        "category" : "A",
        "rating" : "4"
    }

    form_data = '&'.join([f'{key}={value}' for key, value in data.items()])

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = client.post("/store", data=form_data, headers=headers)
    
    assert(response.status_code == 200)
    pass

def test_product_reset(client):
    data = {
        "submit" : "reset",
    }

    form_data = '&'.join([f'{key}={value}' for key, value in data.items()])

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = client.post("/store", data=form_data, headers=headers)
    
    assert(response.status_code == 200)
    pass

def test_user_page(client) : 
    with client.session_transaction() as session:
        session['user_id'] = 1
    response = client.get("/user")
    assert response.status_code == 200
    pass

def test_profile_page(client) : 
    with client.session_transaction() as session:
        session['user_id'] = 1
    response = client.get("/profile")
    assert response.status_code == 200
    pass

def test_order_history_page(client) : 
    with client.session_transaction() as session:
        session['user_id'] = 1
    response = client.get("/order-history")
    assert response.status_code == 200
    pass

def test_community_page(client) : 
    with client.session_transaction() as session:
        session['user_id'] = 1
    response = client.get("/community")
    assert response.status_code == 200
    pass