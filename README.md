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





#### get new access token py refresh token API
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
