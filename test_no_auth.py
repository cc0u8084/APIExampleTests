import requests
from time import sleep
from pydantic import BaseModel, EmailStr

# Note these tests use a public API resource which is designed for testing against.
# Tests which modify data (PUT, PATCH, DELETE) have the behaviour mocked by the API
# provider and will not make changes so are safe to run. 
# As tests do not change underlying data they can be run multiple times in succession 
# without risk that the underlying data has been modified. 

site_URL = 'https://jsonplaceholder.typicode.com'

def test_get_all_users():
    get_users = requests.get(site_URL + '/users')
    assert get_users.status_code == 200
    user_details = get_users.json()
    assert len(user_details) == 10


def test_get_single_user():
    get_user = requests.get(site_URL + '/users/1')
    assert get_user.status_code == 200
    user1_details = get_user.json()
    assert user1_details["name"] == 'Leanne Graham'
    assert "username" in user1_details
    assert "password" not in user1_details


def test_create_new_post():
    post_payload = {
        "title": "Example post",
        "body": "Post body",
        "userId": 1
        }
    
    response = requests.post(site_URL + '/posts', json=post_payload)
    assert response.status_code == 201

    response_content = response.json()
    assert response_content["title"] == "Example post"
    assert response_content["body"] == "Post body"
    assert response_content["userId"] == 1


def test_update_existing_post():
    put_payload = {
        "id": 1,
        "title": "Updated title",
        "body": "Modified body",
        "userId": 2,
    }

    response = requests.put(site_URL + '/posts/1', json=put_payload)
    assert response.status_code == 200

    response_content = response.json()
    assert response_content["id"] == 1
    assert response_content["title"] == "Updated title"
    assert response_content["body"] == "Modified body"
    assert response_content["userId"] == 2


def test_patch_exisiting_post():
    patch_payload = {
        "title": "Patched Title"
    }

    response = requests.patch(site_URL + '/posts/1', json=patch_payload)
    assert response.status_code == 200
    response_content = response.json()
    assert response_content["title"] == "Patched Title"
    assert response_content["body"][:4] == "quia" #checking existing value has not changed

  
def test_delete_existing_post():
    response = requests.delete(site_URL + "/posts/1")
    assert response.status_code == 200

def test_validate_response():
    class User(BaseModel):
        id: int
        name: str
        email: EmailStr

    get_user = requests.get(site_URL + '/users/1')
    assert get_user.status_code == 200
    assert User(**get_user.json())