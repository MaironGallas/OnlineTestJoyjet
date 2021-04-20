import json

from django.test import Client
from django.urls import reverse
from pytest import fixture


@fixture
def payload_input_level1():
    return {
      "articles": [
        { "id": 1, "name": "water", "price": 100 },
        { "id": 2, "name": "honey", "price": 200 },
        { "id": 3, "name": "mango", "price": 400 },
        { "id": 4, "name": "tea", "price": 1000 }
      ],
      "carts": [
        {
          "id": 1,
          "items": [
            { "article_id": 1, "quantity": 6 },
            { "article_id": 2, "quantity": 2 },
            { "article_id": 4, "quantity": 1 }
          ]
        },
        {
          "id": 2,
          "items": [
            { "article_id": 2, "quantity": 1 },
            { "article_id": 3, "quantity": 3 }
          ]
        },
        {
          "id": 3,
          "items": []
        }
      ]
    }


@fixture
def payload_output_level1():
    return {
        "carts": [
            {
                "id": 1,
                "total": 2000
            },
            {
                "id": 2,
                "total": 1400
            },
            {
                "id": 3,
                "total": 0
            }
        ]
    }


client = Client()


def test_level1_status_code_and_output_ok(payload_input_level1, payload_output_level1):
    """Checks if the endpoint responds 201 Ok"""
    response = client.post(reverse('level1'), json.dumps(payload_input_level1), content_type="application/json")
    assert response.status_code == 201
    assert json.loads(response.getvalue().decode('utf-8')) == payload_output_level1

def test_level1_method_get_not_allowed():
    expected = {'detail': 'Method "GET" not allowed.'}
    response = client.get(reverse('level1'), content_type='application/json')
    assert json.loads(response.getvalue().decode('utf-8')) == expected

def test_level1_payload_empty():
    expected = {'articles': ['This field is required.'], 'carts': ['This field is required.']}
    payload_input_level1 = {}
    response = client.post(reverse('level1'), json.dumps(payload_input_level1), content_type="application/json")
    assert json.loads(response.getvalue().decode('utf-8')) == expected

def test_level1_payload_empty_articles():
    expected = {'articles': ['This field is required.']}
    payload_input_level1 = {"carts": [{"id": 1, "items": [{"article_id": 1, "quantity": 6}]}]}
    response = client.post(reverse('level1'), json.dumps(payload_input_level1), content_type="application/json")
    assert json.loads(response.getvalue().decode('utf-8')) == expected

def test_level1_payload_empty_carts():
    expected = {'carts': ['This field is required.']}
    payload_input_level1 = {"articles": [{"id": 1, "name": "water", "price": 100}]}
    response = client.post(reverse('level1'), json.dumps(payload_input_level1), content_type="application/json")
    assert json.loads(response.getvalue().decode('utf-8')) == expected
