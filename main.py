import random
import string
from datetime import datetime
from fastapi import FastAPI
from fastapi import status
from fastapi.responses import JSONResponse

app = FastAPI()
users_db = dict()


def generate_random_string(length=12):
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


@app.post("/users/create")
def user_create():
    # user_id = str(uuid.uuid4())
    user_id = random.randrange(1, 100000)
    name = generate_random_string(10)
    age = random.randint(1, 60)
    is_active = random.choice([True, False])

    new_user = {
        "id": user_id,
        "name": name,
        "age": age,
        "is_active": is_active,
        "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
    }

    users_db[user_id] = new_user
    return new_user


@app.get("/users/list/")
def users_list():
    return users_db


@app.get("/users/{user_id}/")
def users_detail(user_id: int):
    try:
        return users_db[user_id]
    except KeyError:
        return JSONResponse(
            content={"error": "User not found"}, status_code=status.HTTP_404_NOT_FOUND
        )


@app.put("/users/{user_id}/")
def user_update(user_id: int):
    try:
        user = users_db[user_id]
        user["name"] = generate_random_string(10)
        user["age"] = random.randint(1, 60)
        users_db[user_id] = user
        return user
    except KeyError:
        return JSONResponse(
            content={"error": "User not found"}, status_code=status.HTTP_404_NOT_FOUND
        )


@app.delete("/users/{user_id}/")
def user_delete(user_id: int):
    try:
        del users_db[user_id]
        return JSONResponse(
            content={"message": "User deleted successfully"}, status_code=204
        )
    except KeyError:
        return JSONResponse(
            content={"error": "User not found"}, status_code=status.HTTP_404_NOT_FOUND
        )
