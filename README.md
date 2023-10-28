# Valify Task

Task built by Django, Django Rest framework, PostgreSQL database, nginx and docker 
- providing following features:
  - User registration
  - User login
  - create secrets
  - retrieve a list secrets.
  - retrieve a list shared secrets.
  - Decrypt and view a shared secret


## Backend dependencies

- [docker](https://docs.docker.com/get-docker/)

## Run Application

#### 1) get a clone from repo or just download it
#### 2) create `.env` file in root directory  
#### 3) Copy `env_files/.env.local` to `.env`
#### 4) run docker compose :

- run the following commnand to build images and run containers
```sh
docker-compose up 
 ```
- or for docker detached mode run :
```sh
docker-compose up --build  -d
 ```
- or for newer vision of docker 
```sh
docker compose up
```
### base_url : `http://127.0.0.1:9999`
### admin panel url : `http://127.0.0.1:9999/admin`
- default admin email `admin@admin.com`
- default admin password `@dmin@123`

### Test cases
- to run test cases:
```sh
docker exec valify_task_app python manage.py test
```
### query  analytics
- to show query analytics, visit `http://127.0.0.1:9999/silk`
- the query  analytics for development only, in production with be not exists automatically (if `DEBUG` is False
and `HTTPS` is allowed)

### postman collection `Valify.postman_collection.json` in the root directory

## APIS



#### register API
- endpoint `POST`: `{{base_url}}/api/oauth/register`
- payload :
```json
{
    "full_name": "<user_full_name>",
    "email": "<user_email>",
    "password": "<user_password>",
    "re_password": "<user_confirm_password>"
}
```
- response sample :
```json
{
    "full_name": "test name",
    "email": "test@test.com"
}
```
- python code:
```python
import requests

response = requests.post("{{base_url}}/api/oauth/register",
        data={
          "full_name": "<user_full_name>",
          "email": "<user_email>",
          "password": "<user_password>",
          "re_password": "<user_confirm_password>"
        }
)
print(response.json())
```
- notes :
  - all fields are required 
  - password must be at least 8 digits and contains lowercase, uppercase letters,special characters and digits 






#### login API
- endpoint `POST` : `{{base_url}}/api/oauth/login`
- payload :
```json
{
    "email": "<user_email>",
    "password": "<user_password>"
}
```
- response sample :
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMDc2MzY2MywiaWF0IjoxNjk4MTcxNjYzLCJqdGkiOiJmZGIzMTMzODcwNzA0YjFkYTMzNDhhZWNiNDIzNmJjZSIsInVzZXJfaWQiOjMsImVtYWlsIjoidGVzdEB0ZXN0LmNvbSIsImZ1bGxfbmFtZSI6Im1vdXNhIG5hZ2VoIn0.M1Wge4zS_r0SDTganoiLM5JQCttvjTKftuth5LiFrlk",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwNzYzNjYzLCJpYXQiOjE2OTgxNzE2NjMsImp0aSI6Ijc2NDY4MjVhNDExNTQ2YzJiNTRlYjRmNWFmMGJjY2EyIiwidXNlcl9pZCI6MywiZW1haWwiOiJ0ZXN0QHRlc3QuY29tIiwiZnVsbF9uYW1lIjoibW91c2EgbmFnZWgifQ.dv9UIo903dW4VO-n8vS9UQL5DoXU5Kp50jTZC1XxT4A"
}
```
- python code:
```python
import requests

response = requests.post("{{base_url}}/api/oauth/login",
        data={
          "email": "<user_email>",
          "password": "<user_password>",
        }
)
print(response.json())
```
- notes :
  - refresh token expires after 1 month
  - access token expires every 20 minutes





#### get new access token by refresh token API
- endpoint `POST` : `{{base_url}}/api/oauth/refresh-token`
- payload :
```json
{
    "refresh": "<refresh_token>"
}
```
- response sample :
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk4MTczMTE0LCJpYXQiOjE2OTgwODcxODksImp0aSI6IjE5NjNiZTlmZjdkNTQ0ZGJiN2E3ZTU3MzUzMTk0YTU4IiwidXNlcl9pZCI6MywiZW1haWwiOiJ0ZXN0QHRlc3QuY29tIiwiZnVsbF9uYW1lIjoibW91c2EgbmFnZWgifQ.eLFbINHkQsQS1uFBw5iod2y9kbmYa4qHkszpN7SjKbI"
}
```
- python code:
```python
import requests

response = requests.post("{{base_url}}/api/oauth/refresh-token",
        data={
          "refresh": "<refresh_token>"
        }
)
print(response.json())
```




#### create secret with ability to share this secret API
- endpoint `POST` : `{{base_url}}/api/secret/`
- payload :
```json
{
    "secret": "<secret>",
    "shared_with": ["<user_1_email>", "<user_2_email>",... ]
}
```
- response sample :
```json
{
    "id": 1,
    "secret": "secret 1"
}
```
- python code:
```python
import requests
token = "<access_token>"
headers = {
    "Authorization": f"Bearer {token}",
}
response = requests.post("{{base_url}}/api/secret/",
        data={
          "secret": "<secret>",
          "shared_with": ["<user_1_email>", "<user_2_email>",... ]
        },
        headers=headers
)
print(response.json())
```
- notes :
  - this api requires authentication using access token as shown in python code
  - `shared_with` can be empty list
  - `secret` must be at least 8 digits 
  - you can not share secrets with yourself (the same email of yours has logged in)
  - all emails in `shared_with` must be users




#### retrieve a list secrets API
- endpoint `GET` : `{{base_url}}/api/secret`
- response sample :
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {   
            "id": 1,
            "secret": "secret 1234",
            "shared_with": [
                {
                    "id": 1,
                    "user": {
                        "full_name": "mousa nageh",
                        "email": "test@test.com"
                    }
                },
                {
                    "id": 2,
                    "user": {
                        "full_name": "Admin",
                        "email": "admin@admin.com"
                    }
                }
            ]
        }
    ]
}
```
- python code:
```python
import requests
token = "<access_token>"
headers = {
    "Authorization": f"Bearer {token}",
}
response = requests.get("{{base_url}}/api/secret", headers=headers)
print(response.json())
```
- notes :
  - this api requires q authentication using access token as shown in python code  
  - data is paginated by 10




####  share  secret with users API
- endpoint `POST` : `{{base_url}}/api/secret/share-with`
- payload :
```json
{
    "secret_id": "<secret_id>",
    "shared_with": ["<user_1_email>", "<user_2_email>",... ]
}
```
- response sample :
```json
{
    "shared_with": [
        "email@email.com"
    ]
}
```
- python code:
```python
import requests
token = "<access_token>"
headers = {
    "Authorization": f"Bearer {token}",
}
response = requests.post("{{base_url}}/api/secret/share-with",
        data={
          "secret": "<secret>",
          "shared_with": ["<user_1_email>", "<user_2_email>",... ]
        },
        headers=headers
)
print(response.json())
```
- notes :
  - this api requires authentication using access token as shown in python code
  - `secret_id` must be exists and owned by user 
  - you can not share secrets with yourself (the same email of yours has logged in)
  - all emails in `shared_with` must be users



#### retrieve a list shared secrets API
- endpoint `GET` : `{{base_url}}/api/secret/shared`
- response sample :
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 4,
            "secret": "gAAAAABlO3c8HDPXD2fi71rkhENy7K9E9sEI2Odn4-Rl8mVsbJZnxx3wfhQj5T89YVeAKjIDTFhYd7xxY0SYpQzOmtalF47lAg==",
            "shared_by": {
                "full_name": "mousa nageh",
                "email": "test@test.com"
            }
        }
    ]
}
```
- python code:
```python
import requests
token = "<access_token>"
headers = {
    "Authorization": f"Bearer {token}",
}
response = requests.get("{{base_url}}/api/secret/shared", headers=headers)
print(response.json())
```
- notes :
  - this api requires q authentication using access token as shown in python code  
  - data is paginated by 10


#### Decrypt shared secret API
- endpoint `GET` : `{{base_url}}/api/secret/shared/<shared_secret_id>`
- response sample :
```json
{
    "secret": "secret 1234"
}
```
- python code:
```python
import requests
token = "<access_token>"
headers = {
    "Authorization": f"Bearer {token}",
}
response = requests.get("{{base_url}}/api/secret/shared/<shared_secret_id>", headers=headers)
print(response.json())
```
- notes :
  - this api requires q authentication using access token as shown in python code
  - `<shared_secret_id>` replaced with shared secret id retrieved from list of shared secrets. 