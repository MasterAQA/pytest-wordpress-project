from tests.rest_api.fixtures import *



# ---------------Positive Test Posts----------
def test_new_post_and_delete_should_work(check_test_post):

    data = {
        "title": "test",
        "status": "publish",
        "content": "test content",
    }
    response = requests.post(root_url + "/posts", headers=headers, data=data)
    id = response.json().get("id")

    assert response.status_code == 201
    assert response.json().get("status") == "publish"
    assert response.json()["title"]["rendered"] == "test"
    assert response.json()["content"]["raw"] == "test content"

    check_test_post.delete_by_id(id)


def test_patch_post_and_delete_should_work(check_test_post):
    id_post = check_test_post.create()

    response = requests.patch(
        root_url
        + f"/posts/{id_post}?status=publish&title=test%20patched&content=test%20content%20was%20patched",
        headers=headers,
    )
    response_content = json.loads(response.content)
    assert response.status_code == 200
    assert response_content.get("status") == "publish"
    assert response_content.get("title").get("rendered") == "test patched"
    assert response_content.get("content").get("raw") == "test content was patched"

    check_test_post.delete_by_id(id_post)


# ---------------Negative Test Posts----------
@pytest.mark.xfail
def test_new_post_and_delete_xfail_auth(check_test_post):
    id_post = check_test_post.create()

    data = {
        "title": "test",
        "status": "publish",
        "content": "test content",
    }

    response = requests.post(root_url + f"/posts/{id_post}", headers=headers, data=data)

    try:
        assert response.status_code == 401
    finally:
        check_test_post.delete_by_id(id_post)


@pytest.mark.xfail
def test_new_post_and_delete_xfail_data(check_test_post):
    id_post = check_test_post.create()

    data = {
        "title": "test",
        "status": "publish",
        "content": "test content",
    }

    response = requests.post(root_url + f"/posts/{id_post}", headers=headers, data=data)

    try:
        assert response.status_code == 404
    finally:
        check_test_post.delete_by_id(id_post)


@pytest.mark.xfail
def test_patch_post_and_delete_xfail_auth(check_test_post):
    id_post = check_test_post.create()

    response = requests.patch(
        root_url
        + f"/posts/{id_post}?status=publish&title=test%20patched&content=test%20content%20was%20patched",
        headers=headers,
    )

    try:
        assert response.status_code == 401
    finally:
        check_test_post.delete_by_id(id_post)


@pytest.mark.xfail
def test_patch_post_and_delete_xfail_data(check_test_post):
    id_post = check_test_post.create()

    response = requests.patch(
        root_url
        + f"/posts/{id_post}?status=publish&title=test%20patched&content=test%20content%20was%20patched",
        headers=headers,
    )

    try:
        assert response.status_code == 404
    finally:
        check_test_post.delete_by_id(id_post)
