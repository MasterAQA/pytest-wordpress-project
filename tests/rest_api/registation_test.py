from tests.rest_api.fixtures import *


@pytest.fixture
def random_data():
    rand_first_name = names.get_first_name()
    rand_last_name = names.get_last_name()

    data = {
            "username": f"test_{rand_first_name}{rand_last_name}",
            "email": f"test_{rand_first_name}.{rand_last_name}@example.com",
            "password": "test_password",
        }

    return data





# ---------------Positive Test Reg With Rest Pass----------
def test_reg_with_rest_pass_should_work(check_test_user, random_data):
    response = requests.post(root_url + "/users", headers=headers, data=random_data)
    response_content = json.loads(response.content)

    assert response.status_code == 201
    assert "test_" in response_content.get("username")
    assert "test_" in response_content.get("email")
    assert "test_" in response_content.get("nickname")
    # assert response_content.get("link") == "https://wpfolder/author/test_username/"

    check_test_user.delete_by_id(response_content["id"])


# ---------------Negative Test Reg With Rest Pass----------
@pytest.mark.xfail
def test_reg_with_rest_pass_xfail_auth(check_test_user, random_data):
    response = requests.post("https://wpfolder/users", headers=headers, data=random_data)
    response_content = json.loads(response.content)

    try:
        assert response.status_code == 401
    finally:
        check_test_user.delete_by_id(response_content["id"])


@pytest.mark.xfail(reason="Нету или неправильно введён username")
def test_reg_with_rest_pass_xfail_not_username_or_invalid_username(check_test_user, random_data):
    response = requests.post(root_url + "/users", headers=headers, data=random_data)
    response_content = json.loads(response.content)

    try:
        assert response.status_code == 400
        assert response_content.get("message") == "Неверный параметр: username"
        assert response_content.get("code") == "rest_invalid_param"
    finally:
        check_test_user.delete_by_id(response_content["id"])


@pytest.mark.xfail(reason="Нету или неправильно введён email")
def test_reg_with_rest_pass_xfail_not_email(check_test_user, random_data):
    response = requests.post(root_url + "/users", headers=headers, data=random_data)
    response_content = json.loads(response.content)

    try:
        assert response.status_code == 400
        assert response_content.get("message") == "Неверный параметр: email"
    finally:
        check_test_user.delete_by_id(response_content["id"])


@pytest.mark.xfail(reason="Нету или неправильно введён password")
def test_reg_with_rest_pass_xfail_not_pass(check_test_user, random_data):
    response = requests.post(root_url + "/users", headers=headers, data=random_data)
    response_content = json.loads(response.content)

    try:
        assert response.status_code == 400
        assert response_content.get("message") == "Неверный параметр: password"
    finally:
        check_test_user.delete_by_id(response_content["id"])


@pytest.mark.xfail(reason="Ошибка в отправляемых json данных")
def test_reg_with_rest_pass_xfail_data(check_test_user, random_data):
    response = requests.post(root_url + "/users", headers=headers, data=random_data)
    response_content = json.loads(response.content)

    try:
        assert response.status_code == 400
        assert response_content.get("code") == "rest_missing_callback_param"
    finally:
        check_test_user.delete_by_id(response_content["id"])
