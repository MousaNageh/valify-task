user_valid_dataset = [
    {
        "email": "mousa@mousa.com",
        "password": "Mousa@mousa1",
        "full_name": "mousa nageh",
    },
    {
        "email": "admin@admin.com",
        "password": "Mousa@mousa1",
        "full_name": "mousa nageh",
    },
]


register_dataset = {
    "weak_password": {
        "full_name": "mousa nageh",
        "email": "test@test.com",
        "password": "1343456754",
        "re_password": "1343456754",
    },
    "empty_password": {
        "full_name": "mousa nageh",
        "email": "test@test.com",
        "password": "",
        "re_password": "",
    },
    "not_equal_passwords_passwords": {
        "full_name": "mousa nageh",
        "email": "test@test.com",
        "password": "Mousa@mousa1",
        "re_password": "Mousa@mousa12",
    },
    "not_valid_email": {
        "full_name": "mousa nageh",
        "email": "test",
        "password": "Mousa@mousa1",
        "re_password": "Mousa@mousa1",
    },
    "empty_email": {
        "full_name": "mousa nageh",
        "email": "",
        "password": "Mousa@mousa1",
        "re_password": "Mousa@mousa1",
    },
    "empty_full_name": {
        "full_name": "",
        "email": "test@test.com",
        "password": "Mousa@mousa1",
        "re_password": "Mousa@mousa1",
    },
    "valid_data": {
        "full_name": "mousa nageh",
        "email": "test@test.com",
        "password": "Mousa@mousa1",
        "re_password": "Mousa@mousa1",
    },
}


queryset_dataset = {
    "empty_email": {
        "email": "",
        "password": "Mousa@mousa1",
        "full_name": "mousa nageh",
    },
    "empty_password": {
        "email": "test@test",
        "password": "",
        "full_name": "mousa nageh",
    },
    "empty_full_name": {
        "email": "test@test",
        "password": "Mousa@mousa1",
        "full_name": "",
    },
}
