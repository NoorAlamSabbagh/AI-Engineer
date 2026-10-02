users = [
    {
        "id": 1,
        "name": "John",
        "email": "john@example.com"
    },
    {
        "id": 2,
        "name": "David",
        "email": "david@example.com"
    }
]

def create_user(name:str,email:str):
    user={
        "id":len(users)+1,
        "name":name,
        "email":email
    }
    users.append(user)
    print(users)

    return user

def get_users_service():
    return users