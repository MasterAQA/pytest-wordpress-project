from tests.rest_api.fixtures import *


def test_e2e_should_work():
    # auth_with_rest_pass_admin
    response = requests.get(root_url + "/users/me?context=view", headers=headers)

    assert response.status_code == 200
    assert response.json().get("name") == "qatesting"



    # new_post_and_delete
    data = {
        "title": "test",
        "status": "publish",
        "content": "test content",
    }
    response = requests.post(root_url + "/posts", headers=headers, data=data)
    id_post = response.json().get("id")

    assert response.status_code == 201
    assert response.json().get("status") == "publish"
    assert response.json()["title"]["rendered"] == "test"
    assert response.json()["content"]["raw"] == "test content"



    # patch_post
    response = requests.patch(
        root_url
        + f"/posts/{id_post}?status=publish&title=test%20patched&content=test%20content%20was%20patched",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json().get("status") == "publish"
    assert response.json()["title"]["rendered"] == "test patched"
    assert response.json()["content"]["raw"] == "test content was patched"



    # new comment
    data = {
        "content": "test comment",
        "post": f"{id_post}",
    }

    response = requests.post(root_url + "/comments", headers=headers, data=data)
    id_comment = response.json().get("id")

    assert response.status_code == 201
    assert response.json().get("status") == "approved"
    assert response.json()["content"]["raw"] == "test comment"



    # patch comment
    response = requests.patch(
        root_url
        + f"/comments/{id_comment}?content=test%20comment%20was%20patched&post={id_post}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json().get("status") == "approved"
    assert response.json().get("post") == id_post
    assert response.json()["content"]["raw"] == "test comment was patched"



    # delete comment
    response = requests.delete(
        root_url + f"/comments/{id_comment}?force=true", headers=headers
    )

    assert response.status_code == 200



    # delete post
    response = requests.delete(
        root_url + f"/posts/{id_post}?force=true", headers=headers
    )

    assert response.status_code == 200



    # new order
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
    id_order = response.json().get("id")

    assert response.status_code == 201
    assert response.json()["billing"]["first_name"] == f"test_{rand_first_name}"
    assert response.json()["billing"]["last_name"] == f"test_{rand_last_name}"
    assert response.json()["billing"]["email"] == f"test_{rand_first_name}.{rand_last_name}@example.com"
    assert response.json()["billing"]["city"] == "San Francisco"



    # change status order
    status = choice(["pending", "processing", "on-hold", "completed", "cancelled", "refunded", "failed"])

    data = {
        "status": status,
    }

    response = wcapi.put(f"orders/{id_order}", data)

    assert response.status_code == 200
    assert response.json().get("status") == status



    # delete order
    response = wcapi.delete(f"orders/{id_order}", params={"force": True})

    assert response.status_code == 200
    assert response.json()["billing"]["city"] == "San Francisco"