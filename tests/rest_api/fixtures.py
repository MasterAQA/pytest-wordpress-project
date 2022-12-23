import json
from random import randint, choice

import names
import pytest
import requests

from tests.rest_api.settings import *


class check_user:
    def delete(self):
        response = requests.get(
            root_url + "/users?context=view&search=test_username", headers=headers
        )
        id = json.loads(response.content)

        if response.status_code == 200 and id != []:
            response = requests.delete(
                root_url + f"/users/{id[0].get('id')}?force=true&reassign=1",
                headers=headers,
            )

            assert response.status_code == 200

    def delete_by_id(self, id):
        response = requests.delete(
            root_url + f"/users/{id}?force=true&reassign=1",
            headers=headers,
            )

        assert response.status_code == 200
        # assert response_content["deleted"] == "true"



class check_post:
    def create(self):
        data = {
            "title": "Test",
            "status": "publish",
            "content": "test content",
        }
        response = requests.post(root_url + "/posts", headers=headers, data=data)
        assert response.status_code == 201
        id = json.loads(response.content)
        return int(id.get("id"))

    def delete(self):
        response = requests.get(
            root_url + "/posts?context=view&search=test", headers=headers
        )

        id = json.loads(response.content)

        if response.status_code == 200 and id != []:
            response = requests.delete(
                root_url + f"/posts/{id[0].get('id')}?force=true", headers=headers
            )

            assert response.status_code == 200


    def delete_by_id(self, id):
        response = requests.delete(
            root_url + f"/posts/{id}?force=true", headers=headers
        )

        assert response.status_code == 200


    def delete_patch(self):
        response = requests.get(
            root_url + "/posts?context=view&search=test%20patch", headers=headers
        )

        id = json.loads(response.content)

        if response.status_code == 200 and id != []:
            response = requests.delete(
                root_url + f"/posts/{id[0].get('id')}?force=true", headers=headers
            )

            assert response.status_code == 200


class check_comment:
    def create(self):
        id_post = check_post.create(self)


        data = {
            "content": "test comment",
            "post": f"{id_post}",
        }

        response = requests.post(root_url + "/comments", headers=headers, data=data)
        assert response.status_code == 201
        id_comment = json.loads(response.content)
        return id_comment.get("id"), id_post

    def delete(self):
        response = requests.get(
            root_url + "/comments?context=view&search=test%20comment", headers=headers
        )

        id = json.loads(response.content)

        if response.status_code == 200 and id != []:
            response = requests.delete(
                root_url + f"/comments/{id[0].get('id')}?force=true", headers=headers
            )

            assert response.status_code == 200


    def delete_by_id(self, id):
        response = requests.delete(
            root_url + f"/comments/{id}?force=true", headers=headers
        )

        assert response.status_code == 200

    def delete_patch(self):
        response = requests.get(
            root_url + "/comments?context=view&search=test%20comment%20was%20patched",
            headers=headers,
        )

        id = json.loads(response.content)

        if response.status_code == 200 and id != []:
            response = requests.delete(
                root_url + f"/comments/{id[0].get('id')}?force=true", headers=headers
            )

            assert response.status_code == 200


class check_order:
    def create(self):
        rand_first_name = names.get_first_name()
        rand_last_name = names.get_last_name()
        status = choice(
            [
                "pending",
                "processing",
                "on-hold",
                "completed",
                "cancelled",
                "refunded",
                "failed",
            ]
        )

        data = {
            "payment_method": "cod",
            "payment_method_title": "Оплатапридоставке",
            "status": status,
            "created_via": "rest-api",
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
                "phone": "(555) 555-5555",
            },
            "shipping": {
                "first_name": f"test_{rand_first_name}",
                "last_name": f"test_{rand_last_name}",
                "address_1": "969 Market",
                "address_2": "",
                "city": "San Francisco",
                "state": "CA",
                "postcode": "94103",
                "country": "US",
            },
            "line_items": [
                {
                    "product_id": choice(
                        [233, 244, 246, 231, 226, 225, 227, 228, 229, 230]
                    ),
                    "quantity": 1,
                },
                {"product_id": randint(226, 233), "quantity": 1},
                {"product_id": 221, "variation_id": 240, "quantity": 1},
            ],
            "shipping_lines": [
                {
                    "method_id": "local_pickup",
                    "method_title": "Самовывоз",
                    "total": "0.00",
                }
            ],
        }

        # --------Create Order--------

        response = wcapi.post("orders", data)
        response_content = response.json()

        id = response_content.get("id")

        assert response.status_code == 201
        assert response_content["billing"]["first_name"] == f"test_{rand_first_name}"
        assert response_content["billing"]["last_name"] == f"test_{rand_last_name}"
        assert (
            response_content["billing"]["email"]
            == f"test_{rand_first_name}.{rand_last_name}@example.com"
        )
        assert response_content["billing"]["city"] == "San Francisco"

        return id


@pytest.fixture()
def check_test_user():
    return check_user()


@pytest.fixture()
def check_test_post():
    return check_post()


@pytest.fixture()
def check_test_comment():
    return check_comment()


@pytest.fixture()
def check_test_order():
    return check_order()
