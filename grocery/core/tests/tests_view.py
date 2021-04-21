import json

from django.test import Client
from django.urls import reverse
from pytest import fixture


client = Client()

# Test View for level 1


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
    return {"carts": [{"id": 1, "total": 2000}, {"id": 2, "total": 1400}, {"id": 3, "total": 0}]}


def test_level1_status_code_and_output_ok(payload_input_level1, payload_output_level1):
    """Checks if the endpoint responds 201 Ok , Checks if the endpoint returns correctly"""
    response = client.post(reverse('level1'), json.dumps(payload_input_level1), content_type="application/json")
    assert response.status_code == 201
    assert json.loads(response.getvalue().decode('utf-8')) == payload_output_level1

def test_level1_method_get_not_allowed():
    """Checks if the Method "GET" is not allowed."""
    expected = {'detail': 'Method "GET" not allowed.'}
    response = client.get(reverse('level1'), content_type='application/json')
    assert json.loads(response.getvalue().decode('utf-8')) == expected

def test_level1_payload_empty():
    """Checks the message error if payload is empty"""
    expected = {'articles': ['This field is required.'], 'carts': ['This field is required.']}
    payload_input_level1 = {}
    response = client.post(reverse('level1'), json.dumps(payload_input_level1), content_type="application/json")
    assert json.loads(response.getvalue().decode('utf-8')) == expected

def test_level1_payload_empty_articles():
    """Checks the message error if payload doesn't have the articles"""
    expected = {'articles': ['This field is required.']}
    payload_input_level1 = {"carts": [{"id": 1, "items": [{"article_id": 1, "quantity": 6}]}]}
    response = client.post(reverse('level1'), json.dumps(payload_input_level1), content_type="application/json")
    assert json.loads(response.getvalue().decode('utf-8')) == expected

def test_level1_payload_empty_carts():
    """Checks the message error if payload doesn't have the carts"""
    expected = {'carts': ['This field is required.']}
    payload_input_level1 = {"articles": [{"id": 1, "name": "water", "price": 100}]}
    response = client.post(reverse('level1'), json.dumps(payload_input_level1), content_type="application/json")
    assert json.loads(response.getvalue().decode('utf-8')) == expected


# Test View for level 2

@fixture
def payload_input_level2():
    return {
        "articles": [
            {"id": 1, "name": "water", "price": 100},
            {"id": 2, "name": "honey", "price": 200},
            {"id": 3, "name": "mango", "price": 400},
            {"id": 4, "name": "tea", "price": 1000},
        ],
        "carts": [
            {
                "id": 1,
                "items": [
                    {"article_id": 1, "quantity": 6},
                    {"article_id": 2, "quantity": 2},
                    {"article_id": 4, "quantity": 1},
                ],
            },
            {"id": 2, "items": [{"article_id": 2, "quantity": 1}, {"article_id": 3, "quantity": 3}]},
            {"id": 3, "items": []},
        ],
        "delivery_fees": [
            {"eligible_transaction_volume": {"min_price": 0, "max_price": 1000}, "price": 800},
            {"eligible_transaction_volume": {"min_price": 1000, "max_price": 2000}, "price": 400},
            {"eligible_transaction_volume": {"min_price": 2000, "max_price": None}, "price": 0},
        ],
    }


@fixture
def payload_output_level2():
    return {"carts": [{"id": 1, "total": 2000}, {"id": 2, "total": 1800}, {"id": 3, "total": 800}]}


def test_level2_status_code_and_output_ok(payload_input_level2, payload_output_level2):
    """Checks if the endpoint responds 201 Ok , Checks if the endpoint returns correctly"""
    response = client.post(reverse('level2'), json.dumps(payload_input_level2), content_type="application/json")
    assert response.status_code == 201
    assert json.loads(response.getvalue().decode('utf-8')) == payload_output_level2


def test_level2_method_get_not_allowed():
    """Checks if the Method "GET" is not allowed."""
    expected = {'detail': 'Method "GET" not allowed.'}
    response = client.get(reverse('level2'), content_type='application/json')
    assert json.loads(response.getvalue().decode('utf-8')) == expected


def test_level2_payload_empty_carts():
    """Checks the message error if payload doesn't have the carts"""
    expected = {'carts': ['This field is required.']}
    payload_input_level2 = {"delivery_fees": [{"eligible_transaction_volume": {"min_price": 0, "max_price": 1000}, "price": 800}],
                            "articles": [{"id": 1, "name": "water", "price": 100}]
                            }
    response = client.post(reverse('level2'), json.dumps(payload_input_level2), content_type="application/json")
    assert json.loads(response.getvalue().decode('utf-8')) == expected


def test_level2_payload_empty_articles():
    """Checks the message error if payload doesn't have the articles"""
    expected = {'articles': ['This field is required.']}
    payload_input_level2 = {"delivery_fees": [{"eligible_transaction_volume": {"min_price": 0, "max_price": 1000}, "price": 800}],
                            "carts": [{"id": 1, "items": [{"article_id": 1, "quantity": 6}]}]
                            }
    response = client.post(reverse('level2'), json.dumps(payload_input_level2), content_type="application/json")
    assert json.loads(response.getvalue().decode('utf-8')) == expected


def test_level2_payload_empty_delivery_fees():
    """Checks the message error if payload doesn't have the delivery fees"""
    expected = {'delivery_fees': ['This field is required.']}
    payload_input_level2 = {"articles": [{"id": 1, "name": "water", "price": 100}],
                            "carts": [{"id": 1, "items": [{"article_id": 1, "quantity": 6}]}]
                            }
    response = client.post(reverse('level2'), json.dumps(payload_input_level2), content_type="application/json")
    assert json.loads(response.getvalue().decode('utf-8')) == expected


# Test View for level 3

@fixture
def payload_input_level3():
    return {
      "articles": [
        { "id": 1, "name": "water", "price": 100 },
        { "id": 2, "name": "honey", "price": 200 },
        { "id": 3, "name": "mango", "price": 400 },
        { "id": 4, "name": "tea", "price": 1000 },
        { "id": 5, "name": "ketchup", "price": 999 },
        { "id": 6, "name": "mayonnaise", "price": 999 },
        { "id": 7, "name": "fries", "price": 378 },
        { "id": 8, "name": "ham", "price": 147 }
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
          "items": [
            { "article_id": 5, "quantity": 1 },
            { "article_id": 6, "quantity": 1 }
          ]
        },
        {
          "id": 4,
          "items": [
            { "article_id": 7, "quantity": 1 }
          ]
        },
        {
          "id": 5,
          "items": [
            { "article_id": 8, "quantity": 3 }
          ]
        }
      ],
      "delivery_fees": [
        {
          "eligible_transaction_volume": {
            "min_price": 0,
            "max_price": 1000
          },
          "price": 800
        },
        {
          "eligible_transaction_volume": {
            "min_price": 1000,
            "max_price": 2000
          },
          "price": 400
        },
        {
          "eligible_transaction_volume": {
            "min_price": 2000,
            "max_price": None
          },
          "price": 0
        }
      ],
      "discounts": [
        { "article_id": 2, "type": "amount", "value": 25 },
        { "article_id": 5, "type": "percentage", "value": 30 },
        { "article_id": 6, "type": "percentage", "value": 30 },
        { "article_id": 7, "type": "percentage", "value": 25 },
        { "article_id": 8, "type": "percentage", "value": 10 }
      ]
    }


@fixture
def payload_output_level3():
    return {"carts": [{"id": 1, "total": 2350}, {"id": 2, "total": 1775}, {"id": 3, "total": 1798}, {"id": 4, "total": 1083}, {"id": 5, "total": 1196},]}


def test_level3_status_code_and_output_ok(payload_input_level3, payload_output_level3):
    """Checks if the endpoint responds 201 Ok , Checks if the endpoint returns correctly"""
    response = client.post(reverse('level3'), json.dumps(payload_input_level3), content_type="application/json")
    assert response.status_code == 201
    assert json.loads(response.getvalue().decode('utf-8')) == payload_output_level3


def test_level3_method_get_not_allowed():
    """Checks if the Method "GET" is not allowed."""
    expected = {'detail': 'Method "GET" not allowed.'}
    response = client.get(reverse('level3'), content_type='application/json')
    assert json.loads(response.getvalue().decode('utf-8')) == expected


def test_level3_payload_empty_carts():
    """"Checks the message error if payload doesn't have the carts"""
    expected = {'carts': ['This field is required.']}
    payload_input_level3 = {"delivery_fees": [{"eligible_transaction_volume": {"min_price": 0, "max_price": 1000}, "price": 800}],
                            "articles": [{"id": 1, "name": "water", "price": 100}],
                            "discounts": [{"article_id": 2, "type": "amount", "value": 25}],
                            }
    response = client.post(reverse('level3'), json.dumps(payload_input_level3), content_type="application/json")
    assert json.loads(response.getvalue().decode('utf-8')) == expected

def test_level3_payload_empty_articles():
    """"Checks the message error if payload doesn't have the articles"""
    expected = {'articles': ['This field is required.']}
    payload_input_level3 = {"delivery_fees": [{"eligible_transaction_volume": {"min_price": 0, "max_price": 1000}, "price": 800}],
                            "carts": [{"id": 1, "items": [{"article_id": 1, "quantity": 6}]}],
                            "discounts": [{"article_id": 2, "type": "amount", "value": 25}],
                            }
    response = client.post(reverse('level3'), json.dumps(payload_input_level3), content_type="application/json")
    assert json.loads(response.getvalue().decode('utf-8')) == expected


def test_level3_payload_empty_delivery_fees():
    """Checks the message error if payload doesn't have the delivery fees"""
    expected = {'delivery_fees': ['This field is required.']}
    payload_input_level3 = {"articles": [{"id": 1, "name": "water", "price": 100}],
                            "carts": [{"id": 1, "items": [{"article_id": 1, "quantity": 6}]}],
                            "discounts": [{"article_id": 2, "type": "amount", "value": 25}],
                            }
    response = client.post(reverse('level3'), json.dumps(payload_input_level3), content_type="application/json")
    assert json.loads(response.getvalue().decode('utf-8')) == expected


def test_level3_payload_empty_discounts():
    """Checks the message error if payload doesn't have the discounts"""
    expected = {'discounts': ['This field is required.']}
    payload_input_level3 = {"articles": [{"id": 1, "name": "water", "price": 100}],
                            "carts": [{"id": 1, "items": [{"article_id": 1, "quantity": 6}]}],
                            "delivery_fees": [{"eligible_transaction_volume": {"min_price": 0, "max_price": 1000}, "price": 800}],
                            }
    response = client.post(reverse('level3'), json.dumps(payload_input_level3), content_type="application/json")
    assert json.loads(response.getvalue().decode('utf-8')) == expected