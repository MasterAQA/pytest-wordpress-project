from tests.rest_api.fixtures import *


# ---------------Positive Test Comments----------
def test_new_comment_and_delete_should_work(check_test_post, check_test_comment):
    id_post = check_test_post.create()

    data = {
        "content": "test comment",
        "post": f"{id_post}",
    }

    response = requests.post(root_url + "/comments", headers=headers, data=data)
    response_content = json.loads(response.content)
    id_comment = response_content.get("id")

    assert response.status_code == 201
    assert response_content.get("status") == "approved"
    assert response_content.get("post") == id_post
    assert response_content["content"]["raw"] == "test comment"

    check_test_comment.delete_by_id(id_comment)
    check_test_post.delete_by_id(id_post)


def test_patch_comment_and_delete_should_work(check_test_post, check_test_comment):
    id_comment, id_post = check_test_comment.create()

    response = requests.patch(
        root_url
        + f"/comments/{id_comment}?content=test%20comment%20was%20patched&post={id_post}",
        headers=headers,
    )
    response_content = json.loads(response.content)
    assert response.status_code == 200
    assert response_content.get("status") == "approved"
    assert response_content.get("post") == id_post
    assert response_content["content"]["raw"] == "test comment was patched"

    check_test_comment.delete_by_id(id_comment)
    check_test_post.delete_by_id(id_post)


# ---------------Negative Test Comments----------
@pytest.mark.xfail
def test_new_comment_and_delete_xfail_auth(check_test_post, check_test_comment):
    id_post = check_test_post.create()


    data = {
        "content": "test comment",
        "post": f"{id_post}",
    }

    response = requests.post(root_url + "/comments", headers=headers, data=data)
    id_comment = response.json().get("id")

    try:
        assert response.status_code == 401
    finally:
        check_test_comment.delete_by_id(id_comment)
        check_test_post.delete_by_id(id_post)


@pytest.mark.xfail
def test_new_comment_and_delete_xfail_data(check_test_post, check_test_comment):
    id_post = check_test_post.create()


    data = {
        "content": "test comment",
        "post": f"{id_post}",
    }

    response = requests.post(root_url + "/comments", headers=headers, data=data)
    id_comment = response.json().get("id")

    try:
        assert response.status_code == 403
    finally:
        check_test_comment.delete_by_id(id_comment)
        check_test_post.delete_by_id(id_post)


@pytest.mark.xfail
def test_patch_comment_and_delete_xfail_auth(check_test_post, check_test_comment):
    id_comment, id_post = check_test_comment.create()

    response = requests.patch(
        root_url
        + f"/comments/{id_comment}?content=test%20comment%20was%20patched&post={id_post}",
        headers=headers,
    )


    try:
        assert response.status_code == 401
    finally:
        check_test_comment.delete_by_id(id_comment)
        check_test_post.delete_by_id(id_post)


@pytest.mark.xfail
def test_patch_comment_and_delete_xfail_id_post(check_test_post, check_test_comment):
    id_comment, id_post = check_test_comment.create()

    response = requests.patch(
        root_url
        + f"/comments/{id_comment}?content=test%20comment%20was%20patched&post={id_post}",
        headers=headers,
    )

    try:
        assert response.status_code == 403
    finally:
        check_test_comment.delete_by_id(id_comment)
        check_test_post.delete_by_id(id_post)


@pytest.mark.xfail
def test_patch_comment_and_delete_xfail_data(check_test_post, check_test_comment):
    id_comment, id_post = check_test_comment.create()

    response = requests.patch(
        root_url
        + f"/comments/{id_comment}?content=test%20comment%20was%20patched&post={id_post}",
        headers=headers,
    )

    try:
        assert response.status_code == 404
    finally:
        check_test_comment.delete_by_id(id_comment)
        check_test_post.delete_by_id(id_post)
