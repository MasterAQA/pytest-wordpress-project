from tests.rest_api.fixtures import *



# ---------------Test Auth With Rest Pass----------
def test_auth_with_rest_pass_admin_should_work():
    response = requests.get(root_url + "/users/me?context=view", headers=headers)
    response_content = json.loads(response.content)
    assert response.status_code == 200
    assert response_content.get("name") == "qatesting"


def test_auth_with_rest_pass_should_work():
    response = requests.get(root_url + "/users/me?context=view", headers=headers)
    response_content = json.loads(response.content)
    assert response.status_code == 200
    assert (
        response_content["_links"]["collection"][0]["href"]
        == "http://co67514.tw1.ru/wp-json/wp/v2/users"
    )
    # assert (response_content.get["_links.collection.0.href"] == "https://wpfolder/wp-json/wp/v2/users")
    # assert (response_content.get("_links").get("collection").get([0]).get("href") == "https://wpfolder/wp-json/wp/v2/users")


@pytest.mark.xfail
def test_auth_with_rest_pass_admin_xfail_auth():
    response = requests.get(root_url + "/users/me?context=view", headers=headers)

    assert response.status_code == 401


@pytest.mark.xfail
def test_auth_with_rest_pass_xfail_not_admin():
    response = requests.get(root_url + "/users/me?context=view", headers=headers)
    response_content = json.loads(response.content)
    assert response.status_code == 200
    assert response_content.get("name") != "qatesting"
