import requests
import random

#To run these tests visit gorest.co.in and request a token then put this in as the token below

site_url = "https://gorest.co.in/public/v2"
token = "replace this text with your token"

def test_get_all_users():
    #Getting data does not require a token
    response = requests.get(site_url + "/users/")
    assert response.status_code == 200
    response_contents = response.json()
    assert len(response_contents) == 10

def test_get_details_of_single_user():
    #Getting all user data then pulling out a single user's details
    response = requests.get(site_url + "/users")
    assert response.status_code == 200
    users = response.json()
    user = next((u for u in users if u["id"] == 8364706), None)
    assert user["name"] == "Vaishnavi Reddy" and user["status"] =="active"

def test_post_new_user_unauthorised():
    new_user_details = {
        "name":"John Smith", 
        "gender":"male", 
        "email":"john.smith@hfsdhfshfsj.com", 
        "status":"active"
        }
    
    response = requests.post(site_url + "/users", json=new_user_details)
    assert response.status_code == 401

def test_post_new_user_authorised():
    #Test fails if the same credentials are uploaded multiple times so randomising email address.
    emailAddress = random.randint(100000, 200000)
    new_user_details = {
        "name":"John Smith", 
        "gender":"male", 
        "email":"john.smith@" + str(emailAddress) + ".com", 
        "status":"active"
        }
    
    headers = {"Authorization":"Bearer " + token}
    response = requests.post(site_url + "/users", json=new_user_details, headers=headers)
    assert response.status_code == 201

