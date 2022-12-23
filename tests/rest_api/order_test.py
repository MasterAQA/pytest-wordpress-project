
from tests.rest_api.fixtures import *



# ---------------Positive Test Orders----------
def test_get_new_order_should_work(check_test_order):
    id = check_test_order.create()

    response = wcapi.get(f"orders/{id}")
    response_content = response.json()

    assert response.status_code == 200
    assert response_content["id"] == id
    assert response_content["billing"]["city"] == "San Francisco"



def test_new_order_should_work():
    rand_first_name = names.get_first_name()
    rand_last_name = names.get_last_name()
    status = choice(["pending", "processing", "on-hold", "completed", "cancelled", "refunded", "failed"])

    data = {
        "payment_method": "cod",
        "payment_method_title": "Оплатапридоставке",
        "status": status,
        'created_via': 'rest-api',
        "billing": {
            "first_name": f"test_{rand_first_name}",
            "last_name": f"test_{rand_last_name}",
            "address_1": "969 Market",
            "address_2": "",
            "city": "San Francisco",
            "state": "CA",
            "postcode": "94103",
            "country": "US",
            "email": f"test_{rand_first_name}.{rand_last_name}@example.com",
            "phone": "(555) 555-5555"
        },
        "shipping": {
            "first_name": f"test_{rand_first_name}",
            "last_name": f"test_{rand_last_name}",
            "address_1": "969 Market",
            "address_2": "",
            "city": "San Francisco",
            "state": "CA",
            "postcode": "94103",
            "country": "US"
        },
        "line_items": [
            {
                "product_id": choice([233, 244, 246, 231, 226, 225, 227, 228, 229, 230]),
                "quantity": 1
            },
            {
                "product_id": randint(226, 233),
                "quantity": 1
            },
            {
                "product_id": 221,
                "variation_id": 240,
                "quantity": 1
            }
        ],
        "shipping_lines": [
            {
                "method_id": "local_pickup",
                "method_title": "Самовывоз",
                'total': '0.00',
            }
        ]
    }

    # --------Create Order--------

    response = wcapi.post("orders", data)
    response_content = response.json()

    assert response.status_code == 201
    assert response_content["billing"]["first_name"] == f"test_{rand_first_name}"
    assert response_content["billing"]["last_name"] == f"test_{rand_last_name}"
    assert response_content["billing"]["email"] == f"test_{rand_first_name}.{rand_last_name}@example.com"
    assert response_content["billing"]["city"] == "San Francisco"


def test_change_status_order_should_work(check_test_order):
    id = check_test_order.create()
    status = choice(["pending", "processing", "on-hold", "completed", "cancelled", "refunded", "failed"])

    data = {
        "status": status,
    }

    response = wcapi.put(f"orders/{id}", data)
    response_content = response.json()

    assert response.status_code == 200
    assert response_content.get("status") == status


def test_delete_order_should_work(check_test_order):
    id = check_test_order.create()

    response = wcapi.delete(f"orders/{id}", params={"force": True})
    response_content = response.json()

    assert response.status_code == 200
    assert response_content["billing"]["city"] == "San Francisco"












# ---------------Negative Test Orders----------
@pytest.mark.xfail
def test_get_new_order_xfail_auth_wcapi(check_test_order):
    id = check_test_order.create()

    response = wcapi.get(f"orders/{id}")

    assert response.status_code == 401


@pytest.mark.xfail
def test_get_new_order_xfail_incorrect_id(check_test_order):
    id = check_test_order.create()

    response = wcapi.get(f"orders/{id}")

    assert response.status_code == 404







@pytest.mark.xfail
def test_new_order_xfail_invalid_param():
    rand_first_name = names.get_first_name()
    rand_last_name = names.get_last_name()
    status = choice(["pending", "processing", "on-hold", "completed", "cancelled", "refunded", "failed"])

    data = {
        "payment_method": "cod",
        "payment_method_title": "Оплатапридоставке",
        "status": status,
        'created_via': 'rest-api',
        "billing": {
            "first_name": f"test_{rand_first_name}",
            "last_name": f"test_{rand_last_name}",
            "address_1": "969 Market",
            "address_2": "",
            "city": "San Francisco",
            "state": "CA",
            "postcode": "94103",
            "country": "US",
            "email": f"test_{rand_first_name}.{rand_last_name}@example.com",
            "phone": "(555) 555-5555"
        },
        "shipping": {
            "first_name": f"test_{rand_first_name}",
            "last_name": f"test_{rand_last_name}",
            "address_1": "969 Market",
            "address_2": "",
            "city": "San Francisco",
            "state": "CA",
            "postcode": "94103",
            "country": "US"
        },
        "line_items": [
            {
                "product_id": choice([233, 244, 246, 231, 226, 225, 227, 228, 229, 230]),
                "quantity": 1
            },
            {
                "product_id": randint(226, 233),
                "quantity": 1
            },
            {
                "product_id": 221,
                "variation_id": 240,
                "quantity": 1
            }
        ],
        "shipping_lines": [
            {
                "method_id": "local_pickup",
                "method_title": "Самовывоз",
                'total': '0.00',
            }
        ]
    }


    response = wcapi.post("orders", data)
    response_content = response.json()

    assert response.status_code == 400
    assert response_content["code"] == "rest_invalid_param"
    assert "Неверный параметр:" in response_content["message"]





@pytest.mark.xfail
def test_change_status_order_xfail_invalid_param(check_test_order):
    id = check_test_order.create()
    status = choice(["pending", "processing", "on-hold", "completed", "cancelled", "refunded", "failed"])

    data = {
        "status": status,
    }

    response = wcapi.put(f"orders/{id}", data)
    response_content = response.json()

    assert response.status_code == 400
    assert response_content["code"] == "rest_invalid_param"
    assert "Неверный параметр:" in response_content["message"]


@pytest.mark.xfail
def test_change_status_order_xfail_invalid_id(check_test_order):
    id = check_test_order.create()
    status = choice(["pending", "processing", "on-hold", "completed", "cancelled", "refunded", "failed"])

    data = {
        "status": status,
    }

    response = wcapi.put(f"orders/{id}", data)
    response_content = response.json()

    assert response.status_code == 400
    assert response_content["code"] == "woocommerce_rest_shop_order_invalid_id"
    assert "Неверный ID" in response_content["message"]


@pytest.mark.xfail
def test_delete_order_xfail_invalid_id(check_test_order):
    id = check_test_order.create()

    response = wcapi.delete(f"orders/{id}", params={"force": True})
    response_content = response.json()

    assert response.status_code == 404
    assert response_content["code"] == "woocommerce_rest_shop_order_invalid_id"
    assert "Неверный ID" in response_content["message"]
